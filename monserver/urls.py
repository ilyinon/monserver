from django.conf.urls import url, include
from rest_framework import routers
from monserver.api import views

router = routers.DefaultRouter()
router.register(r'servers', views.ServerViewSet)
router.register(r'services', views.ServiceViewSet)
#router.register(r'status', views.StatusRudView)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
