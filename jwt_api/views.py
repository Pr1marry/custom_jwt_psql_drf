from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException, AuthenticationFailed

from .authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from .serializers import UserSerializer
from .models import User


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TokensAPIView(APIView):
    def post(self, request):
        user = User.objects.filter(id=request.data['id']).first()

        if not user:
            raise APIException('Несуществующий пользователь')

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        # сохранение в бд refresh_token:
        # user.refresh = refresh_token
        # user.save()

        response = Response()

        response.set_cookie(key='refreshToken', value=refresh_token, httponly=True)
        response.data = {
            'token': access_token,
            # 'r_token': refresh_token
        }

        return response


class LoginAPIView(APIView):
    def post(self, request):
        user = User.objects.filter(email=request.data['email']).first()

        if not user:
            raise APIException('Несуществующий пользователь')

        if not user.check_password(request.data['password']):
            raise APIException('Неправильный пароль')

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        # сохранение в бд refresh_token:
        # user.refresh = refresh_token
        # user.save()

        response = Response()

        response.set_cookie(key='refreshToken', value=refresh_token, httponly=True)
        response.data = {
            'token': access_token,
            # 'r_token': refresh_token
        }

        return response


class RefreshAPIAccessView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        access_token = create_access_token(id)
        return Response({
            'token': access_token
        })


class RefreshApiAllView(APIView):
    def post(self, request):
        user = User.objects.filter(id=request.data['id']).first()

        if not user:
            raise APIException('Несуществующий пользователь')

        refresh_token = create_refresh_token(user.id)
        access_token = create_access_token(user.id)

        # обновление refresh_token в бд:
        # user.refresh = refresh_token
        # user.save()

        response = Response()

        response.set_cookie(key='refreshToken', value=refresh_token, httponly=True)
        response.data = {
            'token': access_token,
        }

        return response


class LogoutAPIView(APIView):
    def post(self, _):
        response = Response()
        response.delete_cookie(key="refreshToken")
        response.data = {
            'message': 'success'
        }
        return response
