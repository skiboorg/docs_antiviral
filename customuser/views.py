from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from customuser.models import User
from django.http import JsonResponse, HttpResponseRedirect
from .forms import SignUpForm, UpdateForm
# from order.models import Wishlist,Order
from django.core.mail import send_mail
from django.template.loader import render_to_string

def create_password():
    from random import choices
    import string
    password = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
    return password

def account(request):
    if request.user.is_authenticated:
        return render(request, 'pages/lk.html', locals())
    else:
        return HttpResponseRedirect('/')

def orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(client=request.user)
        return render(request, 'lk/orders.html', locals())
    else:
        return HttpResponseRedirect('/')

def order(request, order_code):
    if request.user.is_authenticated:
        order = Order.objects.get(order_code=order_code)
        return render(request, 'lk/order.html', locals())
    else:
        return HttpResponseRedirect('/')

def account_edit(request):

    client = request.user
    print(request.POST)
    if request.POST:
        form = UpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            client.profile_ok = True
            client.save(force_update=True)
            print(form.errors)
        return render(request, 'pages/lk.html', locals())
    else:

        form = UpdateForm(instance=client)
        return render(request, 'pages/lk.html', locals())


def wishlist(request):
    if request.user.is_authenticated:
        wish_list = Wishlist.objects.filter(client=request.user)
        items=[]
        for i in wish_list:
            items.append(i.item)
        return render(request, 'lk/wishlist.html', locals())
    else:
        return HttpResponseRedirect('/')


def restore(request):
    return_dict = {}
    return_dict['result'] = False
    try:
        user = User.objects.get(email=request.POST.get('email'))
    except:
        user = None

    if user:
        new_password = create_password()
        user.set_password(new_password)
        user.save()
        return_dict['result'] = True
        msg_html = render_to_string('email/restore_passord.html', {'login': user.email, 'password': new_password})
        send_mail('Новый пароль на сайте LAKSHMI888', None, 'info@lakshmi888.ru', [user.email],
                  fail_silently=False, html_message=msg_html)
    return JsonResponse(return_dict)


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_page(request):
    return render(request, 'pages/login.html', locals())

def reg_page(request):
    return render(request, 'pages/register.html', locals())

def log_in(request):
    return_dict = {}
    email = request.POST.get('email')
    password = request.POST.get('password')
    print(request.POST)

    user = authenticate(email=email, password=password)
    print(user)
    if user is not None:
        login(request, user)
        return_dict['result'] = 'success'
        return HttpResponseRedirect('/')

    else:
        login_error = True
        return_dict['result'] = 'invalid'
        return HttpResponseRedirect('/user/login/')



def signup(request):
    return_dict = {}
    if request.method == 'POST':

        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        data = {'email': email, 'password2': password2, 'password1': password1}
        form = SignUpForm(data=data)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            print('User registred')
            # msg_html = render_to_string('email/register.html', {'login': email, 'password': password1})
            # send_mail('Регистрация на сайте LAKSHMI888', None, 'info@lakshmi888.ru', [email],
            #           fail_silently=False, html_message=msg_html)
            # print('Email sent to {} with pass {}'.format(email,password1))
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            error = 'Вы ввели не коректные данные'
            print(form.errors)
            return render(request, 'pages/register.html', locals())

