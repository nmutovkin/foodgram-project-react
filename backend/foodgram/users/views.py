from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow
from .pagination import CustomPageNumberPagination
from .serializers import SubscribeSerializer


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPageNumberPagination

    def get_permissions(self):
        if self.action == 'subscribe' or self.action == 'subscriptions':
            self.permission_classes = [IsAuthenticated, ]
        return super().get_permissions()

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, id=None):
        author = self.get_object()
        user = request.user

        follow_object = Follow.objects.filter(
            user=user,
            author=author
        )

        if request.method == 'POST':
            serializer = SubscribeSerializer(
                author,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)

            if follow_object.exists():
                return Response(
                    {'errors': 'already subscribed'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if user != author:
                Follow.objects.get_or_create(user=user, author=author)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'errors': 'self subscription'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:  # DELETE

            if not follow_object.exists():
                return Response(
                    {'errors': 'not subscribed'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            follow_object.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def subscriptions(self, request):

        queryset = self.get_queryset()
        follows = Follow.objects.filter(user=request.user)
        followed_users = queryset.filter(following__in=follows)

        context = {'request': request}

        page = self.paginate_queryset(followed_users)
        if page is not None:
            serializer = SubscribeSerializer(page, many=True,
                                             context=context)
            return self.get_paginated_response(serializer.data)

        serializer = SubscribeSerializer(followed_users, many=True,
                                         context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)
