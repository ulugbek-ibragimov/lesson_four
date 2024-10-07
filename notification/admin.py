from django.contrib import admin

from apps.notification.models import UserFCMToken, Notification, NotificationUser


# Register your models here.

@admin.register(UserFCMToken)
class UserFCMTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass


@admin.register(NotificationUser)
class NotificationUserAdmin(admin.ModelAdmin):
    pass
