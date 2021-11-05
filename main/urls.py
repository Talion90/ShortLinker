from django.urls import path

from main.views import home
from main.views import other_page
from main.views import SLLoginView
from main.views import profile
from main.views import SLLogoutView
from main.views import ChangeUserInfoView
from main.views import SLPasswordChangeView
from main.views import SLPasswordResetView, SLPasswordResetDoneView
from main.views import SLPasswordResetConfirmView, SLPasswordResetCompleteView
from main.views import RegisterUserView, RegisterDoneView
from main.views import user_activate
from main.views import DeleteUserView


app_name = 'main'
urlpatterns = [
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/login/', SLLoginView.as_view(), name='login'),
    path('accounts/logout/', SLLogoutView.as_view(), name='logout'),

    path('accounts/password/change/', SLPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_reset/', SLPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', SLPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/password_reset/<uidb64>/<token>', SLPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('accounts/password_reset/done/', SLPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('<str:page>/', other_page, name='other'),
    path('', home, name='index'),
]
