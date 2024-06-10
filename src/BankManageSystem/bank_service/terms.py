from django.shortcuts import render

def terms(request):
    """显示使用条款页面"""
    return render(request, 'terms.html')

def privacy(request):
    """显示隐私政策页面"""
    return render(request, 'privacy.html')