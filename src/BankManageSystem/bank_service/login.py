from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from django.contrib import messages
from .gen_captcha import gen_captcha
from collections import defaultdict


def auth_login(request: HttpRequest):
    # 如果进入登录页面，清除 session 中的注册标记
    if 'is_registered' in request.session:
        del request.session['is_registered']

    if request.method == 'GET':
        login_dict = defaultdict()
        # 如果 session 中有上次登录的信息，直接填入
        if 'id_number' in request.session:
            login_dict['id_number'] = request.session['id_number']
        if 'password' in request.session:
            login_dict['password'] = request.session['password']
        # 生成新的验证码
        code, image_data_url = gen_captcha()
        request.session['code'] = code
        login_dict['captcha_url'] = image_data_url

        return render(
            request,
            'login.html',
            login_dict
        )

    elif request.method == 'POST':
        id_number = request.POST.get('id_number')
        password = request.POST.get('password')
        captcha = request.POST.get('captcha')  # 用户输入的验证码
        code = request.session.get('code')  # session 中验证码的真实值
        # 将用户输入的信息保存到 session 中
        request.session['id_number'] = id_number
        request.session['password'] = password

        # 检查验证码是否正确
        if captcha != code:
            messages.error(request, '验证码错误')
            return redirect('login')

        # 验证用户
        user = authenticate(request, username=id_number, password=password)
        # 如果用户存在，则进入主页
        if user is not None:
            login(request, user)
            # 删除所有登录相关的 session
            if 'id_number' in request.session:
                del request.session['id_number']
            if 'password' in request.session:
                del request.session['password']
            return redirect('dashboard')
        # 如果用户不存在，需要重新登录
        else:
            messages.error(request, '用户名或密码输入错误')
            if 'id_number' in request.session:
                del request.session['id_number']
            if 'password' in request.session:
                del request.session['password']
            return redirect('login')
