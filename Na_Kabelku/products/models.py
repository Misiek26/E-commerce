from django.db import models
from django.utils.text import slugify

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=75)
    price = models.DecimalField(max_digits=6, default=0.00, decimal_places=2)
    body = models.TextField(blank=True)
    slug = models.SlugField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(blank=True)
    #author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return self.title
    
    def save(self):
        if not self.id:
            self.slug = slugify(self.title)

        super(Product, self).save()
    
'''
class Attachment(DatetimeCreatedMixin, AuthorMixin):
    class AttachmentType(models.TextChoices):
        PHOTO = "Photo", _("Photo")
        VIDEO = "Video", _("Video")

    file = models.ImageField('Attachment', upload_to='attachments/')
    file_type = models.CharField('File type', choices=AttachmentType.choices, max_length=10)

    images = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Model that uses the image field')

    class Meta:
        verbose_name = 'Attachment'
        verbose_name_plural = 'Attachments'

'''