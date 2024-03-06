import re
from datetime import datetime
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from users.models import User, Country, Post
from .exceptions import UniqueError


class UserSerializer(serializers.ModelSerializer):
    editable_fields = ('countryCode', 'isPublic', 'phone', 'image')

    class Meta:
        model = User
        fields = ['login', 'email', 'password', 'countryCode', 'isPublic', 'phone', 'image']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        del ret['password']  # Не показываем пароль
        ret = dict(ret)
        for key in list(ret.keys()):  # Не показываем null значения
            if ret[key] is None:
                del ret[key]
        return ret

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if len(set(validated_data.keys()) - set(self.editable_fields)) > 0:
            raise serializers.ValidationError("You can edit only countryCode isPublic phone image")

        return super().update(instance, validated_data)

    # Валидация
    @staticmethod
    def validate_login(value):
        if not re.search(r"[a-zA-Z0-9-]+", value) or len(value) < 1:
            raise serializers.ValidationError("Not pattern")
        if User.objects.filter(login=value).exists():
            raise UniqueError()

        return value

    @staticmethod
    def validate_email(value):
        if len(value) < 1:
            raise serializers.ValidationError("Not pattern")
        if User.objects.filter(email=value).exists():
            raise UniqueError()

        return value

    @staticmethod
    def validate_countryCode(value):
        if not isinstance(value, str):
            return serializers.ValidationError("The countryCode is incorrect type.")
        if not Country.objects.filter(alpha2=value.upper()).exists():
            raise serializers.ValidationError("The CountryCode is not found.")

        return value.upper()

    @staticmethod
    def validate_password(value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must contain at least 6 characters.")

        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")

        return value

    @staticmethod
    def validate_phone(value):
        if re.match(r"\+\d+", value).end() != len(value) or len(value) < 1:
            raise serializers.ValidationError("Phone must have pattern +123456789.")
        if User.objects.filter(phone=value).exists():
            raise UniqueError()

        return value

    @staticmethod
    def validate_image(value):
        if len(value) < 1 or len(value) > 200:
            raise serializers.ValidationError("Image field size must be [1,200] ")

        return value


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name', 'alpha2', 'alpha3', 'region']


class FriendListSerializer(serializers.Serializer):
    login = serializers.CharField(max_length=50)
    addedAt = serializers.DateTimeField()

    def to_representation(self, instance):
        ret = {"login": instance.following_user.login, 'addedAt': instance.addedAt}
        return ret


class PostSerializer(serializers.ModelSerializer):
    creatable_frields = ("content", "tags")

    class Meta:
        model = Post
        fields = ("id", "content", "author", "tags", "createdAt", "likesCount", "dislikesCount")
        read_only_fields = ("id", "createdAt", "likesCount", "dislikesCount")

    def to_representation(self, instance):
        ret = {}
        for field in self.fields:
            ret[field] = getattr(instance, field)
            if field == 'author':
                ret[field] = ret[field].login
            elif field == "createdAt":
                ret[field] = datetime.strftime(ret[field], "%Y-%m-%dT%TZ")

        return ret


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
