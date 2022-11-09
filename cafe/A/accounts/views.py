from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterationForm, UserLoginForm, UpdateProfileForm
from django.shortcuts import render
from .models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Receipt, Order, Table, MenuItem
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class UserRegisterView(View):
    from_class = UserRegisterationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.from_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.from_class(request.POST)
        if form.is_valid():
            User.objects.create_user(email=form.cleaned_data['email'], phone_number=form.cleaned_data['phone_number'],
                                     full_name=form.cleaned_data['full_name'], password=form.cleaned_data['password'])
            messages.success(request, 'ورود با موفقیت', 'success')
            return redirect('home:home')
        messages.error(request, 'اطلاعات صحیح نیست', 'danger')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'خروج از حساب کاربری با موفقیت انجام شد', 'success')
        return redirect('home:home')


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'ورود به حساب کاربری با موفقیت انجام شد', 'success')
                return redirect('home:home')
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است', 'danger')
        return render(request, self.template_name, {'form': form})


class UserProfileView(LoginRequiredMixin, View):
    form = UpdateProfileForm()
    template_name = 'accounts/profile.html'

    def get(self, request):
        orders = {}
        # for i in Receipt.objects.filter(user=request).order_by(Receipt.timestamp.desc()).all():
        for i in Receipt.objects.filter(users=request.user):
            orders[i] = []
            for j in Order.objects.filter(users=request.user):
                print(j)
                if i == j.receipts:
                    orders[i].append(j)
        print(orders)
        return render(request, self.template_name, {'form': self.form, 'orders': orders})
