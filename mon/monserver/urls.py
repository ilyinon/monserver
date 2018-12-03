from django.conf.urls import url, include
from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from api.views import Overview, DC_view, Server_view, Service_view, LAB_view,\
    Version_view, ServersAll, ServicesAll, ServiceMoreDetail, Winnodes, NodeDetail
from api import apiviews
from django.conf import settings




router = routers.DefaultRouter()
#router.register(r'servers', views.ServerViewSet)
#router.register(r'services', views.ServiceViewSet)
#router.register(r'status', views.StatusRudView)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
#    url(r'^', include(router.urls)),
    path('winnodes/<str:node_name>/', NodeDetail.as_view(), name='winnode_detail'),
    path('', Overview.as_view(), name="overall"),
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('servers/', ServersAll.as_view(), name="servers_list"),
    path("servers/<str:server_name>/", Server_view.as_view()),
    path('services/', ServicesAll.as_view(), name="services_list"),
    path("service/<str:service_name>/", ServiceMoreDetail.as_view(), name="ServiceMoreDetail"),
    path("status/", apiviews.CreateStatus.as_view(), name="send_status"),
    path("status/<str:server>/<str:service>/", apiviews.GetServiceStatus.as_view(), name="get_status"),
    path("dc/<str:dc_name>/", DC_view.as_view()),
    path("<str:server_name>/<str:service_name>/", Service_view.as_view()),
    path("lab/<str:lab_name>", LAB_view.as_view()),
    path("versions/", Version_view.as_view(), name="versions"),
    path('winnodes/', Winnodes.as_view(), name="winnodes"),
    path("winstatus/", apiviews.CreateWinnodeStatus.as_view(), name="winsend_status"),


]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns