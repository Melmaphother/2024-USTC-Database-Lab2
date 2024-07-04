from django.db import connection
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib.auth.hashers import check_password
from ..models import Account, Loan, LoanAccount, LoanGrant, LoanRepay
from datetime import datetime
from django.http import JsonResponse


@login_required
def loan_grant(request):
    if request.method == 'GET':
        return redirect('loan')
    elif request.method == 'POST':
        a_no = request.POST.get('a_no')
        loan_amount = request.POST.get('loan_amount')
        repay_deadline = request.POST.get('repay_deadline')
        password = request.POST.get('password')

        # 检查密码是否正确
        account = Account.objects.get(a_no=a_no)
        if not check_password(password, account.a_password_hash):
            messages.error(request, '密码错误')
            return redirect('loan')

        # 检查 loan_amount 是否为数字
        try:
            loan_amount = Decimal(loan_amount)
            # 检查 loan_amount 是否大于 0
            if loan_amount <= 0:
                messages.error(request, f'账户号：{a_no}，贷款金额必须大于0')
                return redirect('loan')
        except:
            messages.error(request, f'账户号：{a_no}，贷款金额必须为数字')
            return redirect('loan')

        # 根据 a_no 获取贷款账户的贷款额度
        loan_account = LoanAccount.objects.get(la_no=a_no)
        loan_limit = loan_account.la_loan_limit

        # 检查贷款额度是否足够
        if loan_amount > loan_limit:
            messages.error(request, f'账户号：{a_no}，贷款额度不足')
            return redirect('loan')

        # 按 YYYY-MM-DD 格式解析日期
        repay_deadline = datetime.strptime(repay_deadline, '%Y-%m-%d')

        # 调用存储过程
        try:
            with connection.cursor() as cursor:
                cursor.callproc('loan_grant', [a_no, loan_amount, repay_deadline])
            messages.success(request, f'账户号：{a_no}，贷款申请成功，等待发放')
        except:
            messages.error(request, f'账户号：{a_no}，贷款申请失败')

        return redirect('loan')


@login_required
def loan_repay(request):
    if request.method == 'GET':
        return redirect('loan')
    elif request.method == 'POST':
        loan_number = request.POST.get('loan_number')
        repay_amount = request.POST.get('repay_amount')
        password = request.POST.get('password')

        # 获取 loan 的状态
        loan = Loan.objects.get(l_no=loan_number)
        if loan.l_status == 'settled':
            messages.error(request, f'贷款号：{loan_number}，已结清，无需继续还贷')
            return redirect('loan')
        elif loan.l_status == 'pending':
            messages.error(request, f'贷款号：{loan_number}，未发放，无需还贷')
            return redirect('loan')

        # 从 LoanGrant 表中获取 a_no
        loan_grant_ = LoanGrant.objects.filter(
            lg_l_no=loan_number
        ).values('lg_la_no').first()
        a_no = loan_grant_['lg_la_no']

        # 检查密码是否正确
        account = Account.objects.get(a_no=a_no)
        if not check_password(password, account.a_password_hash):
            messages.error(request, f'账户号：{a_no}，密码错误')
            return redirect('loan')

        # 检查 repay_amount 是否为数字
        try:
            repay_amount = Decimal(repay_amount)
            # 检查 repay_amount 是否大于 0
            if repay_amount <= 0:
                messages.error(request, f'账户号：{a_no}，还款金额必须大于0')
                return redirect('loan')
        except:
            messages.error(request, f'账户号：{a_no}，还款金额必须为数字')
            return redirect('loan')

        # 调用存储过程
        try:
            with connection.cursor() as cursor:
                cursor.callproc('loan_repay', [loan_number, repay_amount])
            messages.success(request, f'账户号：{a_no}，还款成功')
        except:
            messages.error(request, f'账户号：{a_no}，还款失败')

        return redirect('loan')


@login_required
def loan_details(request):
    loan_number = request.GET.get('loan_number')

    if loan_number:
        # 从 LoanGrant 表中获取 a_no
        loan_grant_ = LoanGrant.objects.filter(
            lg_l_no=loan_number
        ).values('lg_la_no').first()
        a_no = loan_grant_['lg_la_no']

        details = LoanRepay.objects.filter(
            lr_l_no=loan_number
        ).order_by('-lr_repay_period').values(
            'lr_time', 'lr_amount', 'lr_repay_period', 'lr_after_repay_amount_total', 'lr_overpayment'
        )

        account_info = Account.objects.filter(
            a_no=a_no
        ).values('a_currency').first()

        if account_info:
            currency = account_info['a_currency']
        else:
            currency = 'CNY'

        formatted_details = []
        for detail in details:
            formatted_detail = {
                'lr_time': detail['lr_time'].strftime('%Y-%m-%d %H:%M:%S'),
                'lr_amount': f'{currency} {detail["lr_amount"]}',
                'lr_repay_period': detail['lr_repay_period'],
                'lr_after_repay_amount_total': f'{currency} {detail["lr_after_repay_amount_total"]}',
                'lr_overpayment': f'{currency} {detail["lr_overpayment"]}'
            }
            formatted_details.append(formatted_detail)

        return JsonResponse({"details": formatted_details}, safe=False)
    else:
        return JsonResponse({"error": "No loan number provided"}, status=400)
