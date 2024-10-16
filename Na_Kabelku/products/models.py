from django.db import models
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(null=True, blank=True)
    banner = models.ImageField(blank=True)

    def __str__(self):
        return self.name
    
    def save(self):
        if not self.id:
            self.slug = slugify(self.name)

        super(Category, self).save()

class Brand(models.Model):
    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self):
        if not self.id:
            self.slug = slugify(self.name)

        super(Brand, self).save()

class Product(models.Model):
    title = models.CharField(max_length=75)
    price = models.DecimalField(max_digits=6, default=0.00, decimal_places=2)
    body = models.TextField(blank=True)
    slug = models.SlugField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(blank=True)
    quantity = models.PositiveIntegerField(default=0)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', default="2")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', null=True)
    #author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return self.title
    
    def save(self):
        if not self.id:
            self.slug = slugify(self.title)

        super(Product, self).save()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Image for {self.product.title}"
    

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