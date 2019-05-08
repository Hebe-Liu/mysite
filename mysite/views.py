from django.shortcuts import render, render_to_response,get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import LoginForm, RegisterForm
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from read_count.utils import get_seven_days_read

def home(request):

    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums = get_seven_days_read(blog_content_type)
    context = {}
    context['read_nums'] = read_nums
    return render_to_response('home.html',context)

def check_login(request):

    if request.method == "POST":
        # 提交数据
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        # 加载页面
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request,'login.html',context)

def register(request):

    if request.method == "POST":
        # 提交数据
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username,email,password)
            user.save()
            # 用户登陆
            user = authenticate(username=username,password=password)
            login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        # 加载页面
        register_form = RegisterForm()

    context = {}
    context['register_form'] = register_form
    return render(request,'register.html',context)

