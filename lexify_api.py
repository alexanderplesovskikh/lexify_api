"""
lexify_api.py

Python client for Lexify API with configurable & validated upload options.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

import requests

# =========================
# Constants
# =========================

DEFAULT_BASE_URL = "https://check.lexiqo.ru"

ALLOWED_STYLES = {
    "По умолчанию",
    "Практика ИВТ",
    "Отключить",
}

ALLOWED_FORMATS = {
    "ГОСТ",
    "Elsevier",
    "Harvard",
    "IEEE",
    "MDPI",
    "Springer",
    "Отключить",
}

ALLOWED_DICTIONARIES = {
    "По умолчанию",
    "Практика ИВТ",
    "Отключить",
}

ALLOWED_AI_DETECTOR = {
    "Включить",
    "Отключить",
}

# =========================
# Exceptions
# =========================

class LexifyAPIError(Exception):
    """Custom exception for API errors."""
    pass


# =========================
# Upload Options
# =========================

@dataclass
class UploadOptions:
    """
    Options for file upload.
    """
    style: str = "Практика ИВТ"
    format: str = "ГОСТ"
    dictionary: str = "Практика ИВТ"
    skip_pages: int = 1
    ai_detector: str = "Отключить"

    def validate(self) -> None:
        """
        Validate all fields before sending request.
        """

        if self.style not in ALLOWED_STYLES:
            raise ValueError(
                f"Invalid style '{self.style}'. Allowed: {ALLOWED_STYLES}"
            )

        if self.format not in ALLOWED_FORMATS:
            raise ValueError(
                f"Invalid format '{self.format}'. Allowed: {ALLOWED_FORMATS}"
            )

        if self.dictionary not in ALLOWED_DICTIONARIES:
            raise ValueError(
                f"Invalid dictionary '{self.dictionary}'. Allowed: {ALLOWED_DICTIONARIES}"
            )

        if self.ai_detector not in ALLOWED_AI_DETECTOR:
            raise ValueError(
                f"Invalid ai_detector '{self.ai_detector}'. Allowed: {ALLOWED_AI_DETECTOR}"
            )

        if not isinstance(self.skip_pages, int) or self.skip_pages < 0:
            raise ValueError("skip_pages must be a non-negative integer")


# =========================
# API Client
# =========================

class LexifyAPI:
    """
    Client for interacting with the Lexify API.
    """

    def __init__(self, admin_token: str, base_url: str = DEFAULT_BASE_URL) -> None:
        self.admin_token = admin_token
        self.base_url = base_url.rstrip("/")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": self.admin_token
        })

    # 🔑 1. Get or create user
    def get_user_token(self, email: str) -> str:
        url = f"{self.base_url}/api/v1/admin/users/view/"
        response = self.session.get(url, params={"email": email})

        if response.status_code == 404:
            response = self.session.post(
                f"{self.base_url}/api/v1/admin/users/create/",
                json={"email": email}
            )

        if not response.ok:
            raise LexifyAPIError(f"User request failed: {response.text}")

        data = response.json()
        token = data.get("token") or data.get("user_token")

        if not token:
            raise LexifyAPIError("Token not found in response")

        return token

    # 📤 2. Upload file
    def upload_file(
        self,
        user_token: str,
        file_path: str | Path,
        options: Optional[UploadOptions] = None
    ) -> dict:
        url = f"{self.base_url}/api/v1/upload/"
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(file_path)

        options = options or UploadOptions()
        options.validate()

        with file_path.open("rb") as f:
            response = self.session.post(
                url,
                headers={"Authorization": user_token},
                files={"file": f},
                data={
                    "style": options.style,
                    "format": options.format,
                    "dictionary": options.dictionary,
                    "skip_pages": str(options.skip_pages),
                    "ai_detector": options.ai_detector,
                }
            )

        if not response.ok:
            raise LexifyAPIError(f"Upload failed: {response.text}")

        return response.json()

    # ⏳ 3. Wait until ready
    def wait_until_ready(
        self,
        file_token: str,
        max_attempts: int = 100,
        delay: int = 5
    ) -> str:
        url = f"{self.base_url}/static/docs/{file_token}.withNotes.docx"

        for _ in range(max_attempts):
            response = self.session.head(url)

            if response.status_code == 200:
                return url

            time.sleep(delay)

        raise TimeoutError("File not ready after waiting")

    # 📥 4. Download file
    def download_file(self, url: str, output_path: str | Path) -> Path:
        output_path = Path(output_path)

        response = self.session.get(url)

        if not response.ok:
            raise LexifyAPIError(f"Download failed: {response.text}")

        output_path.write_bytes(response.content)
        return output_path
    
__all__ = ["LexifyAPI", "UploadOptions", "LexifyAPIError"]