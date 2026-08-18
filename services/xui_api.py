
import uuid
import json
import logging
from typing import Optional, Tuple
import aiohttp
import config

logger = logging.getLogger(__name__)

class XUIClient:
    def __init__(self):
        self.base_url = config.XUI_URL
        self.base_path = config.XUI_BASE_PATH
        self.session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True))
        return self.session

    async def login(self) -> bool:
        session = await self._get_session()
        login_url = f"{self.base_url}{self.base_path}/login"
        data = {
            "username": config.XUI_USERNAME,
            "password": config.XUI_PASSWORD
        }
        try:
            async with session.post(login_url, data=data) as resp:
                result = await resp.json()
                if result.get("success"):
                    logger.info("Успешная авторизация в 3X-UI API")
                    return True
                logger.error(f"Ошибка авторизации в 3X-UI: {result.get('msg')}")
                return False
        except Exception as e:
            logger.error(f"Исключение при логине в 3X-UI: {e}")
            return False

    async def add_client(self, tg_user_id: int, username: str) -> Tuple[Optional[str], Optional[str]]:
        session = await self._get_session()
        
        inbound_url = f"{self.base_url}{self.base_path}/panel/api/inbounds/get/{config.INBOUND_ID}"
        async with session.get(inbound_url) as resp:
            inbound_data = await resp.json()
            if not inbound_data.get("success"):
                if await self.login():
                    async with session.get(inbound_url) as retry_resp:
                        inbound_data = await retry_resp.json()
                else:
                    return None, None

        inbound = inbound_data["obj"]
        client_uuid = str(uuid.uuid4())
        email = f"tg_{tg_user_id}_{username or 'user'}"

        client_data = {
            "id": config.INBOUND_ID,
            "settings": json.dumps({
                "clients": [{
                    "id": client_uuid,
                    "email": email,
                    "flow": "xtls-rprx-vision",
                    "enable": True
                }]
            })
        }

        add_url = f"{self.base_url}{self.base_path}/panel/api/inbounds/addClient"
        async with session.post(add_url, json=client_data) as resp:
            res = await resp.json()
            if not res.get("success"):
                logger.error(f"Не удалось добавить клиента: {res.get('msg')}")
                return None, None

        stream_settings = json.loads(inbound.get("streamSettings", "{}"))
        reality_settings = stream_settings.get("realitySettings", {})
        settings = reality_settings.get("settings", {})

        pbk = settings.get("publicKey", "")
        sni = reality_settings.get("serverNames", [""])[0]
        sid = reality_settings.get("shortIds", [""])[0]
        fp = settings.get("fingerprint", "chrome")

        vless_link = (
            f"vless://{client_uuid}@{config.VLESS_SERVER}:{config.VLESS_PORT}"
            f"?type=tcp&security=reality&pbk={pbk}&fp={fp}&sni={sni}&sid={sid}"
            f"&flow=xtls-rprx-vision#{email}"
        )

        return client_uuid, vless_link

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()

xui_client = XUIClient()
