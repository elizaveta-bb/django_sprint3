from django.shortcuts import render, get_object_or_404

from .models import Post, Category

# Константы
POSTS_ON_INDEX_PAGE = 5


def index(request):
    """Главная страница проекта."""
    posts = Post.objects.displayed()[:POSTS_ON_INDEX_PAGE]
    return render(request, 'blog/index.html', {
        'posts': posts,
    })


def post_detail(request, post_id):
    """Страница отдельной публикации."""
    post = get_object_or_404(
        Post.objects.displayed(),
        pk=post_id
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    """Страница категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = category.posts.displayed()

    return render(request, 'blog/category.html', {
        'category': category,
        'post_list': posts
    })
