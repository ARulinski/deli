# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import upload_pdf

urlpatterns = [
    path('', upload_pdf, name='upload_pdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
