from django.urls import path

from .views import PostUpdate, PostView

urlpatterns = [
    path('posts/<int:pk>/edit', PostUpdate.as_view(), name='post_edit'),
    path('posts/<int:pk>', PostView.as_view(), name='post_detail'),
]
