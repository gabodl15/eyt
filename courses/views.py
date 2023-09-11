from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from .models import Lista, Video
from pytube import YouTube, Playlist
import json, datetime


# Create your views here.

def index(request) -> render:
    # MOSTRAMOS LOS ULTIMOS 5 REGISTROS DE ALGUN CURSO / LISTA DE YOUTUBE
    courses = Lista.objects.order_by('-id')[:5]
    context = {
        'courses': courses
    }
    return render(request, 'courses/index.html', context)

def check(request) -> JsonResponse:
    # Verificamos que sea una lista de videos de Youtube.
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    url = body['url']
    playlist = Playlist(url)
    try:
        num_videos = playlist.length
        title = playlist.title
        owner = playlist.owner
        data = {
            'playlist': 'ok',
            'num_videos': num_videos,
            'title': title,
            'owner': owner,
            'csrf_token': get_token(request)
        }
        return JsonResponse(data)
    except Exception as e:
        data = {
            'playlist': 'error'
        }
        return JsonResponse(data)

def add(request) -> redirect:
    # GUARDAMOS LA LISTA Y LOS VIDEOS DE LA LISTA
    url = request.GET['url']
    playlist = Playlist(url)
    lista = Lista(
        name = playlist.title,
        num_videos = playlist.length
    )
    lista.save()
    videos = playlist.videos
    for i, video in enumerate(videos, start=1):
        time = datetime.timedelta(days = 0, seconds = video.length)
        _video = Video(
            lista = lista,
            name = video.title,
            url = video.embed_url,
            youtube_id = video.video_id,
            video_time = time,
            video_number = i
        )
        _video.save()
    return redirect('courses.index')

def list(request, id) -> render:
    # BUSCAMOS LA LISTA DE REPRODUCCION
    course = Lista.objects.get(id=id)
    context = {
        'course': course
    }
    return render(request, 'courses/list.html', context)

def video(request, id) -> render:
    # OBTENEMOS EL VIDEO QUE QUEREMOS VISUALIZAR Y LO ENVIAMOS A LA VISTA
    video = Video.objects.get(id=id)

    # DECLARAMOS LAS VARIABLES NULA, BUSCAMOS SI HAY UN SIGUIENTE VIDEO DE ESA LISTA Y VIDEO PREVIO
    next_video_id = None
    previus_video_id = None
    if video.video_number != video.lista.num_videos:
        next_video_id = Video.objects.filter(
            lista=video.lista,
            video_number=(video.video_number + 1)
        ).first().id
    if video.video_number != 1:
        previus_video_id = Video.objects.filter(
            lista=video.lista,
            video_number=(video.video_number - 1)
        ).first().id
    context = {
        'video': video,
        'next': next_video_id,
        'previus': previus_video_id
    }
    return render(request, 'courses/video.html', context)

def update_time_view(request, video_id, new_time) -> JsonResponse:
    # GUARDAMOS EL TIEMPO EN EL QUE EL VIDEO VA
    video = Video.objects.get(id=video_id)
    video.video_current_time = int(float(new_time))

    duration = video.video_time.total_seconds()
    if (video.video_current_time - duration) < 7:
        video.lista.current_video = video.video_number
        video.is_watched = True
    
    video.save()
    data = {
        'ok': 'ok'
    }
    return JsonResponse(data)
