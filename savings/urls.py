from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    PaymentViewSet,
    CashoutViewSet,
    DashboardSummaryView,
)

router = DefaultRouter()
router.register("payments", PaymentViewSet, basename="payments")
router.register("cashouts", CashoutViewSet, basename="cashouts")

urlpatterns = router.urls + [
    path("summary/", DashboardSummaryView.as_view()),
]