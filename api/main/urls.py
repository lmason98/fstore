from django.urls import path

from .views import FolderView, FileView


urlpatterns = [
	path('folder/', FolderView.as_view(), name='folder'),
	path('folder/<int:id>/', FolderView.as_view(), name='folder'),

	path('file/', FileView.as_view(), name='file'),
	path('file/<int:id>/', FileView.as_view(), name='file'),
]