from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from django.contrib import messages
from .gen_captcha import gen_captcha


def auth_login(request: HttpRequest):
    # 如果进入登录页面，清除 session 中的注册标记
    if 'is_registered' in request.session:
        del request.session['is_registered']

    if request.method == 'GET':
        # 生成验证码
        code, image_data_url = gen_captcha()
        request.session['captcha'] = code
        return render(
            request,
            'login.html',
            {'captcha': image_data_url}
        )

    elif request.method == 'POST':
        id_number = request.POST.get('id_number')
        password = request.POST.get('password')
        captcha = request.POST.get('captcha')

        # 检查验证码是否正确
        if captcha != request.session.get('captcha'):
            messages.error(request, '验证码错误')
            return redirect('login')

        # 验证用户
        user = authenticate(request, username=id_number, password=password)
        # 如果用户存在，则进入主页
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        # 如果用户不存在，需要重新登录
        else:
            messages.error(request, '用户名或密码输入错误')
            return redirect('login')
