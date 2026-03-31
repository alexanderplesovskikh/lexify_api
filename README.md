# ✅ Lexify API

Python SDK для API Lexify.

Он позволяет легко:
- создавать пользователей
- загружать документы и настраивать параметры
- проводить анализ документа
- скачивать результаты

---

## 🔗 Ссылки

- 🌐 Веб-сайт: https://check.lexiqo.ru
- 📦 Python Package: https://github.com/alexanderplesovskikh/lexify_api

---

## 📦 Установка

Установка из GitHub:

```bash
pip install git+https://github.com/alexanderplesovskikh/lexify_api.git
```

## 🚀 Начало работы

Пример использования:

_Для получения токена отправьте запрос на email: [lexiqo_app@mail.ru](mailto:lexiqo_app@mail.ru?subject=Запрос%20токена)_

```python
from lexify_api import LexifyAPI, UploadOptions

# Получите токен
api = LexifyAPI(admin_token="your_lexify_token")

# Укажите путь к вашему файлу
input_file = "file.docx"

# Укажите ваш email
user_token = api.get_user_token("user@example.com")

options = UploadOptions(
    style="По умолчанию",
    format="ГОСТ",
    dictionary="По умолчанию",
    skip_pages=1,
    ai_detector="Включить"
)

upload_data = api.upload_file(user_token, input_file, options)

url = api.wait_until_ready(upload_data['file_token'])

output_name = f"Lexify_{input_file}"

path = api.download_file(url, output_name)

if path.exists():
    print(f"✅ SUCCESS: {path}")
else:
    print("❌ FAILED")
```

---

# ✅ Lexify API

Python SDK for interacting with the Lexify API.

It allows you to easily:
- create/get users
- upload documents with configurable options
- wait for processing
- download results

---

## 🔗 Links

- 🌐 Website: https://check.lexiqo.ru
- 📦 Package: https://github.com/alexanderplesovskikh/lexify_api

---

## 📦 Installation

Install from GitHub:

```bash
pip install git+https://github.com/alexanderplesovskikh/lexify_api.git
```

## 🚀 Getting started

Usage example:

```python
from lexify_api import LexifyAPI, UploadOptions

# Get your token
api = LexifyAPI(admin_token="your_lexify_token")

# Change to your file path
input_file = "file.docx"

# Change to your email
user_token = api.get_user_token("user@example.com")

options = UploadOptions(
    style="По умолчанию",
    format="ГОСТ",
    dictionary="По умолчанию",
    skip_pages=1,
    ai_detector="Включить"
)

upload_data = api.upload_file(user_token, input_file, options)

url = api.wait_until_ready(upload_data['file_token'])

output_name = f"Lexify_{input_file}"

path = api.download_file(url, output_name)

if path.exists():
    print(f"✅ SUCCESS: {path}")
else:
    print("❌ FAILED")
```
