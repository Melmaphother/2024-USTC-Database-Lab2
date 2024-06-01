from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from django.contrib import messages
from captcha.image import ImageCaptcha
from io import BytesIO
import base64
import random


def auth_login(request: HttpRequest):
    # 如果进入登录页面，清除 session 中的注册标记
    if 'is_registered' in request.session:
        del request.session['is_registered']

    if request.method == 'GET':
        # 生成验证码
        image = ImageCaptcha(width=120, height=40)
        code = str(random.randint(1000, 9999))
        request.session['captcha'] = code
        data = image.generate(code)
        image_file = BytesIO(data.read())
        # 转化为base64
        image_data = base64.b64encode(image_file.getvalue()).decode('utf-8')
        image_data_url = f"data:image/png;base64,{image_data}"
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
