from django.conf.urls import url, include, patterns
from rest_framework.urlpatterns import format_suffix_patterns
import TransitView

urlpatterns = [
    url(r'^$', TransitView.path_list),
    url(r'^inteltransit/', TransitView.writetojson),
    url(r'^transitjson/markers', TransitView.returnmarkersjson),
    url(r'^transitjson/routes', TransitView.returnroutesjson),
    url(r'^transitjson/crosses', TransitView.returncrossesjson),
]

urlpatterns = format_suffix_patterns(urlpatterns)