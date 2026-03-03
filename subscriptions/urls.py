from django.urls import path
from .views import ActivateSubscriptionView

urlpatterns = [
    path("activate/", ActivateSubscriptionView.as_view(), name="activate-subscription"),
]