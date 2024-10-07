from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.notification.models import UserFCMToken, NotificationUser
from apps.notification.permissons import IsOwner
from apps.notification.serializers import FCMTokenSerializer, NotificationUserSerializer


# Create your views here.

class RegisterFcmToken(CreateAPIView):
    serializer_class = FCMTokenSerializer
    queryset = UserFCMToken.objects.all()
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class NotificationUserList(ListAPIView):
    serializer_class = NotificationUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NotificationUser.objects.filter(user=self.request.user)


class NotificationUserDetail(RetrieveAPIView):
    queryset = NotificationUser.objects.all()
    serializer_class = NotificationUserSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        obj.is_read = True
        obj.save(update_fields=['is_read'])

        return obj


class UserNotificationExist(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(
            {'notification_exist': NotificationUser.objects.filter(user=self.request.user, is_read=False).exists(),
             'notification_count': NotificationUser.objects.filter(user=self.request.user, is_read=False).count()})
