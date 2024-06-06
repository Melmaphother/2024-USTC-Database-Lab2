from django.db import connection
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib.auth.hashers import make_password, check_password
from ..models import Account, SavingsAccount, SavingsAccountRecord


@login_required
def savings_account_add(request):
    c_id = request.user.username
    if request.method == 'GET':
        return redirect('savings')
    elif request.method == 'POST':
        open_b_name = request.POST.get('open_b_name')
        rate = request.POST.get('rate')
        currency = request.POST.get('currency')
        withdraw_limit = request.POST.get('withdraw_limit')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if len(password) != 6:
            messages.error(request, '密码长度必须为6位')
            return redirect('savings')

        if password != confirm_password:
            messages.error(request, '两次密码不一致')
            return redirect('savings')

        password = make_password(password)  # 对密码进行加密

        rate = Decimal(rate) / 100
        withdraw_limit = Decimal(withdraw_limit)

        try:
            with connection.cursor() as cursor:
                cursor.callproc('savings_account_add', [c_id, open_b_name, rate, currency, withdraw_limit, password])
            messages.success(request, '创建账户成功')
        except:
            messages.error(request, '创建账户失败')

        return redirect('savings')


@login_required
def savings_account_deposit(request):
    if request.method == 'GET':
        return redirect('savings')
    elif request.method == 'POST':
        a_no = request.POST.get('a_no')
        amount = request.POST.get('amount')
        password = request.POST.get('password')

        # 检查 amount 是否为数字
        try:
            amount = Decimal(amount)
        except:
            messages.error(request, f'账户号：{a_no}，存款金额必须为数字')
            return redirect('savings')

        # 检查密码是否正确
        account = Account.objects.get(a_no=a_no)
        if not check_password(password, account.a_password_hash):
            messages.error(request, f'账户号：{a_no}，密码错误')
            return redirect('savings')

        try:
            with connection.cursor() as cursor:
                cursor.callproc('savings_account_deposit', [a_no, amount])
            # 获取当前的余额
            account = Account.objects.get(a_no=a_no)
            messages.success(request, f'账户号：{a_no}，存款成功，当前余额：{account.a_currency} {account.a_balance}')
        except:
            messages.error(request, f'账户号：{a_no}，存款失败')

        return redirect('savings')


def savings_account_withdraw(request):
    if request.method == 'GET':
        return redirect('savings')
    elif request.method == 'POST':
        a_no = request.POST.get('a_no')
        amount = request.POST.get('amount')
        password = request.POST.get('password')

        # 检查 amount 是否为数字
        try:
            amount = Decimal(amount)
        except:
            messages.error(request, f'账户号：{a_no}，取款金额必须为数字')
            return redirect('savings')

        # 检查密码是否正确
        account = Account.objects.get(a_no=a_no)
        if not check_password(password, account.a_password_hash):
            messages.error(request, f'账户号：{a_no}，密码错误')
            return redirect('savings')

        # 检查取款金额是否超过余额
        if account.a_balance < amount:
            messages.error(request, f'账户号：{a_no}，余额不足')
            return redirect('savings')

        # 从 savings_account 表中取出取款限额
        savings_account = SavingsAccount.objects.get(sa_no=a_no)
        # 检查取款金额是否超过取款限额
        if savings_account.sa_withdraw_limit < amount:
            messages.error(request, f'账户号：{a_no}，取款金额超过单次取款限额')
            return redirect('savings')

        try:
            with connection.cursor() as cursor:
                cursor.callproc('savings_account_withdraw', [a_no, amount])
            account = Account.objects.get(a_no=a_no)
            messages.success(request, f'账户号：{a_no}，取款成功，当前余额：{account.a_currency} {account.a_balance}')
        except:
            messages.error(request, f'账户号：{a_no}，取款失败')

        return redirect('savings')


def savings_account_transfer(request):
    if request.method == 'GET':
        return redirect('savings')
    elif request.method == 'POST':
        a_no = request.POST.get('a_no')
        amount = request.POST.get('amount')
        password = request.POST.get('password')
        target_a_no = request.POST.get('target')

        # 检查 amount 是否为数字
        try:
            amount = Decimal(amount)
        except:
            messages.error(request, f'账户号：{a_no}，转账金额必须为数字')
            return redirect('savings')

        # 检查密码是否正确
        account = Account.objects.get(a_no=a_no)
        if not check_password(password, account.a_password_hash):
            messages.error(request, f'账户号：{a_no}，密码错误')
            return redirect('savings')

        # 检查转账金额是否超过余额
        if account.a_balance < amount:
            messages.error(request, f'账户号：{a_no}，余额不足')
            return redirect('savings')

        # 从 savings_account 表中取出取款限额
        savings_account = SavingsAccount.objects.get(sa_no=a_no)
        # 检查转账金额是否超过取款限额
        if savings_account.sa_withdraw_limit < amount:
            messages.error(request, f'账户号：{a_no}，转账金额超过单次限额')
            return redirect('savings')

        # 检查目标账户号是否存在
        try:
            target_account = Account.objects.get(a_no=target_a_no)
        except:
            messages.error(request, f'目标账户号：{target_a_no}，不存在')
            return redirect('savings')

        try:
            with connection.cursor() as cursor:
                cursor.callproc('savings_account_transfer', [a_no, target_a_no, amount])
            account = Account.objects.get(a_no=a_no)
            messages.success(request, f'账户号：{a_no}，转账成功，当前余额：{account.a_currency} {account.a_balance}')
        except:
            messages.error(request, f'账户号：{a_no}，转账失败')

        return redirect('savings')
