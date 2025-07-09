# 🚀 GitHub Webhook Dashboard

GitHub Webhook Dashboard is a minimal Flask application that enables real-time visualization of your GitHub events. This single-file README contains all the information you need to clone the repository, install dependencies, configure environment variables, run the app on Windows or Linux, expose it on the internet, and customize it.

## 🎉 Overview

💌 Listens for **push**, **pull_request**, and **ping** events sent by GitHub webhooks.
💾 Filters and stores incoming events in a **MongoDB Atlas** database.
🖥️ Displays the latest **10 events** on a sleek dashboard that auto-refreshes every **15 seconds**.

## 🗂️ Project Structure

```
webhook-repo/
├── 🐍 app.py
├── 📜 requirements.txt
├── 🔐 .env.example
├── 🚫 .gitignore
└── 📂 static/
    ├── 📄 index.html
    └── 📄 js/main.js
```
- **app.py** – Flask backend defining `/`, `/health`, `/webhook`, and `/events` routes.
- **requirements.txt** – Python dependencies.
- **.env.example** – Template for environment variables.
- **.gitignore** – Excludes `.env` and `venv/` from Git.
- **static/index.html** – Dashboard layout and styling.
- **static/js/main.js** – Front-end logic to poll events and render cards.

## 💻 Installation & Setup (Windows & Linux)

### 1️⃣ Clone the repository
```bash
git clone git@github.com:AmanChand95/webhook-repo.git
cd webhook-repo
```

### 2️⃣ Create and activate virtual environment

#### Windows 🪟
```powershell
python -m venv venv
.\venv\Scripts\activate
```

#### Linux 🐧
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables
```bash
copy .env.example .env   # Windows
cp .env.example .env     # Linux
```
Open `.env` and set:
```dotenv
MONGO_URI=your_mongodb_atlas_uri
FLASK_ENV=development
SECRET_KEY=your_flask_secret_key
GITHUB_WEBHOOK_SECRET=your_webhook_secret
PORT=5000
```
Ensure `.env` and `venv/` are in `.gitignore` 🔒

## ▶️ Running the Application Locally
```bash
flask run --host=0.0.0.0 --port=5000
```
Open your browser at `http://localhost:5000` to see the live dashboard.

## 🌐 Expose with ngrok
```bash
ngrok http 5000
```
Copy the **HTTPS** forwarding URL (e.g. `https://abcd1234.ngrok.io`) and use it for GitHub webhook configuration.

## 🔧 Configuring GitHub Webhook
1. Go to **GitHub Repo → Settings → Webhooks → Add webhook**
2. **Payload URL:** `https://<ngrok-url>/webhook`
3. **Content type:** `application/json`
4. **Secret:** same as `GITHUB_WEBHOOK_SECRET`
5. **Events:** select **Let me select individual events** → check **Push**, **Pull requests**, **Ping**

Save and verify the test ping in your console 👍

## ✨ Customization & Extension
- To support new event types, update the filter logic in `app.py`.
- Modify `static/js/main.js` to adjust card templates and styling.

---

📜 **License:** MIT | ❤️ Made by Aman Chand
