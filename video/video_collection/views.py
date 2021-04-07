from django.shortcuts import render, redirect, get_object_or_404
from .models import Video
from .forms import VideoForm, SearchForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.functions import Lower


def home(request):
    app_name = 'Tennis Videos'  # Defines the app name displayed on the home page of web app
    # Render the template with the app's name upon initial page load and anytime 'Home' link is clicked
    return render(request, 'video_collection/home.html', {'app_name': app_name}) 


def add(request):
    # If the request method is 'POST', try to add the new video
    if request.method == 'POST':
        new_video_form = VideoForm(request.POST) 
        if new_video_form.is_valid():
            try:
                new_video_form.save()
                return redirect('video_list') # If the video is added successfully, redirect to the list of videos
            except ValidationError:
                messages.warning(request, 'Invalid YouTube URL')
            except IntegrityError:
                messages.warning(request, 'You already added that video.')
        
        messages.warning(request, 'Check the data entered')
        return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})
    # If request method is not equal to 'POST' return a blank VideoForm
    new_video_form = VideoForm()
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})


def video_list(request):
    # Get current value of search form
    search_form = SearchForm(request.GET)

    # This code won't run if search_form is blank
    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term']
        # Search is case-insensitive and finds partial matches. Orders alphabetically by name.
        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name')) 
    else:
        # If the search form is blank, return a blank search form and all videos, ordered by name
        search_form = SearchForm()
        videos = Video.objects.order_by(Lower('name'))

    return render(request, 'video_collection/video_list.html', {'videos': videos, 'search_form': search_form})


def video_info(request, video_pk):
    # Retrive the requested video, or return 404 (not found) if the video doesn't exist
    video = get_object_or_404(Video, pk=video_pk)
    return render(request, 'video_collection/video_info.html', {'video': video})


def delete_video(request, video_pk):
    video = get_object_or_404(Video, pk=video_pk)
    video.delete()
    return redirect('video_list')