from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf import settings

router = routers.DefaultRouter()
router.register(r'breeds', views.BreedViewSet)
router.register(r'cats', views.CatViewSet)

# Kết nối API bằng automatic URL routing
# Ngoài ra, bao gồm login URLs cho browsable API
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# Chỉ thêm debug toolbar URLs trong development
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns