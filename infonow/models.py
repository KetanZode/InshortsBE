from django.db import models
import base64

# Create your models here.

class Article(models.Model):
    title       = models.CharField(max_length=124)
    src_link    = models.CharField(max_length=255, null=True, blank=True)
    uploaded_by = models.CharField(max_length=255, null=True, blank=True)
    active      = models.BooleanField(default=True, null=True, blank=True)
    content     = models.TextField(null=True, blank=True)
    image       = models.ImageField(upload_to='media/article', null=True, blank=True)
    image2      = models.TextField(null=True, blank=True)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    source      = models.ForeignKey('Source', on_delete=models.SET_NULL, related_name='articles', null=True)
    language    = models.ForeignKey('Language', on_delete=models.SET_NULL, related_name='articles', null=True)
    categorys   = models.ManyToManyField('Category', related_name='articles', blank=True)
    
    @property
    def image_b64(self):
        try:
            f = self.image.open()
            return f'data:image/png;base64,{base64.b64encode(f.read()).decode()}'
        except  : return None
    
    class Meta:
        db_table = 'info_articles'

class Source(models.Model):
    name        = models.CharField(max_length=255, null=True, blank=True, unique=True)
    main_link   = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = 'info_sources'

class Language(models.Model):
    name        = models.CharField(max_length=255, unique=True)
    class meta:
        db_table = 'info_languages'

class Category(models.Model):
    name        = models.CharField(max_length=255, unique=True)
    class meta:
        db_table = 'info_categories'
