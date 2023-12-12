from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # The 'admin/' path is used to access the Django admin interface.
    # This is a built-in feature of Django for site administration.
    path('admin/', admin.site.urls),

    # The '' (empty path) means the root of the site. This line includes the URLs from the 'store.urls'.
    # Essentially, it's saying: "For any path that comes into the website, refer to 'store.urls' for further instruction."
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]

# The following condition is checked only if the DEBUG setting is True.
# DEBUG should be set to True in development and False in production for security reasons.
if settings.DEBUG:
    # This adds URL patterns for serving static files in development.
    # In development, Django serves static files (like CSS, JavaScript) directly.
    # In production, however, these files should be served by a web server (like Nginx or Apache).
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # This adds URL patterns for serving media files in development.
    # Media files are user-uploaded files, like user profile pictures.
    # Like static files, these should also be served by the web server in production.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
