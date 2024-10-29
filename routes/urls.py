# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import upload_pdf
from . import views

urlpatterns = [
    path('', upload_pdf, name='upload_pdf'),
    path('delete_document/<int:document_id>/', views.delete_document, name='delete_document'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
