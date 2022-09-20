from django.urls import path, include
from rest_framework.routers import DefaultRouter

from profiles.views import ProfileDetailViewSet
from .views import UsersViewSet

# from users.views import (
#     UserRegisterView,
#     UserLogInView,
#     UserLogOutView,
#     ProfileView,
#     UserChangeProfileView,
#     PasswordResetView,
#     PasswordResetDoneView,
#     PasswordResetConfirmView,
#     PasswordResetCompleteView
# )
#
# urlpatterns = [
#     path('registration/', UserRegisterView.as_view(), name='registration'),
#     path('login/', UserLogInView.as_view(), name='login'),
#     path('logout/', UserLogOutView.as_view(), name='logout'),
#     path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
#     path('profile/<int:pk>/change/', UserChangeProfileView.as_view(), name='change_profile'),
#
#     path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
#     path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
#     path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
# ]
router = DefaultRouter()
# router.register('registration/', UserRegistration, basename='create_user')
router.register(r'', UsersViewSet)
router.register(r'', ProfileDetailViewSet, basename='profile_detail')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/profile/', include('profiles.urls')),
]
