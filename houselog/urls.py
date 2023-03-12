from django.urls import path
from houselog.views import DashboardListView, AddItemView, DeleteItemView, LoginView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', DashboardListView.as_view(), name='dashboard'),
    path('add', AddItemView.as_view(), name='add'),
    path('delete', DeleteItemView.as_view(), name='delete'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]