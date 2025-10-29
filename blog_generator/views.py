from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json, os, traceback
from pathlib import Path
import assemblyai as aai
from .models import BlogPost
from django.http import HttpResponse




def health_check(request):
    return HttpResponse("OK", status=200)


# ---------- MAIN PAGE ----------
@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')


# ---------- BLOG GENERATION ----------
@csrf_exempt
@login_required(login_url='login')
def generate_blog(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        yt_link = data.get('link')
        if not yt_link:
            return JsonResponse({'error': 'YouTube link not provided'}, status=400)

        # Validate YouTube URL
        if not ('youtube.com' in yt_link or 'youtu.be' in yt_link):
            return JsonResponse({'error': 'Provided link is not a valid YouTube URL'}, status=400)

        title = yt_title(yt_link)
        if not title:
            return JsonResponse({'error': 'Failed to fetch YouTube title'}, status=400)

        transcript = get_transcript(yt_link)
        if not transcript:
            return JsonResponse({'error': 'Could not retrieve transcript'}, status=500)

        blog_content = generate_blog_content(title, transcript)
        if not blog_content:
            return JsonResponse({'error': 'Failed to generate blog content'}, status=500)

        # ✅ Save blog post to database
        new_blog = BlogPost.objects.create(
            user=request.user,
            youtube_title=title,
            youtube_link=yt_link,
            generated_content=blog_content
        )

        # Return success response with all data
        return JsonResponse({
            'id': new_blog.id,
            'title': title,
            'transcript': transcript,  # ← ADD THIS LINE
            'content': blog_content
        })

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': 'Internal server error', 'detail': str(e)}, status=500)


# ---------- BLOG LIST ----------
@login_required(login_url='login')
def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request, "all-blogs.html", {"blog_articles": blog_articles})


# ---------- BLOG DETAILS ----------
@login_required(login_url='login')
def blog_details(request, pk):
    blog_article_detail = get_object_or_404(BlogPost, id=pk)
    
    # Check if user owns this blog
    if request.user == blog_article_detail.user:
        return render(request, "blog-details.html", {"blog_article_detail": blog_article_detail})
    else:
        return redirect('blog-list')


# ---------- YOUTUBE HELPERS ----------
def yt_title(link):
    """Extract YouTube video title using yt-dlp"""
    try:
        import yt_dlp
        ydl_opts = {'quiet': True, 'skip_download': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            return info.get('title')
    except Exception as e:
        print(f"YouTube Title Error: {e}")
        traceback.print_exc()
        return None


def download_audio(link):
    """Download audio from YouTube using yt-dlp"""
    try:
        import yt_dlp
        media_root = Path(settings.MEDIA_ROOT)
        audio_dir = media_root / 'audio_files'
        audio_dir.mkdir(parents=True, exist_ok=True)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(audio_dir / '%(id)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            video_id = info['id']
            mp3_file = audio_dir / f"{video_id}.mp3"
            if mp3_file.exists():
                print(f"Downloaded audio: {mp3_file}")
                return str(mp3_file)
            return None
    except Exception as e:
        print(f"Audio Download Error: {e}")
        traceback.print_exc()
        return None


# ---------- TRANSCRIPT ----------
def get_transcript(link):
    """Download audio and transcribe using AssemblyAI"""
    audio_file = download_audio(link)
    if not audio_file:
        print("get_transcript: audio_file is None")
        return None

    try:
        aai_key = os.getenv("ASSEMBLYAI_API_KEY") or getattr(settings, "ASSEMBLYAI_API_KEY", None)
        if not aai_key:
            raise RuntimeError("AssemblyAI API key not set")

        aai.settings.api_key = aai_key
        transcriber = aai.Transcriber()

        transcript = transcriber.transcribe(audio_file)

        if transcript.status == aai.TranscriptStatus.error:
            print(f"Transcription failed: {transcript.error}")
            return None

        print("✅ Transcription completed successfully")

        # Clean up audio file after successful transcription
        if os.path.exists(audio_file):
            os.remove(audio_file)
            print(f"Cleaned up audio file: {audio_file}")

        return transcript.text

    except Exception as e:
        print(f"Transcript Error: {e}")
        traceback.print_exc()
        return None


# ---------- GROQ BLOG GENERATION ----------
def generate_blog_content(title, transcript):
    """Generate blog content using Groq API"""
    try:
        from groq import Groq
        
        api_key = os.getenv("GROQ_API_KEY") or getattr(settings, "GROQ_API_KEY", None)
        if not api_key:
            raise RuntimeError("Groq API key not set. Get one at https://console.groq.com/")

        client = Groq(api_key=api_key)

        prompt = (
            f"Based on the following YouTube video transcript, write a comprehensive and engaging blog post.\n\n"
            f"Video Title: {title}\n\n"
            f"Transcript:\n{transcript}\n\n"
            "Please write a well-structured blog article with:\n"
            "- An engaging introduction\n"
            "- Clear sections with subheadings\n"
            "- A compelling conclusion\n"
            "- Professional tone (not like a transcript)\n"
            "Make it informative and easy to read."
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a professional blog writer who creates engaging, well-structured articles."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Groq Error: {e}")
        traceback.print_exc()
        return None


# ---------- AUTH ----------
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
        return render(request, 'login.html', {'error_message': 'Please fill all fields'})
    return render(request, 'login.html')


def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        repeatPassword = request.POST.get('repeatPassword', '')

        if password == repeatPassword:
            if User.objects.filter(username=username).exists():
                return render(request, 'signup.html', {'error_message': 'Username already taken'})
            if User.objects.filter(email=email).exists():
                return render(request, 'signup.html', {'error_message': 'Email already in use'})

            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'signup.html', {'error_message': 'Passwords do not match'})

    return render(request, 'signup.html')


def user_logout(request):
    logout(request)
    return redirect('login')