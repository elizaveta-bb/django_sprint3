from django.db import models
from django.db.models import functions
from django.contrib.auth import get_user_model

from . import constants

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=constants.CATEGORY_TITLE_MAX_LENGTH,
                             verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        max_length=constants.CATEGORY_SLUG_MAX_LENGTH,
        unique=True, blank=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; \
разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Location(BaseModel):
    name = models.CharField(max_length=constants.LOCATION_NAME_MAX_LENGTH,
                            verbose_name='Название места')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'


class PostManager(models.Manager):
    def displayed(self):  # filters posts that can be displayed
        return self.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=functions.Now()
        )


class Post(BaseModel):
    title = models.CharField(max_length=constants.POST_TITLE_MAX_LENGTH,
                             verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — можно делать \
отложенные публикации.'
    )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор публикации')
    location = models.ForeignKey(Location,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True, verbose_name='Местоположение')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True, verbose_name='Категория',
                                 related_name='posts'
                                 )

    objects = PostManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']
