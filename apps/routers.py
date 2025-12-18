
from django.urls import path, include


urlpatterns = [

    path("users/", include("apps.users.urls")),
    path("listings/", include("apps.listings.urls")),


]
