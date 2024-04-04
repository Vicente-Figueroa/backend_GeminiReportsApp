from django.urls import include, path
from rest_framework import routers
#from django.conf.urls import url
from django.contrib import admin

from api_gemini.views import MyView
from csvReader.views import ImportCSVView
from api import urls

router = routers.DefaultRouter()
router.register(r'gemini', MyView, basename='my-view')
router.register(r'csv-file', ImportCSVView, basename='csv-view')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('gemini', MyView.as_view(), name="gemini"),
    path('admin', admin.site.urls, name="admin"),
    path('csv-file',ImportCSVView.as_view(), name="csv-file"),
    path('api/',include(urls))
]
