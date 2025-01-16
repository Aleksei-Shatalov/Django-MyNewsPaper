from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostCreate, PostSearch, PostUpdate, PostDelete


urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit', PostUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
    #path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    #path('articles/<int:pk>/edit', PostUpdate.as_view(), name='article_update'),
    #path('articles/<int:pk>/delete', PostDelete.as_view(), name='article_delete'),
]