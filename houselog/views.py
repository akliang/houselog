from django.shortcuts import render
from django.views.generic import ListView, View, TemplateView
from houselog.models import Houselog
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
import houselog.forms as h_forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date
import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from django.utils import timezone

class LoginView(TemplateView):
     template_name = 'houselog/login.html'

     # hide logout and title
     def get_context_data(self, **kwargs):
          context = {
               'suppress_header': True,
          }
          kwargs.update(context)
          return super().get_context_data(**kwargs)

     def get(self, request, *args, **kwargs):
          if request.user.is_authenticated:
               return redirect('dashboard')
          return super(LoginView, self).get(request, *args, **kwargs)

     def post(self, request, *args, **kwargs):
          user = authenticate(
               username=request.POST.get('username'),
               password=request.POST.get('password')
          )
          if user is not None:
               login(request, user)
               return redirect('dashboard')
          else:
               messages.add_message(request, messages.WARNING, "Incorrect username or password.")
               return redirect('login')

class DashboardListView(LoginRequiredMixin, ListView):
     context_object_name = 'houselog_items'
     template_name = 'houselog/dashboard.html'

     def get_queryset(self):
          dbres = Houselog.objects.filter(user=self.request.user)
          return sorted(dbres, key=lambda m: m.next_run)
     
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
               profile = form.save(commit=False)
               profile.user = request.user
               profile.save()
               return redirect('dashboard')
          else:
               messages.add_message(request, messages.WARNING, "Error when adding item.")
               return redirect('dashboard')

class DeleteItemView(LoginRequiredMixin, View):
     def post(self, request, *args, **kwargs):
          id = request.GET.get('id', None)
          if id:
               entry = Houselog.objects.get(id=id)
               entry.delete()
               return redirect('dashboard')
          else:
               messages.add_message(request, messages.WARNING, "Error deleting item.")
               return redirect('dashboard')

class DoneItemView(LoginRequiredMixin, View):
     def post(self, request, *args, **kwargs):
          id = request.GET.get('id', None)
          if id:
               entry = Houselog.objects.get(id=id)
               entry.last_done = request.POST.get('update_last_done')
               entry.save()
               return redirect('dashboard')
          else:
               messages.add_message(request, messages.WARNING, "Error updating item.")
               return redirect('dashboard')
          
class EditItemView(LoginRequiredMixin, ListView):
     context_object_name = 'item'
     template_name = 'houselog/edit.html'

     def get_queryset(self):
          id = self.request.GET.get('id', None)
          return Houselog.objects.get(id=id)
     
     def post(self, request, *args, **kwargs):
          id = self.request.GET.get('id', None)
          instance = Houselog.objects.get(id=id)
          
          if instance:
               form = h_forms.AddItemForm(request.POST, instance=instance)
               if form.is_valid():
                    form.save()
                    return redirect('dashboard')
               else:
                    messages.add_message(request, messages.WARNING, f"Error: {form.errors}")
                    return redirect('edit', id=id)