from datetime import datetime

from django.shortcuts import render, get_object_or_404

from .models import Post, Category


def index(request):
    """Главная страница проекта."""
    now = datetime.now()
    posts = Post.objects.filter(
        pub_date__lte=now,
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]

    return render(request, 'blog/index.html', {
        'posts': posts,

    })


def post_detail(request, post_id):
    """Страница отдельной публикации."""
    now = datetime.now()
    post = get_object_or_404(
        Post,
        pk=post_id,
        is_published=True,
        pub_date__lte=now,
        category__is_published=True
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    """Страница категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    now = datetime.now()
    
    posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=now
    ).order_by('-pub_date')
    return render(request, 'blog/category.html', {
        'category': category,
        'post_list': posts
    })
