# 🚀 3X-UI Telegram Bot & IaC Infrastructure

Автоматизированный комплекс для развертывания VPN-узла на базе **3X-UI (Xray)** с протоколом **VLESS REALITY**, сайтом-камуфляжем, Telegram-ботом на **aiogram 3** и готовым стеком мониторинга (**Prometheus + Grafana**).

Вся инфраструктура поднимается через **Terraform**, а подготовка ОС, установка Docker и запуск контейнеров выполняются с помощью **Ansible**.

---

## 🛠 Технологический стек

* **Инфраструктура (IaC):** Terraform (провайдер Aeza), Ansible
* **Контейнеризация:** Docker, Docker Compose
* **Бэкенд бота:** Python 3.11+, `aiogram 3.x`, `aiohttp`
* **VPN Core:** 3X-UI (Xray), VLESS REALITY
* **Безопасность и камуфляж:** Nginx, UFW Firewall
* **Мониторинг:** Prometheus, Grafana (с автопровижионингом дашбордов), Node Exporter

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
│ (Docker Container)      │◄─────────────────────────┤ (Генерация ключей)      │
└─────────────────────────┘      VLESS-ссылки        └────────────┬────────────┘
                                                                  │
                                      TCP 443 (VLESS REALITY)    │
                                      (Не-VPN трафик)             │
                                                                  ▼
┌─────────────────────────┐                          ┌─────────────────────────┐
│ Prometheus + Grafana    │                          │ Nginx Camouflage Site   │
│ (Порт 3000: Grafana)    │                          │ (127.0.0.1:8080)        │
└────────────▲────────────┘                          └─────────────────────────┘
             │
             │ (Сбор метрик CPU/RAM/Network/Disk)
┌────────────┴────────────┐
│ Node Exporter           │
└─────────────────────────┘
```

---

## 📂 Структура проекта

```text
3xui-telegram-bot/
├── Dockerfile                   # Сборка образа Telegram-бота
├── docker-compose.yml           # Оркестрация контейнеров (Bot, Nginx, Prometheus, Grafana)
├── .env.example                 # Шаблон переменных окружения
├── .gitignore                   # Исключения Git
├── README.md                    # Документация проекта
├── main.py                      # Точка входа Telegram-бота
├── config.py                    # Конфигурация и валидация .env
├── requirements.txt             # Зависимости Python
│
├── handlers/                    # Обработчики команд Telegram
│   └── user.py                  # Хендлеры /start, генерация VLESS и QR
│
├── services/                    # Интеграции
│   └── xui_api.py               # Асинхронный клиент 3X-UI API
│
├── monitoring/                  # Конфигурации мониторинга
│   ├── prometheus/
│   │   └── prometheus.yml       # Конфиг сбора метрик с Node Exporter
│   └── grafana/
│       └── provisioning/        # Автонастройка Grafana при старте
│           ├── datasources/
│           │   └── prometheus.yml
│           └── dashboards/
│               ├── dashboards.yml
│               └── node_exporter.json
│
└── infrastructure/              # Инфраструктура как код (IaC)
    ├── terraform/               # Создание VDS на Aeza
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    └── ansible/                 # Установка Docker и развертывание Compose-стека
        ├── inventory.ini
        └── playbook.yml
```

---

## 🚀 Быстрый старт

### 1. Подготовка локального окружения

Убедитесь, что на вашей локальной машине установлены:
* Terraform (>= 1.5.0)
* Ansible
* Пара SSH-ключей (`~/.ssh/id_rsa` и `~/.ssh/id_rsa.pub`)

### 2. Развертывание VDS через Terraform

Перейдите в директорию Terraform и инициализируйте провайдер:

```bash
cd infrastructure/terraform
terraform init
```

Запустите создание сервера (укажите API-токен Aeza и ваш SSH-ключ):

```bash
terraform apply \
  -var="aeza_api_token=ВАШ_AEZA_TOKEN" \
  -var="ssh_public_key=$(cat ~/.ssh/id_rsa.pub)"
```

Запомните IP-адрес из вывода Terraform:

```text
Outputs:
server_ip = "138.124.xx.xx"
```

### 3. Автоматическая настройка сервера через Ansible

Перейдите в папку Ansible:

```bash
cd ../ansible
```

Откройте `inventory.ini` и вставьте IP вашего сервера:

```ini
[vpn_nodes]
frankfurt.ptr.network ansible_host=138.124.xx.xx ansible_user=root ansible_ssh_private_key_file=~/.ssh/id_rsa
```

Запустите playbook для настройки ОС, установки Docker, панели 3X-UI и запуска контейнеров:

```bash
ansible-playbook -i inventory.ini playbook.yml
```

### 4. Настройка 3X-UI и запуск бота

Подключитесь к серверу по SSH:

```bash
ssh root@138.124.xx.xx
```

Откройте веб-панель 3X-UI (`http://138.124.xx.xx:2096`) и создайте подключение VLESS REALITY (Inbound ID: 1).

Перейдите в каталог проекта и скопируйте файл конфигурации:

```bash
cd /opt/3xui-bot
cp .env.example .env
nano .env
```

Укажите ваши данные:

```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyZ
XUI_URL=http://127.0.0.1:2096
XUI_USER=admin
XUI_PASSWORD=your_secure_password
INBOUND_ID=1
GRAFANA_PASSWORD=your_grafana_password
```

Перезапустите стек Docker Compose:

```bash
docker compose restart bot
```

---

## 📊 Мониторинг (Grafana)

После развертывания стека Grafana доступна по адресу:
`http://138.124.xx.xx:3000`

* **Логин:** `admin`
* **Пароль:** Задается переменной `GRAFANA_PASSWORD` в `.env` (по умолчанию `admin_secure_pass`).

Благодаря автопровижионингу, в Grafana автоматически подключен Prometheus в качестве источника данных и загружен дашборд **Node Exporter - Light Dashboard**, показывающий:
* Загрузку процессора (CPU Usage)
* Использование оперативной памяти (RAM Usage)
* Заполненность диска (Disk Space Usage)
* Входящий и исходящий сетевой трафик (Network Traffic)

---

## 🔍 Управление и логи

Просмотр статуса всех контейнеров:

```bash
docker compose ps
```

Просмотр логов Telegram-бота:

```bash
docker compose logs -f bot
```

Перезапуск всей инфраструктуры:

```bash
docker compose restart
```

---

## 🛡 Безопасность

* Порт камуфляжного сайта (8080), Node Exporter (9100) и Prometheus (9090) открыты только локально (127.0.0.1) и недоступны из внешней сети.
* Внешние порты, открытые в файрволе UFW:
  * `22` (SSH)
  * `80` (HTTP / Nginx)
  * `443` (VLESS REALITY / HTTPS)
  * `2096` (Панель 3X-UI)
  * `3000` (Grafana)

---

## 📝 Лицензия

MIT