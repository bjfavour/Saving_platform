from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import CustomLoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/login/', CustomLoginView.as_view()),
    path('api/auth/refresh/', TokenRefreshView.as_view()),

    path('api/accounts/', include('accounts.urls')),
    path("api/savings/", include("savings.urls")),
    path("api/subscription/", include("subscriptions.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
