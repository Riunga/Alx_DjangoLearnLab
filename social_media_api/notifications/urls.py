# notifications/urls.py
from django.urls import path
from .views import NotificationListView, MarkNotificationsReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications'),
    path('mark-read/', MarkNotificationsReadView.as_view(), name='mark-notifications-read'),
]
