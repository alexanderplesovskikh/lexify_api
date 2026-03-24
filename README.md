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
- 📄 API Docs: https://check.lexiqo.ru/docs

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

api = LexifyAPI(admin_token="your_lexify_token")

input_file = "file.docx"

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
