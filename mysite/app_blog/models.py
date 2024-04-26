from django.db import models
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    category = models.CharField("Категорія", max_length=250, help_text="Максимум 250 символів")
    slug = models.SlugField("Слаг")

    class Meta:
        verbose_name = "Категорія для публікації"
        verbose_name_plural = "Категорії для публікацій"

    def __str__(self):
        return self.category
    
class Article(models.Model):
    title = models.CharField("Заголовок", max_length=250, help_text="Максимум 250 сим.")
    description = models.TextField(blank=True, verbose_name="Опис")
    pub_date = models.DateTimeField(u'Дата публікації', default=timezone.now)
    slug = models.SlugField(u'Слаг', unique_for_date='pub_date')
    main_page = models.BooleanField(u'Головна', default=True, help_text=u'Показувати')
    category = models.ForeignKey(Category, related_name='articles', blank=True, null=True, verbose_name=u'Категорія', on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name = u'Статя'
        verbose_name_plural = u'Статті'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        try:
            url = url = reverse('news-detail', kwargs={'year': self.pub_date.strftime("%Y"), 'month': self.pub_date.strftime("%m"),'day': self.pub_date.strftime("%d"), 'slug': self.slug, })
        except:
            url = "/"
            return url
        
class ArticleImage(models.Model):
    article = models.ForeignKey(Article, verbose_name=u'Стаття', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField('Фото', upload_to='photos')
    title = models.CharField('Заголовок', max_length=250, help_text=u'Максимум 250 сим.', blank=True)

    class Meta:
        verbose_name = 'Фото для статті'
        verbose_name_plural = 'Фото для статті'

    def __str__(self):
        return self.title
    
    @property
    def filename(self):
        return self.image.name.rsplit('/', 1)[-1]
    
    
