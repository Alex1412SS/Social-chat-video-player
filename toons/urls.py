from django.contrib import admin
from django.urls import path, include
from .views import index, toons_detail, toons_series, get_streaming_video, category_detail, like, favorite, review, like_review, review_update,review_delete

app_name = 'toons'

urlpatterns = [
    path('', index, name='index'),
    path('<slug:slug>/', toons_detail, name='toons_detail'),
    path('series/<int:pk>/', toons_series, name='toonseries_detail'),
    path('category/<slug:slug>/', category_detail, name='category_detail'),
    path('toonserie/<int:pk>/', get_streaming_video, name='toonseries_detaisl'),
    path('like/<slug:slug>/', like, name='like'),
    path('favorite/<slug:slug>/', favorite, name='favorite'),
    path('review/<slug:slug>/', review, name='review'),
    path('review_likes/<int:review_id>/', like_review, name='review_like'),
    path('review_update/<int:review_id>/', review_update, name='review_update'),
    path('review_delete/<int:review_id>/', review_delete, name='review_delete'),



]
