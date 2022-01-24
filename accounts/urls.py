from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views
from .views import MyTokenObtainPairView

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('join/', views.join, name='join'),
    path('logout/', views.logout, name='logout'),
    path('find_username/', views.find_username, name='find_username'),
    path('signin/kakao/', views.kakao_login, name="kakao_signin"),
    path('signin/kakao/callback/', views.kakao_login_callback, name="kakao_signin_callback"),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/access_token/', TokenRefreshView.as_view(), name='token_refresh_access_token'),
    path('api/token/refresh/refresh_token/', views.ApiRefreshRefreshTokenView.as_view(),
         name='token_refresh_refresh_token'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
