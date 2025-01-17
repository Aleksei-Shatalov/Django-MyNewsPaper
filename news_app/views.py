from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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

        post.save()
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

