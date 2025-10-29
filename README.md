# 🤖 AI Blog Generator

Transform any YouTube video into a professional, well-structured blog post in minutes using the power of AI.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Keys](#api-keys)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- 🎥 **YouTube Video Processing** - Paste any YouTube URL and extract audio
- 🎙️ **AI Transcription** - Automatic speech-to-text using AssemblyAI
- 📝 **Blog Generation** - Convert transcripts to engaging blog posts with Groq AI
- 💾 **Save & Organize** - Store all generated blogs in your personal library
- 👤 **User Authentication** - Secure signup/login system
- 📱 **Responsive Design** - Beautiful UI that works on all devices
- ⚡ **Fast Processing** - Groq's LLM delivers results in seconds
- 🎨 **Markdown Support** - Well-formatted blog posts with proper styling

## 🎬 Demo

### Generate Blog from YouTube
![Generate Blog](https://via.placeholder.com/800x400?text=Generate+Blog+Demo)

### View All Blogs
![All Blogs](https://via.placeholder.com/800x400?text=All+Blogs+View)

### Blog Details
![Blog Details](https://via.placeholder.com/800x400?text=Blog+Details+Page)

## 🛠️ Tech Stack

**Backend:**
- Python 3.9+
- Django 5.2.7
- PostgreSQL (Supabase)

**Frontend:**
- HTML5
- Tailwind CSS
- JavaScript (Vanilla)
- Marked.js (Markdown rendering)

**APIs & Services:**
- [AssemblyAI](https://www.assemblyai.com/) - Audio transcription
- [Groq](https://groq.com/) - Fast LLM inference (Llama 3.3 70B)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube audio extraction

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- FFmpeg (required for audio processing)
- PostgreSQL database (or SQLite for development)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-blog-generator.git
cd ai-blog-generator
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### 5. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Database (PostgreSQL)
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432
DB_SSLMODE=require

# API Keys
ASSEMBLYAI_API_KEY=your_assemblyai_key
GROQ_API_KEY=your_groq_key
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## 🔑 API Keys

### AssemblyAI API Key

1. Go to [AssemblyAI](https://www.assemblyai.com/)
2. Sign up for a free account
3. Navigate to your dashboard
4. Copy your API key
5. Add to `.env` file: `ASSEMBLYAI_API_KEY=your_key_here`

**Free Tier:** 5 hours of transcription per month

### Groq API Key

1. Go to [Groq Console](https://console.groq.com/)
2. Sign up (completely free, no credit card required)
3. Click "API Keys" in sidebar
4. Create new API key
5. Add to `.env` file: `GROQ_API_KEY=your_key_here`

**Free Tier:** 14,400 requests per day

## 📖 Usage

### Generating a Blog Post

1. **Login** to your account
2. **Paste** a YouTube video URL
3. **Click** "Generate Blog"
4. **Wait** 1-2 minutes for processing
5. **View** transcription and generated blog
6. **Access** saved blogs from "My Blogs"

### Supported YouTube URLs

```
✅ https://www.youtube.com/watch?v=VIDEO_ID
✅ https://youtu.be/VIDEO_ID
⚠️  https://www.youtube.com/shorts/VIDEO_ID (may be unreliable)
```

**Tip:** Regular YouTube videos work best. Shorts may have audio extraction issues.

## 📁 Project Structure

```
ai-blog-generator/
├── ai_blog_app/
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL config
│   └── wsgi.py
├── blog_generator/
│   ├── views.py             # Main logic
│   ├── models.py            # Database models
│   ├── urls.py              # App URLs
│   └── templates/
│       ├── index.html       # Home page
│       ├── all-blogs.html   # Blog list
│       ├── blog-details.html
│       ├── login.html
│       └── signup.html
├── media/
│   └── audio_files/         # Temporary audio storage
├── .env                     # Environment variables (create this)
├── requirements.txt         # Python dependencies
├── manage.py
└── README.md
```

## 🎨 Features in Detail

### User Authentication
- Secure registration and login
- Password validation
- Session management
- User-specific blog storage

### Blog Generation Pipeline
1. **Audio Extraction** - yt-dlp downloads YouTube audio
2. **Transcription** - AssemblyAI converts speech to text
3. **AI Generation** - Groq's Llama 3.3 creates blog post
4. **Storage** - Save to PostgreSQL database
5. **Display** - Render with markdown formatting

### Blog Management
- View all your generated blogs
- Search and filter (coming soon)
- Edit and delete (coming soon)
- Export to markdown (coming soon)

## ⚙️ Configuration

### Database Options

**Development (SQLite):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Production (PostgreSQL):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
```

## 🐛 Troubleshooting

### "No transcript available"
- **Cause:** Audio extraction or transcription failed
- **Solution:** 
  - Check FFmpeg is installed: `ffmpeg -version`
  - Verify AssemblyAI API key in `.env`
  - Use regular YouTube videos (not Shorts)

### "Audio Download Error"
- **Cause:** FFmpeg not installed or yt-dlp issue
- **Solution:**
  - Install FFmpeg (see installation steps)
  - Update yt-dlp: `pip install --upgrade yt-dlp`

### "Groq API Error"
- **Cause:** Invalid API key or rate limit
- **Solution:**
  - Check Groq API key in `.env`
  - Verify free tier limits (14,400 requests/day)

### Blog Content Has No Spacing
- **Cause:** Missing CSS styles
- **Solution:** Ensure `marked.js` is loaded and styles are applied

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Sunnet Fusion**

- GitHub: [@sunnetfusion](https://github.com/sunnetfusion)
- Email: sunnetfusion@gmail.com

## 🙏 Acknowledgments

- [AssemblyAI](https://www.assemblyai.com/) for transcription API
- [Groq](https://groq.com/) for lightning-fast LLM inference
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube audio extraction
- [Tailwind CSS](https://tailwindcss.com/) for beautiful UI

## 📊 Project Stats

- **Lines of Code:** ~1,500
- **Average Processing Time:** 1-2 minutes per video
- **Supported Video Length:** 1-30 minutes (recommended)
- **Database:** PostgreSQL with Django ORM

## 🚧 Roadmap

- [ ] Add blog editing functionality
- [ ] Implement search and filtering
- [ ] Export blogs to PDF/Markdown
- [ ] Add multiple language support
- [ ] Batch processing of videos
- [ ] API endpoint for external integration
- [ ] Mobile app (React Native)

## ⭐ Star History

If you found this project helpful, please consider giving it a star!

---

Made with ❤️ by Sunnet Fusion
