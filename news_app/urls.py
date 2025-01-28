from django.urls import path
from .views import PostsList, PostDetail, PostCreate, PostSearch, PostUpdate, PostDelete
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(PostsList.as_view()), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit', PostUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
    path('category/unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('category/subscribe/', views.subscribe, name='subscribe'),
]