from django.urls import path
from .views import RegisterView, CustomLoginView, profile, ChangePasswordView
from .forms import LoginForm
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='users-register'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True,
                                           template_name='accounts/login.html',
                                           authentication_form=LoginForm),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view
         (template_name='accounts/logout.html'), name='logout'),
    path('profile/', profile, name='users-profile'),
    path('password-change/', ChangePasswordView.as_view(),
         name='password_change'),
]
