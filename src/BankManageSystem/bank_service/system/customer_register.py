from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.contrib import messages
from .gen_captcha import gen_captcha
from bank_service.models import Customer
from collections import defaultdict
from pathlib import Path


def customer_register(request):
    if request.method == 'GET':
        register_dict = defaultdict()
        # 如果 session 中有上次登录的信息，直接填入
        if 'id_number' in request.session:
            register_dict['id_number'] = request.session['id_number']
        if 'password' in request.session:
            register_dict['password'] = request.session['password']
        if 'confirm_password' in request.session:
            register_dict['confirm_password'] = request.session['confirm_password']
        # 生成新的验证码
        code, image_data_url = gen_captcha()
        request.session['code'] = code
        register_dict['captcha_url'] = image_data_url
        return render(
            request,
            'customer_register.html',
            register_dict
        )
    elif request.method == 'POST':
        id_number = request.POST.get('id_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        captcha = request.POST.get('captcha')  # 用户输入的验证码
        code = request.session.get('code')  # session 中验证码的真实值
        # 将用户输入的信息保存到 session 中
        request.session['id_number'] = id_number
        request.session['password'] = password
        request.session['confirm_password'] = confirm_password

        # 检查验证码是否正确
        if captcha != code:
            messages.error(request, '验证码错误')
            return redirect('customer_register')

        # 检查身份证号长度是否为 18 位
        # 这里不需要检查 id_number 是否为 None，因为提交表单时，id_number 不能为空
        if len(id_number) != 18:
            messages.error(request, '身份证号长度应为 18 位')
            if 'id_number' in request.session:
                del request.session['id_number']
            return redirect('customer_register')
        # 检查身份证号是否已经存在，身份证号就是用户名
        if User.objects.filter(username=id_number).exists():
            messages.error(request, '已经注册，请勿重复注册')
            if 'id_number' in request.session:
                del request.session['id_number']
            return redirect('customer_register')

        # 检查密码长度是否在 6-10 之间，这里也不需要检查 password 是否为 None
        if not 6 <= len(password) <= 10:
            messages.error(request, '密码长度应在 6-10 之间')
            if 'password' in request.session:
                del request.session['password']
            if 'confirm_password' in request.session:
                del request.session['confirm_password']
            return redirect('customer_register')

        # 检查密码是否一致
        if password != confirm_password:
            messages.error(request, '密码不一致')
            if 'password' in request.session:
                del request.session['password']
            if 'confirm_password' in request.session:
                del request.session['confirm_password']
            return redirect('customer_register')

        # 使用 USTCer 作为默认姓名
        default_name = 'USTCer'

        # 使用 logo.png 作为默认头像
        # 使用用户的 id_avatar 作为文件名
        fs = FileSystemStorage(location=Path.joinpath(settings.MEDIA_ROOT, 'avatar'))
        avatar_name = f'{id_number}_avatar.jpg'
        default_avatar_path = Path.joinpath(settings.STATICFILES_DIRS[0], 'image/logo.png')
        with open(default_avatar_path, 'rb') as f:
            default_avatar = ContentFile(f.read())
        # 若之前指定头像则替换它
        if fs.exists(avatar_name):
            fs.delete(avatar_name)
        fs.save(avatar_name, default_avatar)
        upload_avatar_url = f'avatar/{avatar_name}'

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
            c_id=id_number,
            c_name=default_name,
            c_avatar=upload_avatar_url
        )

        # 标记为已经注册，没有输入个人信息
        # 这个字段用于：无法直接访问编辑个人信息页面而不经过注册页面
        request.session['is_registered'] = True
        # 将 session 中的 confirm_password 删除
        if 'confirm_password' in request.session:
            del request.session['confirm_password']
        return redirect('edit_profile')


def edit_profile(request):
    # 如果没有注册，跳转到注册页面
    if not request.session.get('is_registered', False):
        return redirect('customer_register')

    if request.method == 'GET':
        edit_profile_dict = defaultdict()
        # 如果 session 中有上次登录的信息，直接填入
        if 'name' in request.session:
            edit_profile_dict['name'] = request.session['name']
        if 'upload_avatar' in request.session:
            edit_profile_dict['upload_avatar'] = request.session['upload_avatar']
        if 'gender' in request.session:
            edit_profile_dict['gender'] = request.session['gender']
        if 'phone' in request.session:
            edit_profile_dict['phone'] = request.session['phone']
        if 'age' in request.session:
            edit_profile_dict['age'] = request.session['age'] if request.session['age'] else ''
        if 'address' in request.session:
            edit_profile_dict['address'] = request.session['address']
        return render(
            request,
            'edit_profile.html',
            edit_profile_dict
        )
    elif request.method == 'POST':
        # 从注册过程中保存的 session 中获取用户 id
        c_id = request.session.get('id_number')

        name = request.POST.get('name')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        address = request.POST.get('address')
        # 将用户输入的信息保存到 session 中
        request.session['name'] = name
        request.session['gender'] = gender
        request.session['phone'] = phone
        request.session['age'] = age
        request.session['address'] = address

        # 检查 name 长度是否小于等于 50，不需要检查 name 是否为 None
        if len(name) > 50:
            messages.error(request, '姓名应在 50 字以内')
            if 'name' in request.session:
                del request.session['name']
            return redirect('edit_profile')

        # 将 gender 转换为单个字符
        if gender:
            if gender == "male":
                gender = "M"
            else:
                gender = "F"
        else:
            gender = ''  # 这里不能设为 None，因为 models 中该字段为 CharField，null=False

        # 检查手机号长度是否为 11 位，注意未提交的 post 为 None
        if phone:
            if len(phone) != 11:
                messages.error(request, '手机号长度应为 11 位')
                if 'phone' in request.session:
                    del request.session['phone']
                return redirect('edit_profile')
        else:
            phone = ''

        if age:
            # 如果输入了年龄，检查年龄是否为数字
            try:
                age = int(age)  # 不能直接转换为 int，int 方法会抛出异常
            except:
                messages.error(request, '年龄应为数字')
                if 'age' in request.session:
                    del request.session['age']
                return redirect('edit_profile')
            # 检查年龄是否在 0-150 之间
            if not 0 <= age <= 150:
                messages.error(request, '年龄应在 0-150 之间')
                if 'age' in request.session:
                    del request.session['age']
                return redirect('edit_profile')
        else:
            age = None  # age 是 IntegerField，可以设为 None

        # 检查地址是否在 200 字以内
        if address:
            if len(address) > 200:
                messages.error(request, '地址应在 200 字以内')
                if 'address' in request.session:
                    del request.session['address']
                return redirect('edit_profile')
        else:
            address = ''

        # 将这些信息写入 customer 表对应表项
        customer = Customer.objects.get(c_id=c_id)
        customer.c_name = name
        customer.c_gender = gender
        customer.c_age = age
        customer.c_phone = phone
        customer.c_addr = address
        customer.save()

        # 直接为用户登录
        # 验证用户
        user = authenticate(request, username=c_id, password=request.session.get('password'))
        # 如果用户存在，则进入主页
        if user is not None:
            login(request, user)
            # 删除所有注册相关的 session
            if 'id_number' in request.session:
                del request.session['id_number']
            if 'password' in request.session:
                del request.session['password']
            if 'name' in request.session:
                del request.session['name']
            if 'gender' in request.session:
                del request.session['gender']
            if 'phone' in request.session:
                del request.session['phone']
            if 'age' in request.session:
                del request.session['age']
            if 'address' in request.session:
                del request.session['address']
            return redirect('dashboard')
        # 如果用户不存在，其实是出错的
