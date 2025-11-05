from django.db import models

class Image(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image_file = models.ImageField(upload_to='gallery/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-uploaded_at']
    