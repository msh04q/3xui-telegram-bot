
import io
import qrcode
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from services.xui_api import xui_client

router = Router()

def get_main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔑 Получить VPN ключ", callback_data="get_vpn")]
        ]
    )

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! Нажми кнопку ниже, чтобы получить ключ доступа к VPN.",
        reply_markup=get_main_keyboard()
    )

@router.callback_query(F.data == "get_vpn")
async def process_get_vpn(callback: CallbackQuery):
    await callback.answer("Генерируем ключ...")
    
    user_id = callback.from_user.id
    username = callback.from_user.username or "user"
    
    client_uuid, vless_link = await xui_client.add_client(user_id, username)
    
    if not vless_link:
        await callback.message.answer("❌ Произошла ошибка при выпуске ключа. Обратитесь к администратору.")
        return

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(vless_link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    photo = BufferedInputFile(img_byte_arr, filename="vpn_qr.png")

    caption = (
        f"✅ **Ваш ключ успешно создан!**\n\n"
        f"Скопируйте ссылку ниже и вставьте её в ваш VLESS-клиент:\n\n"
        f"`{vless_link}`"
    )

    await callback.message.answer_photo(
        photo=photo,
        caption=caption,
        parse_mode="Markdown"
    )
