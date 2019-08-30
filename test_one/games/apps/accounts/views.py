from django.shortcuts import render
from apps.download.models import GameDetails
# Create your views here.
import re
from django.core.mail import send_mail
from .models import User
import random,string

def index(request):
    game1 = GameDetails.objects.get(game_name="剑士")
    game2 = GameDetails.objects.get(game_name="汤姆克兰西：全境封锁2")
    game3 = GameDetails.objects.get(game_name="皇牌空战7：未知空域")
    game4 = GameDetails.objects.get(game_name="正当防卫4")
    game5 = GameDetails.objects.get(game_name="刺客信条：起源")
    game6 = GameDetails.objects.get(game_name="天国：拯救")
    game7 = GameDetails.objects.get(game_name="腐烂国度2")
    game8 = GameDetails.objects.get(game_name="古墓丽影：暗影")
    game9 = GameDetails.objects.get(game_name="尼尔：机械纪元")
    game10 = GameDetails.objects.get(game_name="狙击精英V2重制版")
    # game1 = games.filter(game_name="剑士")

    kwsg = {
        "game1":game1,
        "game2":game2,
        "game3":game3,
        "game4":game4,
        "game5":game5,
        "game6":game6,
        "game7":game7,
        "game8":game8,
        "game9":game9,
        "game10":game10,

    }
    return render(request,'accounts/index.html',kwsg)


def login_test(request):
    return render(request, 'accounts/login.html')
# def login(request):
#     return render(request,'accounts/login.html')
#
# def register(request):
#     return render(request,'accounts/register.html')

from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views.generic import View
from django.core.cache import cache
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.http import JsonResponse
import logging
from .forms import RegisterForm, LoginForm
from .models import User
logger = logging.getLogger("account")

# Create your views here.


class Register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "accounts/register.html", {"form":form})

    # Ajax提交表单
    def post(self, request):
        ret = {"status": 400, "msg": "调用方式错误"}
        # 检查是不是ajax的请求
        if request.is_ajax():
            form = RegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                email = form.cleaned_data["email"]
                mobile = form.cleaned_data["mobile"]
                mobile_captcha = form.cleaned_data["mobile_captcha"]
                mobile_captcha_reids = cache.get(email)
                if mobile_captcha == mobile_captcha_reids:
                    user = User.objects.create(username=username, password=make_password(password),mobile=mobile,email=email)
                    user.save()
                    ret['status'] = 200
                    ret['msg'] = "注册成功"
                    logger.debug(f"新用户{username}注册成功！")
                    user = auth.authenticate(username=username, password=password)
                    if user is not None and user.is_active:
                        auth.login(request, user)
                        logger.debug(f"新用户{user}登录成功")
                    else:
                        logger.error(f"新用户{user}登录失败")
                else:
                    # 验证码错误
                    ret['status'] = 401
                    ret['msg'] = "验证码错误或过期"
            else:
                ret['status'] = 402
                ret['msg'] = form.errors

        logger.debug(f"用户注册结果：{ret}")
        return JsonResponse(ret)


class Login(View):
    def get(self, request):
        # 设置下一跳转地址(如果get有next，如果没有跳转到repo:index)
        request.session["next"] = request.GET.get('next', reverse('index'))
        # 如果已登录，则直接跳转到index页面
        # request.user 表示的是当前登录的用户对象,没有登录 `匿名用户`
        if request.user.is_authenticated:
            return redirect(request.session["next"])
        form = LoginForm()
        return render(request, "accounts/login.html", {"form":form})
        # return render_to_response("login.html", {"form":form})


    # Form表单直接提交
    def post(self, request):
        # 表单数据绑定
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            captcha = form.cleaned_data["captcha"]
            session_captcha_code = request.session.get("captcha_code", "")
            logger.debug(f"登录提交验证码:{captcha}-{session_captcha_code}")
            # 验证码一致
            # print(captcha.lower(), session_captcha_code.lower())
            if captcha.lower() == session_captcha_code.lower():
                user, flag = form.check_password()
                # user = auth.authenticate(username=username, password=password)
                if flag and user and user.is_active:
                    auth.login(request, user)
                    logger.info(f"{user.username}登录成功")
                    # 跳转到next
                    return redirect(request.session.get("next", 'index.html'))
            msg = "用户名或密码错误"
            logger.error(f"{username}登录失败, 用户名或密码错误")
            # else:
            #     msg = "验证码错误"
            #     logger.error(f"{username}登录失败, 验证码错误")
        else:
            msg = "表单数据不完整"
            logger.error(msg)
        return render(request, "accounts/login.html", {"form": form, "msg": msg})

def logout(request):
    auth.logout(request)
    return redirect(reverse("index"))


# 邮箱验证码
class Email_check(View):
    def post(self,request):
        email = request.POST.get("email")
        print(email)
        ret = {"status": 400, "msg": "调用方式错误"}
        # 已存在人数
        use_num = User.objects.filter(email=email).count()
        if use_num == 0:
            if re.match(r'^([\w]+\.*)([\w]+)\@[\w]+\.\w{3}(\.\w{2}|)$', email) is not None:
                email_code = "".join(random.choices(string.digits, k=6))
                from django.core.cache import cache
                cache.set(email, email_code, 300)
                send_mail('《游林网》——', f"您的验证码为：{email_code} ，请在30分钟内输入验证，如超时您需重新获取~", None, [email])
                print(1234)
                ret["status"] = 200
                ret["msg"] = "邮件发送成功，请登录邮箱查看！如果未找到可能在回收箱中。"
                return JsonResponse(ret, safe=False)
            else:
                ret["status"] = 404
                if email:
                    ret["msg"] = "输入的邮箱不合法！"
                    return JsonResponse(ret, safe=False)
                else:
                    ret["msg"] = "请输入邮箱号！"
                    return JsonResponse(ret, safe=False)
        else:
            ret["msg"] = "此邮箱已存在"
            return JsonResponse(ret, safe=False)
