from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bank_service.models import Customer
from collections import defaultdict
from pathlib import Path


@login_required
def profile(request):
    c_id = request.user.username
    if request.method == 'GET':
        customer = Customer.objects.get(c_id=c_id)
        profile_dict = defaultdict()
        profile_dict['c_id'] = c_id
        profile_dict['c_name'] = customer.c_name
        profile_dict['c_gender'] = customer.c_gender
        profile_dict['c_age'] = customer.c_age if customer.c_age else ''
        profile_dict['c_phone'] = customer.c_phone
        profile_dict['c_addr'] = customer.c_addr
        profile_dict['c_avatar'] = customer.c_avatar
        return render(
            request,
            'dashboard/profile.html',
            profile_dict
        )
    elif request.method == 'POST':
        upload_avatar = request.FILES.get('avatar')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        address = request.POST.get('address')

        # 保存头像文件到对应位置
        # 使用用户的 id_avatar 作为文件名
        if upload_avatar:
            print("allowed")
            # 不允许头像大于 1M
            if upload_avatar.size > 1024 * 1024:
                messages.error(request, '头像图片大小不能超过 1MB')
                return redirect('profile')

            fs = FileSystemStorage(location=Path.joinpath(settings.MEDIA_ROOT, 'avatar'))
            avatar_name = f'{c_id}_avatar.jpg'
            # 若之前指定头像则替换它
            if fs.exists(avatar_name):
                fs.delete(avatar_name)
            fs.save(avatar_name, upload_avatar)
            upload_avatar = f'avatar/{avatar_name}'

        # 检查手机号长度是否为 11 位，注意未提交的 post 为 None
        if phone:
            if len(phone) != 11:
                messages.error(request, '手机号长度应为 11 位')
                return redirect('profile')
        else:
            phone = ''

        if age:
            # 检查年龄是否为数字
            try:
                age = int(age)  # 不能直接转换为 int，int 方法会抛出异常
            except:
                messages.error(request, '年龄应为数字')
                return redirect('profile')
            # 检查年龄是否在 0-150 之间
            if not 0 <= age <= 150:
                messages.error(request, '年龄应在 0-150 之间')
                return redirect('profile')
        else:
            age = None

        # 检查地址是否在 200 字以内
        if address:
            if len(address) > 200:
                messages.error(request, '地址应在 200 字以内')
                return redirect('profile')
        else:
            address = ''

        customer = Customer.objects.get(c_id=c_id)
        # 如果上传图片为 None，那么仍然使用之前的头像
        customer.c_avatar = upload_avatar if upload_avatar else customer.c_avatar
        customer.c_age = age
        customer.c_phone = phone
        customer.c_addr = address
        customer.save()

        # 重定向到 profile 页面
        return redirect('profile')
