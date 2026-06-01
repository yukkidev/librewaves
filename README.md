# LibreWaves

A free, open-source, self-hostable music streaming platform. Upload your own audio files, organize them into playlists, and stream them through a web-based dashboard with a built-in music player.

## Features

- User registration and login
- Audio file upload and management (upload, rename, delete)
- Playlist creation and management
- Built-in music player with play/pause, next/previous, shuffle, and repeat
- Dark-themed UI
- Azure Blob Storage for cloud file storage

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLAlchemy with SQLite
- **Cloud Storage:** Azure Blob Storage
- **Frontend:** HTML, CSS, vanilla JavaScript

## Project Structure

```
librewaves/
├── client/              # Frontend (static HTML/CSS/JS)
│   ├── index.html       # Main dashboard page
│   ├── login.html       # Login/register page
│   ├── test.html        # API test page
│   ├── style.css        # Global styles
│   └── scripts/         # JavaScript files
│       ├── dashboard.js
│       └── login.js
└── server/              # Backend (Flask API)
    └── app.py           # Main application with routes and models
```

## Getting Started

### Prerequisites

- Python 3
- An Azure Storage account

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yukkidev/librewaves.git
   cd librewaves
   ```

2. Install server dependencies:
   ```bash
   pip install flask flask-sqlalchemy flask-jwt-extended azure-storage-blob pyjwt werkzeug
   ```

3. Configure your Azure Blob Storage connection string in `server/app.py`.

### Running

Start the Flask backend:

```bash
python server/app.py
```

The server runs at `http://127.0.0.1:5000`. Open `client/login.html` in your browser to access the frontend.

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Authenticate a user |
| POST | `/logout` | Logout |
| POST | `/upload` | Upload audio files |
| GET | `/files` | List user files |
| PUT | `/rename` | Rename a file |
| DELETE | `/delete` | Delete a file |
| POST | `/playlist` | Create a playlist |
| DELETE | `/playlist/<id>` | Delete a playlist |
| POST | `/playlist/<id>/song` | Add a song to a playlist |
| DELETE | `/playlist/<id>/song/<id>` | Remove a song from a playlist |
