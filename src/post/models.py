# -*- coding:utf-8 -*-

"""
Нийтлэл
"""

from unidecode import unidecode

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.template.defaultfilters import slugify
from tinymce import HTMLField


class Category(models.Model):
    """
    Нийтлэл ангилал
    """
    name = models.CharField(verbose_name='Ангилал', max_length=32)

    class Meta:
        verbose_name = 'Ангилал'
        verbose_name_plural = 'Ангиллууд'
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Нийтлэл таг
    """
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name = 'Таг'
        verbose_name_plural = 'Тагууд'
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Нийтлэл
    """
    author = models.ForeignKey(
        User,
        verbose_name='Нийтлэгч',
        on_delete=models.CASCADE,
        related_name='posts'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Ангилал',
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(
        verbose_name='Гарчиг',
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        'Слаг',
        max_length=256,
        editable=False,
        unique=True
    )
    background_image = models.ImageField(verbose_name='Нүүр зураг')
    content = HTMLField(verbose_name='Агуулга')
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тагууд',
        related_name='posts',
        blank=True
    )
    is_published = models.BooleanField(default=True)
    is_active = models.BooleanField(verbose_name='Идэвхитэй', default=True)
    created_at = models.DateTimeField(
        verbose_name='Үүссэн огноо',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Зассан огноо',
        auto_now=True
    )

    class Meta:
        verbose_name = 'Нийтлэл'
        verbose_name_plural = 'Нийтлэлүүд'
        ordering = ['-updated_at', 'id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Нийтлэл
        """
        self.slug = slugify(unidecode(self.title))
        super(Post, self).save(*args, **kwargs)

    def get_is_published_html(self):
        """
        Нийтлэл
        """
        if self.is_published:
            return '<div class="badge badge-success">Нийтлэгдсэн</div>'
        return '<div class="badge badge-warning">Ноорог</div>'
    get_is_published_html.short_description = 'Төлөв'

    def get_category_name(self):
        """
        Нийтлэл
        """
        return self.category.name
    get_category_name.short_description = 'Ангилал'

    @property
    def get_update_url(self):
        """
        Нийтлэл
        """
        return 'employee-post-update'

    @property
    def get_delete_url(self):
        """
        Нийтлэл
        """
        return 'employee-post-update'

    def get_action(self):
        """
        Нийтлэл
        """
        return '''<div class = "dropdown">
              <button class = "btn btn-white btn-xs dropdown-toggle" type = "button"
                id = "dropdownMenuButton"
                data-toggle = "dropdown"
                aria-haspopup = "true"
                aria-expanded = "false" >
                <i data-feather = "settings"></i>
                Тохиргоо
              </button>
              <div class = "dropdown-menu"
                aria-labelledby = "dropdownMenuButton">
                <a class="dropdown-item" href="{0}">Засах</a>
                <a class="dropdown-item" href="javascript:;" data-toggle="deleteAlert" data-href="{1}">Устгах</a>
              </div>
            </div>'''.format(
            reverse_lazy('employee-post-update', kwargs={'pk': self.pk}),
            reverse_lazy('employee-post-delete', kwargs={'pk': self.pk})
        )
