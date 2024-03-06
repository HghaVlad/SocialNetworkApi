from django.http import HttpResponse, Http404, JsonResponse
from rest_framework.generics import RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, \
    ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, ValidationError, \
    NotAuthenticated, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.exceptions import InvalidToken

from users.models import User, Country, Follow, Post
from .serializers import UserSerializer, CountrySerializer, FriendListSerializer, \
    PostSerializer, LoginSerializer
from .permissions import IsTokenAvailable, MyToken
from .exceptions import UniqueError

# Create your views here.


def ping_view(request):

    return HttpResponse("ok")


class CountryList(ListAPIView):
    queryset = Country.objects.all().order_by("alpha2")
    serializer_class = CountrySerializer

    def get_queryset(self):
        region_list = self.request.GET.getlist("region")
        print(region_list)
        if not region_list or region_list[0] == "":
            return super().get_queryset()
        for region in region_list:
            if not Country.objects.filter(region=region).exists():
                raise ParseError("Region is not found")

        return Country.objects.filter(region__in=region_list).all()

    def handle_exception(self, exc):
        return Response({"reason": str(exc)}, 400)


class CountryOne(RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = "alpha2"

    def handle_exception(self, exc):
        if isinstance(exc, (NotFound, Http404)):
            return Response({"reason": "The alpha2 is not exist."}, status=404)

        return Response({"reason": str(exc)}, 400)

    def get_object(self):
        try:
            return Country.objects.get(alpha2__iexact=self.kwargs[self.lookup_field])
        except ObjectDoesNotExist:
            raise NotFound


class UserProfile(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response({"profile": serializer.data}, status=201, headers=headers)

    def handle_exception(self, exc):
        if isinstance(exc, UniqueError):
            return Response({"reason": str(exc)}, 409)

        return Response({"reason": str(exc)}, 400)


class SignIn(APIView):
    serializer = LoginSerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer(data=self.request.data)

        if serializer.is_valid():
            user = self.get_object(data=serializer.validated_data)
            if user:
                token = MyToken.for_user(user)
                return Response({"token": str(token)}, status=200)

        return Response({"reason": "User with the specified login and password was not found."}, status=401)

    @staticmethod
    def get_object(data):
        user = User.objects.filter(login=data['login']).first()
        if user is not None:
            if user.check_password(data['password']):
                return user

    def handle_exception(self, exc):
        if isinstance(exc, UniqueError):
            return Response({"reason": str(exc)}, 409)

        return Response({"reason": str(exc)}, 400)


class MyProfile(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsTokenAvailable)

    def get_object(self):
        return self.request.user

    def handle_exception(self, exc):
        if isinstance(exc, UniqueError):
            return Response({"reason": str(exc)}, 409)
        if isinstance(exc, (InvalidToken, NotAuthenticated, AuthenticationFailed)):
            return Response({"reason": "The token is invalid or not exist"}, 401)

        return Response({"reason": str(exc)}, 400)

    def update(self, request, *args, **kwargs):

        if len(set(request.data.keys()) - set(UserSerializer.editable_fields)) > 0:
            raise ValidationError("You can edit only 'countryCode', 'isPublic', 'phone', 'image'")
        partial = kwargs.pop('partial', False)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class Profiles(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsTokenAvailable)
    lookup_field = "login"

    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return Response({"reason": "The user with this login is not found"}, status=403)
        if isinstance(exc, UniqueError):
            return Response({"reason": str(exc)}, 409)
        if isinstance(exc, (InvalidToken, NotAuthenticated, AuthenticationFailed)):
            return Response({"reason": "The token is invalid or not exist"}, 401)

        return Response({"reason": str(exc)}, 400)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.isPublic is True or request.user.login == instance.login or \
                Follow.objects.filter(follower=instance, following_user=self.request.user).exists():
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        return Response({"reason": "The user public status is false"}, status=403)


class UpdatePassword(APIView):
    permission_classes = (IsAuthenticated, IsTokenAvailable)

    def post(self, *args, **kwargs):
        old_password = self.request.data.get('oldPassword')
        new_password = self.request.data.get('newPassword')

        if old_password is None or new_password is None:
            return Response({"reason": "Please specify the oldPassword, newPassword"}, status=400)

        if self.request.user.check_password(old_password):
            if self.request.user.set_password(new_password):
                return Response({"status": "ok"})

            return Response({"reason": "New password is too easy"}, status=400)

        return Response({"reason": "Old password is incorrect"}, status=403)

    def handle_exception(self, exc):
        if isinstance(exc, (NotFound, Http404)):
            return Response({"reason": str(exc)}, 404)
        if isinstance(exc, UniqueError):
            return Response({"reason": str(exc)}, 409)
        if isinstance(exc, (InvalidToken, NotAuthenticated, AuthenticationFailed)):
            return Response({"reason": "The token is invalid or not exist"}, 401)

        return Response({"reason": str(exc)}, 400)


class AddFriend(APIView):
    permission_classes = (IsAuthenticated, IsTokenAvailable)

    def post(self, *args, **kwargs):
        friend = self.get_friend()
        self.request.user.add_friend(friend)
        return Response({"status": "ok"}, status=200)

    def get_friend(self):
        login = self.request.data.get("login")
        if login is None:
            raise ParseError(detail="Please specify login")

        friend = User.objects.filter(login=login).first()
        if friend is None:
            raise NotFound(detail="User with this login is not found")
        return friend

    def handle_exception(self, exc):
        if isinstance(exc, (NotFound, Http404)):
            return Response({"reason": str(exc)}, 404)
        if isinstance(exc, UniqueError):
            return Response({"reason": str(exc)}, 409)
        if isinstance(exc, (InvalidToken, NotAuthenticated, AuthenticationFailed)):
            return Response({"reason": "The token is invalid or not exist"}, 401)

        return Response({"reason": str(exc)}, 400)


class RemoveFriend(AddFriend):

    def post(self, *args, **kwargs):
        friend = self.get_friend()
        if friend:
            self.request.user.remove_friend(friend)
        return Response({"status": "ok"}, status=200)

    def get_friend(self):
        login = self.request.data.get("login")
        if login is None:
            raise ParseError(detail={"reason": "Please specify login"})

        friend = User.objects.filter(login=login).first()
        if friend is None:
            return False
        return friend


class FriendList(ListAPIView):
    permission_classes = (IsAuthenticated, IsTokenAvailable)
    serializer_class = FriendListSerializer

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user).all().order_by("-addedAt")

    def filter_queryset(self, queryset):
        params = self.request.query_params
        limit = params.get("limit", 5)
        offset = params.get("offset", 0)
        if int(limit) > 50 or int(limit) < 0 or int(offset) < 0:
            raise ValidationError("Limit and offset must be in range of [0; 50]")

        return queryset[int(offset):int(offset)+int(limit)]

    def handle_exception(self, exc):
        if isinstance(exc, UniqueError):
            return Response({"reason": str(exc)}, 409)
        if isinstance(exc, (InvalidToken, NotAuthenticated, AuthenticationFailed)):
            return Response({"reason": "The token is invalid or not exist"}, 401)

        return Response({"reason": str(exc)}, 400)


class PostCreate(CreateAPIView):
    permission_classes = (IsAuthenticated, IsTokenAvailable)
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if len(set(request.data.keys()) - set(PostSerializer.creatable_frields)) > 0 \
                or len(request.data.keys()) != 2:
            raise ValidationError("There more fields than is needed")

        data['author'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=200, headers=headers)

    def handle_exception(self, exc):
        if isinstance(exc, UniqueError):
            return Response({"reason": str(exc)}, 409)
        if isinstance(exc, (InvalidToken, NotAuthenticated, AuthenticationFailed)):
            return Response({"reason": "The token is invalid or not exist"}, 401)

        return Response({"reason": str(exc)}, 400)


class PostList(ListAPIView):
    permission_classes = (IsAuthenticated, IsTokenAvailable)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "login"

    def filter_queryset(self, queryset):
        params = self.request.query_params
        limit = params.get("limit", 5)
        offset = params.get("offset", 0)
        if int(limit) > 50 or int(limit) < 0 or int(offset) < 0:
            raise ValidationError("Limit and offset must be in range of [0; 50]")
        return queryset[int(offset):int(offset) + int(limit)]

    def list(self, request, login=None, *args, **kwargs):
        if login == 'my':
            user = request.user
        else:
            user = User.objects.filter(login=login).first()
            if user is None:
                return Response({"reason": "User is not found"}, status=404)
            if user.isPublic is False and not user == request.user and not \
                    Follow.objects.filter(follower=user, following_user=self.request.user).exists():
                return Response({"reason": "You have not access"}, status=404)

        queryset = self.filter_queryset(Post.objects.filter(author=user).all().order_by("-createdAt"))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def handle_exception(self, exc):
        if isinstance(exc, UniqueError):
            return Response({"reason": str(exc)}, 409)
        if isinstance(exc, (InvalidToken, NotAuthenticated, AuthenticationFailed)):
            return Response({"reason": "The token is invalid or not exist"}, 401)

        return Response({"reason": str(exc)}, 400)


class PostOne(RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsTokenAvailable)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id"

    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return Response({"reason": "The post is not exist or not found."}, status=404)
        if isinstance(exc, UniqueError):
            return Response({"reason": str(exc)}, 409)
        if isinstance(exc, (InvalidToken, NotAuthenticated, AuthenticationFailed)):
            return Response({"reason": "The token is invalid or not exist"}, 401)

        return Response({"reason": str(exc)}, 400)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.author
        if user.isPublic is False and not user == request.user and not \
                Follow.objects.filter(follower=user, following_user=self.request.user).exists():
            return Response({"reason": "You have no access"}, status=404)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PostLike(PostOne):
    def post(self, *args, **kwargs):
        instance = self.get_object()
        user = instance.author
        if user.isPublic is False and not user == self.request.user and not \
                Follow.objects.filter(follower=user, following_user=self.request.user).exists():
            return Response({"reason": "You have no access"}, status=404)

        instance.like(self.request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get(self, *args, **kwargs):
        return Response({"reason": "Method POST not allowed."}, 400)


class PostDislike(PostLike):
    def post(self, *args, **kwargs):
        instance = self.get_object()
        user = instance.author
        if user.isPublic is False and not user == self.request.user and not \
                Follow.objects.filter(follower=user, following_user=self.request.user).exists():
            return Response({"reason": "You have no access"}, status=404)

        instance.dislike(self.request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


def handler404_view(request, *args, **kwargs):
    return JsonResponse({"reason": "Sorry, page not found"}, status=404)
