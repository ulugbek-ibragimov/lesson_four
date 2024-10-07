from django.urls import path

from apps.notification.views import RegisterFcmToken, NotificationUserList, NotificationUserDetail, \
    UserNotificationExist

app_name = 'notification'

urlpatterns = [
    path("RegisterFcmToken/", RegisterFcmToken.as_view(), name="register-fcm-token"),
    path("UserNotification/", NotificationUserList.as_view(), name="user-notification-list"),
    path("UserNotification/<int:pk>/", NotificationUserDetail.as_view(), name="user-notification-detail"),
    path("UserNotificationExist/", UserNotificationExist.as_view(), name="user-notification-exist")
]
