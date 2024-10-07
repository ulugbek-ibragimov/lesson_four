from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from apps.notification.managers import NotificationManager


class Notification(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    message = models.TextField("Message")
    is_for_everyone = models.BooleanField(_("Is for everyone"), default=False)
    users = models.ManyToManyField(User, verbose_name=_("Users"), blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    objects = NotificationManager()

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self):
        return self.title


class NotificationUser(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    is_sent = models.BooleanField(_("Is sent"), default=False)
    is_read = models.BooleanField(_("Is read"), default=False)
    sent_time = models.DateTimeField(_("Sent time"), null=True, blank=True)
    created_time = models.DateTimeField(_("Created time"), auto_now_add=True)
    notification = models.ForeignKey(Notification, on_delete=models.PROTECT, related_name='notification_users',
                                     verbose_name=_("Notification"))

    class Meta:
        verbose_name = _("NotificationUser")
        verbose_name_plural = _("NotificationUsers")

    def __str__(self):
        return f'{self.user.username} - {self.is_read}'


class UserFCMToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    token = models.CharField(_("Token"), max_length=512, unique=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("UserFCMToken")
        verbose_name_plural = _("UserFCMTokens")

    def __str__(self):
        return f'{self.created_at.timestamp()}'
