from django.conf.urls import url
from django.urls import path
from .views import AuthRegister, AuthInfoGetView, AuthInfoUpdateView, AuthInfoDeleteView

urlpatterns = [
    path('register/', AuthRegister.as_view()),
    path('', AuthInfoGetView.as_view()),
    path('auth_update/', AuthInfoUpdateView.as_view()),
    path('delete/', AuthInfoDeleteView.as_view()),
]
