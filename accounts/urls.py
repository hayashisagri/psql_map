from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.forms import EmailAuthenticationForm
from .views import SignupView

app_name = "accounts"

urlpatterns = [
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(
        form_class=EmailAuthenticationForm,
        redirect_authenticated_user=True,
        template_name='accounts/login.html'
    ), name='login')
]
