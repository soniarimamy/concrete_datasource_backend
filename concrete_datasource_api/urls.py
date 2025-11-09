from django.urls import path
from .views import RegisterView, LoginView, CreateApplicationView, ConfirmApplicationView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('create-application/', CreateApplicationView.as_view(), name='create_application'),
    path('confirm-application/<int:pk>/', ConfirmApplicationView.as_view(), name='confirm_application'),
]
