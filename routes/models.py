# models.py
from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='pdfs/')  # PDF file upload
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # To store the extracted total

    def __str__(self):
        return self.title
