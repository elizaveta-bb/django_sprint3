from django.contrib import admin

from django.utils.translation import gettext_lazy as _

from .models import Post, Category, Location


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (_('Основное'), {'fields': ('title', 'description', 'slug')}),
        (_('Публикация'), {'fields': ('is_published',)}),
                )

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('title')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'is_published':
            field.help_text = _('Снимите галочку, чтобы скрыть категорию.')
        if db_field.name == 'slug':
            field.help_text = _('Идентификатор страницы для URL; разрешены \
                символы латиницы, цифры, дефис и подчёркивание.')

        return field


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')

    class Meta:
        verbose_name = _('Местоположение')
        verbose_name_plural = _('Местоположения')

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('name')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'name':
            field.label = _('Название места')
        if db_field.name == 'is_published':
            field.help_text = _('Снимите галочку, /
                                'чтобы скрыть местоположение.')
        return field


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'pub_date', 'is_published')
    list_filter = ('author', 'category', 'location', 'is_published')
    search_fields = ('title', 'text')
    date_hierarchy = 'pub_date'
    fieldsets = (
        (_('Основное'), {'fields': ('title', 'text',
                                    'author', 'category', 'location')}),
        (_('Публикация'), {'fields': ('pub_date', 'is_published')}),
    )

    class Meta:
        verbose_name = _('Публикация')
        verbose_name_plural = _('Публикации')

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-pub_date')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'is_published':
            field.help_text = _('Снимите галочку, чтобы скрыть публикацию.')
        if db_field.name == 'pub_date':
            field.help_text = _('Если установить дату и /
            'время в будущем — '
                                'можно делать отложенные публикации.')
        if db_field.name == 'category':
            field.label = _('Категория')
        if db_field.name == 'location':
            field.label = _('Местоположение')
        if db_field.name == 'author':
            field.label = _('Автор публикации')

        return field
