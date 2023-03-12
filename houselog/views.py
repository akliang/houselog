from django.shortcuts import render
from django.views.generic import ListView, View, TemplateView
from houselog.models import Houselog
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
import houselog.forms as h_forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginView(TemplateView):
     template_name = 'houselog/login.html'

     def post(self, request, *args, **kwargs):
          user = authenticate(
               username=request.POST.get('username'),
               password=request.POST.get('password')
          )
          if user is not None:
               login(request, user)
               return redirect('dashboard')
          else:
               print("Login failed")
               return redirect('login')

class DashboardListView(LoginRequiredMixin, ListView):
    #  queryset = Houselog.objects.all()
     context_object_name = 'houselog_items'
     template_name = 'houselog/dashboard.html'

     def get_queryset(self):
          self.user = get_object_or_404(User, id=1)
          return Houselog.objects.filter(user=self.user)
     
     def get_context_data(self, **kwargs):
          add_form = h_forms.AddItemForm()
          context = {
               'add_form': add_form,
          }
          kwargs.update(context)
          return super().get_context_data(**kwargs)

class AddItemView(LoginRequiredMixin, View):
     def post(self, request, *args, **kwargs):
          form = h_forms.AddItemForm(request.POST)
          if form.is_valid():
               form.save()
               return redirect('dashboard')
          else:
               # TODO
               pass

class DeleteItemView(LoginRequiredMixin, View):  
     def post(self, request, *args, **kwargs):
          id = request.GET.get('id', None)
          if id:
               entry = Houselog.objects.get(id=id)
               entry.delete()
               return redirect('dashboard')
          else:
               # TODO
               pass

