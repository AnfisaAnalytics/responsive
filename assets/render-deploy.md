# Деплой Flask-приложения на Render через CLI

## 1. Подготовка проекта

### 1.1 Структура проекта
```
my-flask-app/
├── app.py
├── requirements.txt
└── render.yaml
```

### 1.2 Необходимые файлы

**requirements.txt**
```
flask
gunicorn
```

**render.yaml**
```yaml
services:
  - type: web
    name: my-flask-app
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9
```

## 2. Установка Render CLI

```bash
# Для macOS
brew tap render-oss/render
brew install render

# Для Linux через curl
curl -o render https://render.com/download/render-cli/linux
chmod +x render
sudo mv render /usr/local/bin/
```

## 3. Аутентификация

```bash
# Получите API ключ с https://dashboard.render.com/settings/api-keys
render login --api-key YOUR_API_KEY
```

## 4. Команды деплоя

```bash
# Создание нового сервиса
render services create

# Деплой изменений
render services deploy SERVICE_ID

# Проверка статуса
render services status SERVICE_ID

# Просмотр логов
render services logs SERVICE_ID
```

## 5. Полезные команды для отладки

```bash
# Список всех сервисов
render services list

# Информация о конкретном сервисе
render services info SERVICE_ID

# Остановка сервиса
render services suspend SERVICE_ID

# Перезапуск сервиса
render services restart SERVICE_ID
```
