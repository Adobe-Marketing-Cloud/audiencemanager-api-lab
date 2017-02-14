
from django.conf import settings
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^app/$', views.view_index, name='index'),
    url(r'^app/cart$', views.view_cart, name='cart'),
    url(r'^$', RedirectView.as_view(url='app/', permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
