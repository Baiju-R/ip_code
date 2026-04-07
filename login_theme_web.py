"""Simple Flask web app with login interface and light/dark theme changer."""

from flask import Flask, redirect, render_template_string, request, session, url_for

app = Flask(__name__)
app.secret_key = "change-me-in-production"

VALID_USERS = {
    "admin": "admin123",
    "user": "password",
}

PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Simple Login + Theme Changer</title>
    <style>
        :root {
            --bg: #f5f7fb;
            --surface: #ffffff;
            --text: #1f2937;
            --muted: #6b7280;
            --accent: #2563eb;
            --danger: #dc2626;
            --border: #d1d5db;
        }

        body.dark {
            --bg: #111827;
            --surface: #1f2937;
            --text: #f9fafb;
            --muted: #d1d5db;
            --accent: #60a5fa;
            --danger: #f87171;
            --border: #374151;
        }

        * {
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }

        body {
            margin: 0;
            min-height: 100vh;
            background: var(--bg);
            color: var(--text);
            display: grid;
            place-items: center;
            transition: background .2s ease, color .2s ease;
        }

        .card {
            width: min(420px, 92vw);
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.2rem;
            box-shadow: 0 8px 28px rgba(0,0,0,0.08);
        }

        h1 { margin: .3rem 0 1rem; font-size: 1.2rem; }

        label {
            display: block;
            margin: .7rem 0 .25rem;
            color: var(--muted);
            font-size: .9rem;
        }

        input {
            width: 100%;
            padding: .65rem .7rem;
            border: 1px solid var(--border);
            border-radius: 8px;
            background: transparent;
            color: var(--text);
        }

        .row {
            display: flex;
            justify-content: space-between;
            gap: .6rem;
            margin-top: .9rem;
        }

        button {
            border: none;
            border-radius: 8px;
            padding: .65rem .85rem;
            cursor: pointer;
            color: white;
            background: var(--accent);
            font-weight: 600;
        }

        .secondary {
            background: #6b7280;
        }

        .error {
            margin-top: .8rem;
            color: var(--danger);
            font-size: .9rem;
        }

        .welcome {
            margin-bottom: 1rem;
            font-size: .95rem;
            color: var(--muted);
        }
    </style>
</head>
<body>
    <main class="card">
        {% if user %}
            <h1>Welcome, {{ user }} 👋</h1>
            <p class="welcome">You are now logged in.</p>
            <form method="post" action="{{ url_for('logout') }}">
                <button type="submit" class="secondary">Logout</button>
            </form>
        {% else %}
            <h1>Login</h1>
            <form method="post" action="{{ url_for('login') }}">
                <label for="username">Username</label>
                <input id="username" name="username" required />
                <label for="password">Password</label>
                <input id="password" name="password" type="password" required />
                <div class="row">
                    <button type="submit">Sign in</button>
                    <button type="button" class="secondary" onclick="toggleTheme()">Toggle theme</button>
                </div>
                {% if error %}<p class="error">{{ error }}</p>{% endif %}
            </form>
        {% endif %}
    </main>

    <script>
      const savedTheme = localStorage.getItem("theme");
      if (savedTheme === "dark") {
        document.body.classList.add("dark");
      }

      function toggleTheme() {
        document.body.classList.toggle("dark");
        const isDark = document.body.classList.contains("dark");
        localStorage.setItem("theme", isDark ? "dark" : "light");
      }
    </script>
</body>
</html>
"""


@app.get("/")
def index() -> str:
    return render_template_string(PAGE_TEMPLATE, user=session.get("user"), error=None)


@app.post("/login")
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if VALID_USERS.get(username) == password:
        session["user"] = username
        return redirect(url_for("index"))

    return render_template_string(
        PAGE_TEMPLATE,
        user=None,
        error="Invalid username or password.",
    )


@app.post("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
