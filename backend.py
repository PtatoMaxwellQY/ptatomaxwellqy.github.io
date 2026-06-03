import cgi
import json
import mimetypes
import os
import re
import uuid
from datetime import datetime
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"


class SubmissionStore:
    def __init__(self, data_dir=DATA_DIR):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save_submission(self, fields, cv_filename=None, cv_file=None):
        now = datetime.now()
        submission_id = now.strftime("%Y%m%d%H%M%S") + "-" + uuid.uuid4().hex[:8]
        date_dir = self.data_dir / now.strftime("%Y%m%d")
        submission_dir = date_dir / self._safe_folder_name(fields["name"])
        cv_dir = submission_dir / "upload_CV"
        submission_dir.mkdir(parents=True, exist_ok=True)
        cv_dir.mkdir(parents=True, exist_ok=True)

        clean_filename = None
        stored_cv_path = None
        if cv_filename and cv_file:
            clean_filename = self._safe_filename(cv_filename)
            stored_cv_path = self._unique_path(cv_dir / clean_filename)
            with stored_cv_path.open("wb") as output:
                output.write(cv_file.read())

        info_path = self._unique_path(submission_dir / f"{submission_id}.txt")
        info_path.write_text(
            self._format_submission_text(fields, submission_id, now, clean_filename, stored_cv_path),
            encoding="utf-8",
        )

        return submission_id

    def _format_submission_text(self, fields, submission_id, created_at, cv_filename, stored_cv_path):
        stored_cv = str(stored_cv_path.relative_to(self.data_dir)) if stored_cv_path else ""
        return (
            f"Submission ID: {submission_id}\n"
            f"Created at: {created_at.isoformat(timespec='seconds')}\n"
            f"Name: {fields['name']}\n"
            f"Title: {fields.get('title', '')}\n"
            f"Email: {fields['email']}\n"
            f"CV file: {cv_filename or ''}\n"
            f"CV path: {stored_cv}\n"
            "\n"
            f"Message: {fields['message']}\n"
        )

    @staticmethod
    def _safe_folder_name(name):
        folder_name = re.sub(r"[^A-Za-z0-9._-]+", "_", name.strip())
        return folder_name.strip("._-") or "unknown"

    @staticmethod
    def _safe_filename(filename):
        name = Path(filename).name.strip()
        name = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
        return name or "uploaded_cv"

    @staticmethod
    def _unique_path(path):
        if not path.exists():
            return path
        stem = path.stem
        suffix = path.suffix
        parent = path.parent
        counter = 2
        while True:
            candidate = parent / f"{stem}_{counter}{suffix}"
            if not candidate.exists():
                return candidate
            counter += 1


class OptiHKRequestHandler(SimpleHTTPRequestHandler):
    store = None

    def do_POST(self):
        if self.path != "/api/contact":
            self.send_error(HTTPStatus.NOT_FOUND, "Unknown endpoint")
            return

        try:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    "REQUEST_METHOD": "POST",
                    "CONTENT_TYPE": self.headers.get("Content-Type", ""),
                    "CONTENT_LENGTH": self.headers.get("Content-Length", "0"),
                },
            )
            fields = {
                "name": self._form_value(form, "name"),
                "title": self._form_value(form, "title"),
                "email": self._form_value(form, "email"),
                "message": self._form_value(form, "message"),
            }
            self._validate(fields)

            cv_item = form["cv"] if "cv" in form and getattr(form["cv"], "filename", "") else None
            submission_id = self._store().save_submission(
                fields,
                cv_item.filename if cv_item is not None else None,
                cv_item.file if cv_item is not None else None,
            )
        except ValueError as error:
            self._send_json({"ok": False, "error": str(error)}, HTTPStatus.BAD_REQUEST)
            return
        except Exception:
            self._send_json(
                {"ok": False, "error": "The submission could not be saved. Please try again."},
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )
            return

        self._send_json({"ok": True, "submissionId": submission_id}, HTTPStatus.CREATED)

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    @staticmethod
    def _form_value(form, key):
        return form.getfirst(key, "").strip()

    @staticmethod
    def _validate(fields):
        if not fields["name"]:
            raise ValueError("Please enter your name.")
        if "@" not in fields["email"]:
            raise ValueError("Please enter a valid email address.")
        if not fields["message"]:
            raise ValueError("Please enter a message.")

    @classmethod
    def _store(cls):
        if cls.store is None:
            cls.store = SubmissionStore()
        return cls.store

    def _send_json(self, payload, status):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run(host="127.0.0.1", port=8000):
    os.chdir(PROJECT_ROOT)
    mimetypes.add_type("image/webp", ".webp")
    server = ThreadingHTTPServer((host, port), OptiHKRequestHandler)
    print(f"OptiHK website running at http://{host}:{port}")
    print(f"Submissions folder: {DATA_DIR}")
    server.serve_forever()


if __name__ == "__main__":
    run()
