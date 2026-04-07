# ip_code

Simple Python Flask demo for a login webpage interface with a light/dark theme changer.

## Run

```bash
python3 -m pip install flask werkzeug
FLASK_SECRET_KEY='replace-this-secret' python3 login_theme_web.py
```

Open `http://127.0.0.1:5000`.

## Demo credentials

- `admin` / `admin123`
- `user` / `password`

## Notes

- This app is intentionally simple and intended for learning.
- For production, use a database-backed user store, secure secret management, HTTPS, and CSRF protection.
