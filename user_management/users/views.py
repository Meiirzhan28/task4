from django.shortcuts import render, redirect 
from django.contrib import messages
from django.views import View
from .forms import RegisterForm
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def block_user(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            selected_users_id = request.POST.getlist('boxes')
            caller_id = request.user.id
            selected_users_id.remove(str(caller_id))
            for id in selected_users_id:
                u = User.objects.get(id = id)
                u.is_active = False
                u.save()
                messages.success(request, "The User is Blocked")
            return redirect(to='/user/')

@login_required
def unblock_user(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            selected_users_id = request.POST.getlist('boxes')
            caller_id = request.user.id
            selected_users_id.remove(str(caller_id))
            for id in selected_users_id:
                u = User.objects.get(id = id)
                u.is_active = True
                u.save()
                messages.success(request, "The User is Unblocked")
            return redirect(to='/user/') 

@login_required
def delete_user(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            selected_users_id = request.POST.getlist('boxes')
            caller_id = request.user.id
            selected_users_id.remove(str(caller_id))
            for id in selected_users_id:
                u = User.objects.get(id = id)
                u.delete()
                messages.success(request, "The User is Deleted")
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
    return render(request, 'users/home.html')

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