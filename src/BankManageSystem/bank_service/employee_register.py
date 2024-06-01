from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.http import HttpRequest
from django.contrib import messages
from captcha.image import ImageCaptcha
from io import BytesIO
import base64
import random