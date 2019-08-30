from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "uc_profile.html")

    def post(self, request):
        ret_info = {"code": 200, "msg": "修改成功"}
        try:
            if request.POST.get("email"):
                request.user.email = request.POST.get("email")
            if request.POST.get("mobile"):
                request.user.mobile = request.POST.get("mobile")
            # if request.POST.get("qq"):
                # request.user.qq = request.POST.get("qq")
            if request.POST.get("username"):
                request.user.usernmae = request.POST.get("username")
            request.user.save()
        except Exception as ex:
            ret_info = {"code": 200, "msg": "修改失败"}
        return render(request, "uc_profile.html", {"ret_info":ret_info})
#       return JsonResponse(ret_info)


from django.views.generic import View, ListView
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
# 修改密码
class ChangePasswdView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "change_passwd.html")

    def post(self, request):
        # from表单提交的数据
        old_password = request.POST.get("oldpassword")
        new_password1 = request.POST.get("newpassword1")
        new_password2 = request.POST.get("newpassword2")

        ## 前端验证 new_password1 == new_password2 才能提交

        if new_password1 != new_password2:
            ret_info = {"code":400, "msg":"新密码不一致"}
        else:
            user = auth.authenticate(username=request.user.username, password=old_password)
            if user:
                user.set_password(new_password1)
                user.save()
                auth.logout(request)
                # auth.update_session_auth_hash(request, user)
                ret_info = {"code":200, "msg":"修改成功"}
            else:
                ret_info = {"code": 400, "msg": "旧密码不正确"}
        return render(request, "change_passwd.html", {"ret_info":ret_info})



import random
import string
from django.core.mail import send_mail
from apps.accounts.models import User
from .models import FindPassword
# 找回密码
class PasswordForget(View):
    def get(self, request):
        return render(request, "password_forget.html")

    def post(self, request):
        email = request.POST.get("email")
        print(email)
        if email and User.objects.filter(email=email):
            verify_code = "".join(random.choices(string.ascii_lowercase+string.digits, k=128))
            url = f"{request.scheme}://{request.META['HTTP_HOST']}/uc/password/reset/{verify_code}?email={email}"
            ret = FindPassword.objects.get_or_create(email=email)
            # (<FindPassword: FindPassword object>, True)
            ret[0].verify_code = verify_code
            ret[0].status = False
            ret[0].save()
            print(url)
            print("发邮件")
            send_mail('注册用户验证信息', url, None, [email])
            return HttpResponse("邮件发送成功，请登录邮箱查看！")
        else:
            msg = "输入的邮箱不存在！"
            return render(request, "password_forget.html", {"msg": msg})


# 重置密码
class PasswordReset(View):
    def get(self, request, verify_code):
        import datetime
        create_time_newer = datetime.datetime.utcnow()-datetime.timedelta(minutes=30)
        email = request.GET.get("email")
        # 邮箱、verify_code、status=False、时间近30分钟
        find_password = FindPassword.objects.filter(status=False, verify_code=verify_code, email=email, creat_time__gte=create_time_newer)
        # great_then_equal, lte, lt, gt
        if verify_code and find_password:
            return render(request, "password_reset.html")
        else:
            return HttpResponse("链接失效或有误")

    def post(self, request, verify_code):
        import datetime
        create_time_newer = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password2 == password1:
            try:
                find_password = FindPassword.objects.get(status=False, verify_code=verify_code, creat_time__gte=create_time_newer)
                user = User.objects.get(email=find_password.email)
                user.set_password(password1)
                user.save()
                msg = "重置密码成功，请登录"
                find_password.status = True
                find_password.save()
            except Exception as ex:
                # 记日志 ex
                msg = "出错啦"
        else:
            msg = "两次密码不一致"
        return render(request, "password_reset.html", {"msg":msg})

def Callme(request):
    return render(request,'QQandphone.html')