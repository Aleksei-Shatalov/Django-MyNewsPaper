from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.models import User
from django.core.signing import Signer
from .tasks import send_news_to_subscribers_task
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.core.cache import cache
signer = Signer()

class PostsList(ListView):
    model = Post
    ordering = 'created_at'
    #queryset = Post.objects.all().order_by('-created_at')
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10  # вот так мы можем указать количество записей на странице



class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

# Добавляем новое представление для создания товаров.
class PostSearch(ListView):
    model = Post
    ordering = 'created_at'
    # queryset = Post.objects.all().order_by('-created_at')
    template_name = 'news_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news_app.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def get_initial(self):
        initial = super().get_initial()
        if 'news' in self.request.path:
            initial['type'] = 'NW'  # Тип для новостей
        elif 'articles' in self.request.path:
            initial['type'] = 'AR'  # Тип для статей

        return initial

    def form_valid(self, form):
        post = form.save(commit=False)

        # Устанавливаем тип на основе пути
        if 'news' in self.request.path:
            post.type = 'NW'
        elif 'articles' in self.request.path:
            post.type = 'AR'
        else:
            raise ValueError("Unknown type in the request path.")  # Ошибка, если тип не определён
        author = Author.objects.get(user=self.request.user)
        today = now() - timedelta(days=1)
        posts_today = Post.objects.filter(author=author, created_at__gte=today).count()
        if posts_today >= 3:
            return HttpResponseForbidden("Вы не можете публиковать более 3 новостей в сутки.")
        form.instance.author = author

        category = form.cleaned_data['categories']
        post.save()
        post.categories.add(category)  # Добавляем одну категорию
        #send_news_to_subscribers(category, post.title, post.text, post_id=post.id)  # Отправляем письмо
        send_news_to_subscribers_task.delay(category.id, post.title, post.text, post.id)
        return super().form_valid(form)

# Добавляем представление для изменения товара.
class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news_app.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    # Представление удаляющее товар.
class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news_app.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('posts_list')

signer = Signer()

def subscribe(request):
    if request.method == "POST":
        category_id = request.POST.get("category_id")
        category = get_object_or_404(Category, id=category_id)

        if not Post.objects.filter(categories=category, type='NW').exists():
            return HttpResponse("Подписка доступна только для новостей.", status=400)

        if request.user.is_authenticated:
            category.subscribers.add(request.user)
        redirect_url = request.POST.get("redirect_url", reverse('post_list'))
        return redirect(redirect_url)

    return HttpResponse("Некорректный запрос", status=400)

def unsubscribe(request):
    category_id = request.GET.get('category_id')
    user_id = request.GET.get('user_id')
    token = request.GET.get('token')

    # Проверяем параметры
    if not category_id or not user_id or not token:
        return HttpResponse("Некорректная ссылка", status=400)

    try:
        data = signer.unsign(token)
        if data != f"{user_id}:{category_id}":
            return HttpResponse("Некорректный токен", status=400)
    except:
        return HttpResponse("Некорректный токен", status=400)

    category = get_object_or_404(Category, id=category_id)
    user = get_object_or_404(User, id=user_id)
    category.subscribers.remove(user)

    return HttpResponse("Вы успешно отписались от категории новостей.")
