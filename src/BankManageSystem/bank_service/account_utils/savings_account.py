from django.db import connection
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib.auth.hashers import make_password, check_password
from ..models import Account, SavingsAccount, SavingsAccountRecord
from django.http import JsonResponse


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


@login_required
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


@login_required
def savings_account_transfer(request):
    if request.method == 'GET':
        return redirect('savings')
    elif request.method == 'POST':
        a_no = request.POST.get('a_no')
        amount = request.POST.get('amount')
        password = request.POST.get('password')
        target_a_no = request.POST.get('target')

        # 检查 target_a_no 是否与 a_no 相同
        if a_no == target_a_no:
            messages.error(request, f'账户号：{a_no}，无法为自己转账')
            return redirect('savings')

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
            _ = Account.objects.get(a_no=target_a_no)
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


@login_required
def savings_account_details(request):
    account_number = request.GET.get('account_number')

    if account_number:
        details = SavingsAccountRecord.objects.filter(
            sar_a_no=account_number
        ).order_by('-sar_time').values(
            'sar_a_no', 'sar_time', 'sar_other_a_no', 'sar_amount', 'sar_after_balance', 'sar_type'
        )

        account_info = Account.objects.filter(
            a_no=account_number
        ).values('a_currency').first()

        if account_info:
            currency = account_info['a_currency']
        else:
            currency = 'CNY'

        # 转化交易记录数据
        formatted_details = []
        for detail in details:
            formatted_balance = f"{currency} {detail['sar_after_balance']}"
            formatted_amount = f"{currency} {detail['sar_amount']}"

            # 时间格式化
            formatted_time = detail['sar_time'].strftime('%Y-%m-%d %H:%M:%S')

            # 类型转化为中文
            type_mapping = {
                'deposit': '存款',
                'withdraw': '取款',
                'transfer_in': '转入',
                'transfer_out': '转出'
            }
            formatted_type = type_mapping.get(detail['sar_type'], detail['sar_type'])

            # 如果 other_a_no 是自己，说明为存款取款，那么把对方账户号设为空
            formatted_other_a_no = detail['sar_other_a_no']
            if detail['sar_type'] in ['deposit', 'withdraw']:
                formatted_other_a_no = ''

            formatted_details.append({
                'd_time': formatted_time,
                'd_type': formatted_type,
                'd_other_a_no': formatted_other_a_no,
                'd_amount': formatted_amount,
                'd_balance': formatted_balance
            })
        return JsonResponse({"details": formatted_details}, safe=False)
    else:
        return JsonResponse({"error": "No account number provided"}, status=400)
