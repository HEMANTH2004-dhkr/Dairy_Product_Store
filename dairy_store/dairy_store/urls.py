from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Your main app
    path('cart/', include('cart.urls')),  # Cart app
    path('accounts/', include('django.contrib.auth.urls')),  # ✅ Login/Logout URLs
    path('orders/', include('orders.urls')),  # Orders app
    path('signup/', include('core.urls')),  # ✅ Signup URL
    path('accounts/signup/', include('core.urls')),  # ✅ Signup URL
    path('accounts/profile/', include('core.urls')),  # ✅ Profile URL
]





# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)