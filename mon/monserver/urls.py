from django.conf.urls import url, include
from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from api.views import Overview, DC_view, Server_view, Service_view, LAB_view, Version_view, ServersAll, ServicesAll
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
    path('', Overview.as_view()),
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('servers/', ServersAll.as_view(), name="servers_list"),
    path('servers/<int:pk>/', apiviews.ServerDetail.as_view(), name="servers_detail"),
    path('services/', ServicesAll.as_view(), name="service_list"),
    path('services/<int:pk>/', apiviews.ServiceDetail.as_view(), name="service_detail"),
    path("status/", apiviews.CreateStatus.as_view(), name="send_status"),
    path("status/<str:server>/<str:service>/", apiviews.GetServiceStatus.as_view(), name="get_status"),
    path("servers/<str:server_name>/", Server_view.as_view()),
    path("dc/<str:dc_name>/", DC_view.as_view()),
    path("<str:server_name>/<str:service_name>/", Service_view.as_view()),
    path("lab/<str:lab_name>", LAB_view.as_view()),
    path("versions/", Version_view.as_view()),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns