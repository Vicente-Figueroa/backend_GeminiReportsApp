from django.urls import include, path
from rest_framework import routers
from django.contrib import admin

from csvReader.views import ImportCSVView
from api import urls as urls_api
from api_gemini import urls as urls_gemini

router = routers.DefaultRouter()
router.register(r'csv-file', ImportCSVView, basename='csv-view')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin', admin.site.urls, name="admin"),
    path('csv-file',ImportCSVView.as_view(), name="csv-file"),
    path('api/',include(urls_api)),
    path('gemini/',include(urls_gemini))
]
