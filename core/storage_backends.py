import os

from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from vercel_blob import (
    BlobFileError,
    BlobRequestError,
    delete as blob_delete,
    head as blob_head,
    put as blob_put,
)


@deconstructible
class VercelBlobStorage(Storage):
    """Django storage backend for Vercel Blob using the official Python SDK."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = os.getenv("BLOB_READ_WRITE_TOKEN", "")
        self.base_url = os.getenv("BLOB_BASE_URL", "").rstrip("/")
        self.access = os.getenv("BLOB_ACCESS", "public")

        if not self.token:
            raise ValueError("BLOB_READ_WRITE_TOKEN is required for VercelBlobStorage")

    def _normalize_name(self, name: str) -> str:
        return name.replace("\\", "/").lstrip("/")

    def _blob_url(self, name: str) -> str:
        normalized_name = self._normalize_name(name)
        if self.base_url:
            return f"{self.base_url}/{normalized_name}"
        return normalized_name

    def _open(self, name, mode="rb"):
        # Public blobs can be read directly by URL.
        import requests

        url = self.url(name)
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return ContentFile(response.content, name=name)

    def _save(self, name, content):
        normalized_name = self._normalize_name(name)
        if hasattr(content, "seek"):
            content.seek(0)
        payload = content.read()
        if isinstance(payload, str):
            payload = payload.encode("utf-8")

        options = {
            "access": self.access,
            "token": self.token,
            "addRandomSuffix": False,
            "allowOverwrite": True,
        }

        result = blob_put(normalized_name, payload, options=options, multipart=True)
        return result["pathname"]

    def delete(self, name):
        try:
            blob_delete(self._blob_url(name), options={"token": self.token})
        except (BlobRequestError, BlobFileError):
            # Ignore missing files for compatibility with Django's default storage behavior.
            return

    def exists(self, name):
        try:
            blob_head(self._blob_url(name), options={"token": self.token})
            return True
        except (BlobRequestError, BlobFileError):
            return False

    def size(self, name):
        meta = blob_head(self._blob_url(name), options={"token": self.token})
        return meta.get("size", 0)

    def url(self, name):
        normalized_name = self._normalize_name(name)
        if self.base_url:
            return f"{self.base_url}/{normalized_name}"

        # If BLOB_BASE_URL is not set, fall back to returning the pathname itself.
        # This still preserves DB values and allows explicit URL resolution later.
        return normalized_name
