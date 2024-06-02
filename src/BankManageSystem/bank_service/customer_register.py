from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.http import HttpRequest
from django.contrib import messages
from .gen_captcha import gen_captcha
from .models import Customer


def customer_register(request: HttpRequest):
    if request.method == 'GET':
        # 生成验证码
        code, image_data_url = gen_captcha()
        request.session['captcha'] = code
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
        # 这里不需要检查 id_number 是否为 None，因为提交表单时，id_number 不能为空
        if len(id_number) != 18:
            messages.error(request, '身份证号长度应为 18 位')
            return redirect('customer_register')
        # 检查身份证号是否已经存在，身份证号就是用户名
        if User.objects.filter(username=id_number).exists():
            messages.error(request, '已经注册，请勿重复注册')
            return redirect('customer_register')

        # 检查密码长度是否在 6-10 之间，这里也不需要检查 password 是否为 None
        if not 6 <= len(password) <= 10:
            messages.error(request, '密码长度应在 6-10 之间')
            return redirect('customer_register')

        # 检查密码是否一致
        if password != confirm_password:
            messages.error(request, '密码不一致')
            return redirect('customer_register')

        # 创建用户
        user = User.objects.create_user(
            username=id_number,
            password=password
        )
        # 检查是否存在 customer 用户组，不存在则创建 customer 用户组
        group, _ = Group.objects.get_or_create(name='customer')
        user.groups.add(group)  # 将用户添加到 customer 用户组

        # 将用户同时加入 Customer 表
        Customer.objects.create(
            c_id=id_number
        )
        # 保存身份证号到 session 中
        request.session['id_number'] = id_number

        # 标记为已经注册，没有输入个人信息
        # 这个字段用于：无法直接访问个人信息页面而不经过注册页面
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

        # 检查 name 长度是否小于等于 50，不需要检查 name 是否为 None
        if len(name) > 50:
            messages.error(request, '姓名应在 50 字以内')
            return redirect('edit_profile')

        # 将 gender 转换为单个字符
        if gender:
            if gender == "male":
                gender = "M"
            else:
                gender = "F"

        # 检查手机号长度是否为 11 位，注意未提交的 post 为 None
        if phone and len(phone) != 11:
            messages.error(request, '手机号长度应为 11 位')
            return redirect('edit_profile')
        if age:
            # 检查年龄是否为数字
            try:
                age = int(age)  # 不能直接转换为 int，int 方法会抛出异常
            except:
                messages.error(request, '年龄应为数字')
                return redirect('edit_profile')
            # 检查年龄是否在 0-150 之间
            if not 0 <= age <= 150:
                messages.error(request, '年龄应在 0-150 之间')
                return redirect('edit_profile')

        # 检查地址是否在 200 字以内
        if address and len(address) > 200:
            messages.error(request, '地址应在 200 字以内')
            return redirect('edit_profile')

        # 将这些信息写入 customer 表对应表项
        c_id = request.session.get('id_number')
        customer = Customer.objects.get(c_id=c_id)
        customer.c_name = name
        customer.c_gender = gender
        customer.c_age = age
        customer.c_phone = phone
        customer.c_addr = address
        customer.save()

        # 跳转到登录页面
        return redirect('login')
