# optihk_web_station

repository of the website portal

## Run locally

Use the bundled Python backend so the contact form can save submissions and CV uploads:

```powershell
python backend.py
```

Then open `http://127.0.0.1:8000`.

Submissions are stored as folders under `data/YYYYMMDD/name/`. Uploaded CV files are stored in `upload_CV/`, and the visitor details are saved as a `.txt` file in the same name folder.
