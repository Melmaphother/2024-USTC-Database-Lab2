from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import models
from collections import defaultdict
from pathlib import Path


@login_required
def dashboard(request):
    c_id = request.user.username
    customer = models.Customer.objects.get(c_id=c_id)
    dashboard_dict = defaultdict()
    dashboard_dict['c_id'] = c_id
    dashboard_dict['c_name'] = customer.c_name
    dashboard_dict['c_avatar'] = customer.c_avatar
    account_types = {
        'SavingsAccount': 'Saving',
        'CreditAccount': 'Credit',
        'LoanAccount': 'Loan'
    }

    account_numbers = models.AccountHoldManage.objects.filter(
        ahm_c_id=c_id
    ).values_list('ahm_a_no', flat=True)

    for key, account_type in account_types.items():
        accounts = models.Account.objects.filter(
            a_no__in=account_numbers,
            a_type=account_type
        ).order_by('-a_open_time').values(
            'a_no', 'a_balance', 'a_currency', 'a_open_time', 'a_open_b_name'
        )
        formatted_accounts = []
        for account in accounts:
            # 格式化余额和货币单位
            formatted_balance = f"{account['a_currency']} {account['a_balance']:.2f}"
            account['formatted_balance'] = formatted_balance
            # 移除原始的余额和货币字段
            del account['a_balance'], account['a_currency']
            formatted_accounts.append(account)

        dashboard_dict[key] = formatted_accounts

    return render(
        request,
        'dashboard/dashboard.html',
        dashboard_dict
    )


@login_required
def profile(request):
    c_id = request.user.username
    if request.method == 'GET':
        customer = models.Customer.objects.get(c_id=c_id)
        profile_dict = defaultdict()
        profile_dict['c_id'] = c_id
        profile_dict['c_name'] = customer.c_name
        profile_dict['c_gender'] = customer.c_gender
        profile_dict['c_age'] = customer.c_age
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
        if phone and len(phone) != 11:
            messages.error(request, '手机号长度应为 11 位')
            return redirect('profile')
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

        # 检查地址是否在 200 字以内
        if address and len(address) > 200:
            messages.error(request, '地址应在 200 字以内')
            return redirect('profile')

        customer = models.Customer.objects.get(c_id=c_id)
        # 如果上传图片为 None，那么仍然使用之前的头像
        customer.c_avatar = upload_avatar if upload_avatar else customer.c_avatar
        customer.c_age = age
        customer.c_phone = phone
        customer.c_addr = address
        customer.save()

        # 重定向到 profile 页面
        return redirect('profile')


@login_required
def savings(request):
    return render(
        request,
        'dashboard/savings.html'
    )


@login_required
def credit(request):
    return render(
        request,
        'dashboard/credit.html'
    )


@login_required
def loan(request):
    return render(
        request,
        'dashboard/loan.html'
    )


@login_required
def logout(request):
    return render(
        request,
        'dashboard/logout.html'
    )
