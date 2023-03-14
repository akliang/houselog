from django.urls import path
import houselog.views as hlv
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login', hlv.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', hlv.DashboardListView.as_view(), name='dashboard'),
    path('add',hlv.AddItemView.as_view(), name='add'),
    path('delete', hlv.DeleteItemView.as_view(), name='delete'),
    path('done', hlv.DoneItemView.as_view(), name='done'),
]