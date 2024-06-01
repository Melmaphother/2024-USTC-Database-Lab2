from django.shortcuts import render


def dashboard(request):
    return render(
        request,
        'dashboard/dashboard.html'
    )


def profile(request):
    return render(
        request,
        'dashboard/profile.html'
    )


def savings(request):
    return render(
        request,
        'dashboard/savings.html'
    )


def credit(request):
    return render(
        request,
        'dashboard/credit.html'
    )


def loan(request):
    return render(
        request,
        'dashboard/loan.html'
    )


def logout(request):
    return render(
        request,
        'dashboard/logout.html'
    )