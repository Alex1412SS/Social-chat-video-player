from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .services import open_file
from django.http import StreamingHttpResponse
from .models import toons_model, category, toon_series, genre, Review, authors, Review_review
from .filters import BookFilter
from account.models import chat_messages, notification, Profile
from subscribe_payment.models import lvl_subscribe

User = get_user_model()
from .forms import ReviewForm, UpdateReview


def index2(request):
    return render(request, 'shablon/base_index.html')

@login_required(login_url='account:login')
def review(request, slug):
    toon = get_object_or_404(toons_model, slug=slug)
    if request.method == 'POST':
        form = ReviewForm(request.POST, user=request.user)
        if form.is_valid():
            review = form.save(commit=False)
            review.toon = toon
            review.save()
            toon.reviews.add(review)
            return redirect('toons:index')
    else:
        form = ReviewForm(user=request.user)
    return render(request, 'toons/review.html', {'form': form, 'toon': toon})


def index(request):
    messages = chat_messages.objects.all()
    f = BookFilter(request.GET, queryset=toons_model.objects.all())
    genres = genre.objects.all()
    categorys = category.objects.all()
    notifications = notification.objects.filter(for_user=request.user)

    if 'reset' in request.GET:
        f = BookFilter(queryset=toons_model.objects.all())
        toons = f.qs  # Обновление toons при сбросе фильтрации
    else:
        toons = f.qs

    return render(request, 'shablon/base_index.html', {'filter': f, 'genres': genres, 'toons': toons, 'categorys': categorys, 'messages': messages, "notifications": notifications})



def category_detail(request, slug):
    f = BookFilter(request.GET, queryset=toons_model.objects.all())
    genres = genre.objects.all()
    authorss = authors.objects.all()
    categories = category.objects.get(slug=slug)
    if 'reset' in request.GET:
        f = BookFilter(queryset=toons_model.objects.all())
        toons = f.qs.filter(category=categories)  # Обновление toons при сбросе фильтрации
    else:
        toons = f.qs.filter(category=categories)

    return render(request, 'toons/category_detail.html', {'categories': categories, 'toons': toons, 'genres': genres, 'filter': f, 'authors': authorss})
def toons_detail(request, slug):
    toon = toons_model.objects.all().get(slug=slug)
    profile = request.user.profile.sub

    if request.user.is_authenticated:
        toon.visit()
        if toon.subing == profile or toon.subing == None:
            try:
                toon_ser = toon_series.objects.get(toon=toon, is_published=True)
            except toon_series.DoesNotExist:
                return render(request, 'toons/404.html')
            return render(request, 'toons/toon_detail.html', {'toon': toon, 'toon_ser': toon_ser,})
        else:
            return render(request, 'toons/404.html')
    else:
        return redirect('account:login')
def like_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    profile = request.user.profile
    if request.user in review.likes.all():
        # User has already liked the review, remove the like
        profile.likes_reviews.remove(review)
        review.like(request.user)  # Implement the method to remove the like
        request.user.review_likes.remove(review)

    else:
        # User has not liked the review, add the like
        review.like(request.user)  # Implement the method to add the like
        request.user.review_likes.add(review)
        profile.likes_reviews.add(review)
    return redirect('toons:index')  # Redirect to a specific page after liking the review

def review_update(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    if request.method == 'POST':
      form = UpdateReview(request.POST, instance=review)
      if form.is_valid():
        form.save()
        return redirect('toons:index')
    else:
      form = UpdateReview(instance=review, user=request.user)
    return render(request, 'toons/review_update.html', {'form': form, 'review': review})

def review_delete(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()
    return redirect('toons:index')
def toons_series(request, pk):
    toon_ser = toon_series.objects.get(pk=pk)

    return render(request, 'toons/toon_series.html', {'toon_ser': toon_ser})

def get_streaming_video(request, pk: int):
    video, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(video, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response
def like(request, slug):
    toon = get_object_or_404(toons_model, slug=slug)
    if request.user in toon.likes.all():
        toon.like(request.user)
        request.user.toon_likes.remove(toon)  # Добавить toon в лайки пользователя
    else:
        toon.like(request.user)
        request.user.toon_likes.add(toon)  # Добавить toon в лайки пользователя
    return redirect('toons:index')


def favorite(request, slug):
    toon = get_object_or_404(toons_model, slug=slug)

    # Assuming profile is related to User through a OneToOneField named 'profile'
    profile = request.user.profile

    if request.user in toon.favourites.all():
        toon.unfavourite(request.user)
        request.user.favourites.remove(toon)  # Remove the toon from the user's favorites
        profile.favorites.remove(toon)  # Remove the toon from the user's profile favorites
    else:
        toon.favourite(request.user)
        request.user.favourites.add(toon)  # Add the toon to the user's favorites
        profile.favorites.add(toon)  # Add the toon to the user's profile favorites

    return redirect('toons:index')

def like(request, slug):
    toon = get_object_or_404(toons_model, slug=slug)

    # Assuming profile is related to User through a OneToOneField named 'profile'
    profile = request.user.profile

    if request.user in toon.favourites.all():
        toon.unlike(request.user)
        request.user.toon_likes.remove(toon)  # Remove the toon from the user's favorites
        profile.likes_for.remove(toon)  # Remove the toon from the user's profile favorites
    else:
        toon.like(request.user)
        request.user.toon_likes.add(toon)  # Add the toon to the user's favorites
        profile.likes_for.add(toon)  # Add the toon to the user's profile favorites

    return redirect('toons:index')