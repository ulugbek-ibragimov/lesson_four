from django.db.models import QuerySet, Manager


class NotificationQuerySet(QuerySet):
    def update(self, **kwargs):
        from apps.notification.signals import bulk_update_signal
        updated_ids = self.values_list('id', flat=True)
        bulk_update_signal.send(sender=self.model, instance_ids=updated_ids, updated_fields=kwargs)

        return super(NotificationQuerySet, self).update(**kwargs)


class NotificationManager(Manager):
    def get_queryset(self):
        return NotificationQuerySet(self.model, using=self._db)
