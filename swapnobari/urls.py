
from django.contrib import admin
from django.urls import path, include
from swapnobari.views import root_views
from django.conf.urls.static import static
from django.conf import settings

from django.urls import include, path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Swapno Bari Housing Ltd. API",
        default_version="v1",
        description=(
            "Swapno Bari Housing Ltd.-এর Website ও Custom Admin Dashboard-এর জন্য "
            "একটি RESTful API। এই API-এর মাধ্যমে Project, Plot, Customer, "
            "Content এবং অন্যান্য প্রয়োজনীয় তথ্য পরিচালনা করা যাবে। "
            "Admin Dashboard থেকে সকল Content Create, Read, Update ও Delete (CRUD) "
            "করা যাবে এবং Website Visitors শুধুমাত্র প্রকাশিত তথ্য দেখতে পারবেন।"
        ),
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(
            name="Swapno Bari Housing Ltd.",
            email="contact@swapnobarihousing.com",
        ),
        license=openapi.License(
            name="Swapno Bari Housing Ltd."
        ),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_views),
    
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/", include("api.urls"), name="api-root"),
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)