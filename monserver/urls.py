from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from rest_framework import routers
from .api.views import Overview, DC_view
from .api import apiviews

router = routers.DefaultRouter()
#router.register(r'servers', views.ServerViewSet)
#router.register(r'services', views.ServiceViewSet)
#router.register(r'status', views.StatusRudView)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
#    url(r'^', include(router.urls)),
    path('', Overview.as_view()),
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('servers/', apiviews.ServerList.as_view(), name="servers_list"),
    path('servers/<int:pk>/', apiviews.ServerDetail.as_view(), name="servers_detail"),
    path('services/', apiviews.ServiceList.as_view(), name="service_list"),
    path('services/<int:pk>/', apiviews.ServiceDetail.as_view(), name="service_detail"),
    path("status/", apiviews.CreateStatus.as_view(), name="send_status"),
    path("status/<str:server>/<str:service>/", apiviews.GetServiceStatus.as_view(), name="get_status"),
    path("dc/<str:dc_name>/", DC_view.as_view()),
]
