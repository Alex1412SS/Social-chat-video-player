from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('toons/', include('toons.urls', namespace='toons')),
    path('account/', include('account.urls', namespace='account')),
    path('subscription/', include('subscribe_payment.urls', namespace='subscribe_payment')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

