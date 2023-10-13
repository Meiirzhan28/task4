from django.shortcuts import render, redirect 
from django.contrib import messages
from django.views import View
from .forms import RegisterForm
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def block_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect(to='/user/')

@login_required
def unblock_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect(to='/user/')

@login_required
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect(to='/user/')

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def user_table(request):
    users = User.objects.all()
    return render(request, 'users/user_table.html', {'users': users})

def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)
    
class CustomLoginView(LoginView):
    form_class = LoginForm
    def form_valid(self, form):
        return super(CustomLoginView, self).form_valid(form)
    
def home(request):
    return render(request, 'users\home.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect(to='/')
        return render(request, self.template_name, {'form': form})