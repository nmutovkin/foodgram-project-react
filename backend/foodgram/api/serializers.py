from djoser.serializers import UserSerializer, UserCreateSerializer


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name'
        )
        read_only_fields = ('id', )


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'password'
        )
        read_only_fields = ('id', )
