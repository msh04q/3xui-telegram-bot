# 🚀 3X-UI Telegram Bot & IaC Deployment

Автоматизированный комплекс для развертывания VPN-узла на базе **3X-UI (Xray)** с протоколом **VLESS REALITY**, сайтом-камуфляжем и Telegram-ботом на **aiogram 3** для управления доступом.

Вся инфраструктура поднимается и настраивается автоматически с помощью **Terraform** и **Ansible**.

---

## 🛠 Технологический стек

* **Инфраструктура:** Terraform (провайдер Aeza), Ansible
* **Бэкенд бота:** Python 3.11+, `aiogram 3.x`, `aiohttp`
* **VPN Core:** 3X-UI (Xray), VLESS REALITY
* **Безопасность и камуфляж:** Nginx, UFW Firewall

---

## 📐 Архитектура системы

```text
┌─────────────────────────┐
│  Telegram User          │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐       API (aiohttp)      ┌─────────────────────────┐
│ Telegram Bot            ├─────────────────────────►│ 3X-UI Panel / Xray      │
│ (/opt/3xui-bot)         │◄─────────────────────────┤ (Генерация ключей)      │
└─────────────────────────┘      VLESS-ссылки        └────────────┬────────────┘
                                                                  │
                                      TCP 443 (VLESS REALITY)    │
                                      (Не-VPN трафик)             │
                                                                  ▼
                                                     ┌─────────────────────────┐
                                                     │ Nginx Camouflage Site   │
                                                     │ (127.0.0.1:8080)        │
                                                     └─────────────────────────┘
```

---

## 📂 Структура проекта

```text
3xui-telegram-bot/
├── .env.example                 # Шаблон конфигурации бота
├── .gitignore                   # Исключения Git
├── README.md                    # Документация проекта
├── main.py                      # Точка входа бота
├── config.py                    # Валидация и загрузка настроек
├── requirements.txt             # Зависимости Python
│
├── handlers/                    # Обработчики команд Telegram
│   └── user.py                  # Хендлеры /start, генерации ключей и QR
│
├── services/                    # Интеграции
│   └── xui_api.py               # Асинхронный клиент 3X-UI API
│
└── infrastructure/              # Инфраструктура как код (IaC)
    ├── terraform/               # Создание VDS на Aeza
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    │
    └── ansible/                 # Конфигурирование ОС и деплой
        ├── inventory.ini
        └── playbook.yml
```

---

## 🚀 Быстрый старт

### 1. Подготовка локального окружения

Убедитесь, что у вас установлены:
* Terraform (>= 1.5.0)
* Ansible
* Сгенерированная пара SSH-ключей (`~/.ssh/id_rsa` и `~/.ssh/id_rsa.pub`)

### 2. Поднятие VDS через Terraform

Перейдите в директорию Terraform и инициализируйте провайдер:

```bash
cd infrastructure/terraform
terraform init
```

Запустите создание сервера (потребуется API-токен Aeza и ваш публичный SSH-ключ):

```bash
terraform apply \
  -var="aeza_api_token=ВАШ_AEZA_TOKEN" \
  -var="ssh_public_key=$(cat ~/.ssh/id_rsa.pub)"
```

После завершения Terraform выведет IP-адрес созданного сервера:

```text
Outputs:
server_ip = "138.124.xx.xx"
```

### 3. Автоматическая настройка сервера через Ansible

Перейдите в папку Ansible:

```bash
cd ../ansible
```

Откройте `inventory.ini` и укажите полученный IP-адрес:

```ini
[vpn_nodes]
frankfurt.ptr.network ansible_host=138.124.xx.xx ansible_user=root ansible_ssh_private_key_file=~/.ssh/id_rsa
```

Запустите playbook:

```bash
ansible-playbook -i inventory.ini playbook.yml
```

**Что выполнит Playbook:**
* Установит системные утилиты, Nginx, UFW и Python venv.
* Развернет веб-сайт камуфляжа на порту 8080.
* Установит и запустит панель 3x-ui.
* Клонирует бота в `/opt/3xui-bot` и настроит systemd-службу.

### 4. Первичная настройка 3X-UI и .env

Подключитесь к серверу по SSH:

```bash
ssh root@138.124.xx.xx
```

Откройте панель 3X-UI в браузере (`http://138.124.xx.xx:2096`) и создайте VLESS REALITY подключение (Inbound).

Создайте файл конфигурации для бота:

```bash
cd /opt/3xui-bot
cp .env.example .env
nano .env
```

Заполните переменные окружения:

```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyZ
XUI_URL=http://127.0.0.1:2096
XUI_USER=admin
XUI_PASSWORD=your_secure_password
INBOUND_ID=1
```

Перезапустите службу бота:

```bash
systemctl restart 3xui-bot
```

---

## 🔍 Проверка статуса и логов

Проверить статус службы бота на сервере:

```bash
systemctl status 3xui-bot
```

Просмотреть логи бота в реальном времени:

```bash
journalctl -u 3xui-bot -f
```

---

## 🛡 Безопасность

* Порт камуфляжного сайта (8080) закрыт снаружи файрволом UFW и доступен только для проксирования Xray внутри 127.0.0.1.
* Открытые порты системы: `22` (SSH), `80` (HTTP), `443` (VLESS REALITY / HTTPS), `2096` (Панель 3X-UI).

---

## 📝 Лицензия

MIT