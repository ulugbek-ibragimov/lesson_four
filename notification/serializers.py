from rest_framework import serializers

from apps.notification.models import UserFCMToken, Notification, NotificationUser


class FCMTokenSerializer(serializers.ModelSerializer):
    user = serializers.CurrentUserDefault()

    class Meta:
        model = UserFCMToken
        fields = ('token', 'user')
        # extra_kwargs = {
        #     'user': {'required': False}
        # }


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class NotificationUserSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer()

    class Meta:
        model = NotificationUser
        fields = ('id', 'is_read', 'created_time', 'sent_time')
