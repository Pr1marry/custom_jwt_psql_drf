from django.urls import path
from .views import RegisterAPIView, TokensAPIView, RefreshAPIAccessView, LogoutAPIView, RefreshApiAllView, LoginAPIView

urlpatterns = [
    # регистрация нового пользователя
    path('register', RegisterAPIView.as_view()),
    # получение всех токенов по заданному пользователю (id)
    path('tokens', TokensAPIView.as_view()),
    # входим под определенным пользователем и получаем токены
    path('login', LoginAPIView.as_view()),
    # обновление пары токенов по id пользователя
    path('refresh_all', RefreshApiAllView.as_view()),
    # обновление Access токена
    path('refresh_access', RefreshAPIAccessView.as_view()),
    # удаление рефреш токена из cookie файлов
    path('logout', LogoutAPIView.as_view())
]
