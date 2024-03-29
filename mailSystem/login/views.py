from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from . import models
from . import forms
import hashlib
import login.RSA as rsa
import login.RSAmakeKey as rsamake
from django.contrib import messages


# from login import login_handler
# Create your views here.

# 哈希运算
def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    name = request.session['user_name']
    user = models.User.objects.get(name=name)
    user_all = user._meta.get_fields()
    # user_all = models.User.objects.all()
    rmails = models.Recipemail.objects.filter(recipient=user.email)
    return render(request, 'login/index.html', locals())


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
            except :
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())

            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                rsamake.make_my_rsa(username)
                new_key = models.PublicKey()
                with open(username + '-public.pem', 'rb') as f:
                    public_key = f.read()
                new_key.user = username
                new_key.publicKey = public_key
                new_key.save()
                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    request.session.flush()
    # del request.session['is_login']
    return redirect("/login/")


def readmail(request, rmail_id):
    rmail = get_object_or_404(models.Recipemail, id=rmail_id)
    request.id = rmail_id
    print(request.session['user_name'])
    mail = models.Recipemail.objects.get(id=rmail_id)
    name = mail.addresser
    i = name.find('@')
    print(i)
    user = models.PublicKey.objects.get(user=name[:3])
    with open('bjw-private.pem', 'rb') as f:
        public_key = f.read()
    sign = models.Recipemail.objects.get(id=rmail_id)
    if rsa.rsa_verify(sign.affix,sign.letter.encode('utf-8'),public_key):
        messages.success(request, "验证成功")
    else:
        messages.success(request, "验证失败")
    return render(request, 'login/readmail.html', locals())


def compose(request):
    # if request.session.get('is_login', None):
    #     return redirect('/index/')

    if request.method == 'POST':
        mail_form = forms.MailForm(request.POST)
        if mail_form.is_valid():
            subject = request.POST.get('subject')
            recipient = request.POST.get('recipient')
            letter = request.POST.get('letter')
            # 验证
            name = request.session['user_name']
            new_mail = models.Recipemail()
            new_mail.subject = subject
            new_mail.addresser = recipient
            new_mail.recipient = recipient
            new_mail.letter = letter
            with open(name + '-private.pem','rb') as f:
                private_key = f.read()
            new_mail.affix = rsa.rsa_sign(letter.encode(encoding='utf-8'),private_key)
            new_mail.status = 1
            new_mail.save()
            messages.success(request, "发送成功")
            return redirect('/compose/')
        else:
            return render(request, 'login/compose.html', locals())
    mail_form = forms.MailForm()
    return render(request, 'login/compose.html', locals())

