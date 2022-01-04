from django.db.models import Exists, OuterRef
from djoser.views import UserViewSet
from recipes.models import Follow


class CustomUserViewSet(UserViewSet):
    def get_queryset(self):
        queryset = super().get_queryset()
        follows = Follow.objects.filter(
            user=self.request.user,
            author=OuterRef('id')
        )
        return queryset.annotate(is_subscribed=Exists(follows))
