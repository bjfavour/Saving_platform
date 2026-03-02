from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, CashoutViewSet

router = DefaultRouter()
router.register("payments", PaymentViewSet, basename="payments")
router.register("cashouts", CashoutViewSet, basename="cashouts")

urlpatterns = router.urls