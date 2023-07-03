from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from register.views import *

router = DefaultRouter()
router.register('bemorlar', BemorModelViewSet)
router.register('tolovlar', TolovModelViewSet)
router.register('xulosalar', XulosaModelViewSet)
router.register('xonalar', XonaModelViewSet)
router.register('bosh_xonalar', BoshXonalarModelViewSet)
router.register('joylashtirishlar', JoylashtirishModelViewSet)
router.register('xulosa_shablonlar', XulosaShablonModelViewSet)
router.register('yollanmalar', YollanmaModelViewSet)
router.register('tolov_qaytarishlar', TolovQaytarishViewSet)


schema_view = get_schema_view(
   openapi.Info(
      title="Klinika API",
      default_version='v1',
      description="Odiljon Revmatolog klinikasi sotuv tizimi uchun yozilgan API",
      contact=openapi.Contact(email="1997abdulhamid@gmail.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
