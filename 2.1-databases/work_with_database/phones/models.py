from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Phone(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    image = models.ImageField()
    release_date = models.TextField()
    lte_exists = models.TextField()
    slug = models.SlugField(max_length=50, db_index=True, null=True)

    def __str__(self):
        return f'{self.id}, {self.name}, {self.price}, ' \
               f'{self.release_date}, {self.lte_exists}, ' \
               f'{self.slug}'

    def get_absolute_url(self):
        return reverse('Phone_detail', kwargs={'slug': self.slug})  # new

    def save(self, *args, **kwargs):    # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
