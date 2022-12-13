from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import telegram
import requests
from types import SimpleNamespace
from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def index(request):
    data = """
    [
        {
        "name": "Led Light Gloves",
        "description": "Waterproof LED Flashlight Gloves",
        "price": "15",
        "image": "gloves1.png",
        "id": "4"
        },
        {
        "name": "Led Light Gloves 2",
        "description": "Waterproof LED Flashlight Gloves",
        "price": "16",
        "image": "gloves2.png",
        "id": "4"
        },
        {
        "name": "Kaktus giesskanne",
        "description": "Eiene tolle Kaktus giesskanne",
        "price": "13",
        "image": "kanne.png",
        "id": "1"
        },
        {
        "name": "Air humidifier 1",
        "description": "Portable USB Air Humidifier For Essential Oil",
        "price": "25",
        "image": "card1.png",
        "id": "1"
        },
        {
        "name": "Air humidifier 2",
        "description": "Portable USB Air Humidifier For Essential Oil",
        "price": "26",
        "image": "card2.png",
        "id": "2"
        },
        {
        "name": "Air humidifier 3",
        "description": "Portable USB Air Humidifier For Essential Oil",
        "price": "27",
        "image": "card3.png",
        "id": "3"
        }
    ]
    """
    products = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    try:
        user = request.session['user']
    except:
        user = ""
    if(request.GET.get('showModal', '') and request.GET.get('item', '')):
        return render(request, 'index.html', { 'products': products, 'name': user, 'webName': "Purifee", 'showModal': 'True', 'item': str(request.GET.get('item', '')) })
    if(request.GET.get('orderConfirmedModal', '')):
        return render(request, 'index.html', { 'products': products, 'name': user, 'webName': "Purifee", 'orderConfirmedModal': 'True', 'item': str(request.GET.get('item', '')) })
    else:
        return render(request, 'index.html', { 'products': products, 'name': user, 'webName': "Purifee"})

def login(request):
    return render(request, 'login.html')

def logout(request):
    request.session['user'] = ''
    return redirect('../')

def receipt(request):
    return render(request, 'receipt.html')

def loginAPI(request):
    request.session['user'] = request.GET.get('username', '')
    print(request.GET.get('username', ''))
    return redirect('../')

def addToCart(request):
    try:
        request.session['cart_items'] += ""
    except:
        request.session['cart_items'] = ""
    if(request.session['cart_items'] != ""):
        request.session['cart_items'] += """,
        {
            "name": " """ + request.GET.get('name', '') + """ ",
            "description": " """ + request.GET.get('description', '') + """ ",
            "price": " """ + request.GET.get('price', '') + """ ",
            "image": " """ + request.GET.get('image', '') + """ "
        }"""
    else:
        request.session['cart_items'] = """[
        {
            "name": " """ + request.GET.get('name', '') + """ ",
            "description": " """ + request.GET.get('description', '') + """ ",
            "price": " """ + request.GET.get('price', '') + """ ",
            "image": " """ + request.GET.get('image', '') + """ "
        }"""
        print("F")
    return redirect('../?showModal=True&item=' + request.GET.get('name', ''))

def panel(request):
    request.session['cart_items'] = ""
    return redirect('/checkout')
    return render(request, 'panel.html')



def checkout(request):
    try:
        user = request.session['user']
    except:
        user = ""
    try:
        totalPrice = 0
        data = request.session['cart_items']
        products = json.loads(data + "\n]", object_hook=lambda d: SimpleNamespace(**d))
        for item in products:
            item.image = item.image[1:]
            totalPrice += float(item.price)
    except:
        products = ""
    return render(request, 'checkout.html', {'name': user, 'products': products, 'totalPrice': totalPrice})

def pay(request):
    email = request.GET.get('email', '')
    try:
        user = request.session['user']
    except:
        user = ""
    if(user == ""):
        alert = "You got a new order!"
    else:
        alert = f"You got a new order from {user}!"
    totalPrice = 0
    items = ""
    try:
        data = request.session['cart_items']
        products = json.loads(data + "\n]", object_hook=lambda d: SimpleNamespace(**d))
        for item in products:
            item.image = item.image[1:]
            totalPrice += float(item.price)
            items += "<img src='http://192.168.1.145/static/img/" + item.image + "'>\n" + item.name + "\n" + item.price + "€\n"
        context = {
            'name': user,
            'products': products,
            'totalPrice': totalPrice,
            'email': email
        }
        # Send telegram message
        TOKEN = "5687014560:AAF_Xn-KIBNGkS4tFjG_euT6LH_P-XPO7ho"
        chat_id = "2057074097"
        message = f"{alert}\n{items}\nTotal: {str(totalPrice)}€\n Email: {email}"
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
        print(requests.get(url).json())
        context = {
            'name': user,
            'products': products,
            'totalPrice': totalPrice,
            'email': email
        }
        html_message = render_to_string('mail_template.html', context)
        plain_message = strip_tags(html_message)
        subject = "Order confirmed!"
        mail.send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [email])
        return redirect('../?orderConfirmedModal=True')
        # return render(request, 'mail_template.html', context)
    except:
        return redirect('../')

    return redirect('../?orderConfirmedModal=True')

def item(request):
    print(request.GET.get('item', ''))
    return redirect('../')

def logout(request):
    request.session['user'] = ""
    return redirect('../')