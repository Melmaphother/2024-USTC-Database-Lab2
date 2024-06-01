from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.http import HttpRequest
from django.contrib import messages
from captcha.image import ImageCaptcha
from io import BytesIO
import base64
import random


def customer_register(request: HttpRequest):
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
            'customer_register.html',
            {'captcha': image_data_url}
        )
    elif request.method == 'POST':
        id_number = request.POST.get('id_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        captcha = request.POST.get('captcha')

        # 检查验证码是否正确
        if captcha != request.session.get('captcha'):
            messages.error(request, '验证码错误')
            return redirect('customer_register')

        # 检查身份证号长度是否为 18 位
        if len(id_number) != 18:
            messages.error(request, '身份证号长度应为 18 位')
            return redirect('customer_register')
        # 检查身份证号是否已经存在，身份证号就是用户名
        if User.objects.filter(username=id_number).exists():
            messages.error(request, '已经注册，请勿重复注册')
            return redirect('customer_register')

        # 检查密码是否一致
        if password != confirm_password:
            messages.error(request, '密码不一致')
            return redirect('customer_register')

        # 检查密码长度是否在 6-10 之间
        if not 6 <= len(password) <= 10:
            messages.error(request, '密码长度应在 6-10 之间')
            return redirect('customer_register')

        # 创建用户
        user = User.objects.create_user(
            username=id_number,
            password=password
        )
        # 检查或创建 customer 用户组
        group, is_created = Group.objects.get_or_create(name='customer')
        if is_created:
            print('customer 用户组已创建')
        else:
            print('customer 用户组已存在')
        user.groups.add(group)

        # 标记为已经注册，没有输入个人信息，跳转到输入个人信息页面
        request.session['is_registered'] = True
        return redirect('edit_profile')


def edit_profile(request: HttpRequest):
    # 如果没有注册，跳转到注册页面
    if not request.session.get('is_registered', False):
        return redirect('customer_register')

    if request.method == 'GET':
        return render(
            request,
            'edit_profile.html'
        )
    elif request.method == 'POST':
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        address = request.POST.get('address')

        # 检查手机号长度是否为 11 位
        if len(phone) != 11:
            messages.error(request, '手机号长度应为 11 位')
            return redirect('edit_profile')
        # 检查年龄是否为数字
        try:
            age = int(age)
        except:
            messages.error(request, '年龄应为数字')
            return redirect('edit_profile')
        # 检查年龄是否在 0-150 之间
        if not 0 <= age <= 150:
            messages.error(request, '年龄应在 0-150 之间')
            return redirect('edit_profile')

        # 检查地址是否在 200 字以内
        if len(address) > 200:
            messages.error(request, '地址应在 200 字以内')
            return redirect('edit_profile')

        # 将这些信息写入 customer 表
        # TODO

        # 跳转到登录页面
        return redirect('login')
