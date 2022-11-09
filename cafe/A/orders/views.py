from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import MenuItem, Order, Table, Receipt
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
import json
from suds.client import Client
import requests


class OrderView(LoginRequiredMixin, View):
    def get(self, request):
        total_price = 0
        total_price_without_discount = 0
        counter = 0
        orders = []
        receipt = Receipt.objects.first()
        table = request.session['table']
        table = Table.objects.filter(id=table).first()
        for k, v in request.session.items():
            item = MenuItem.objects.filter(slug=k).first()
            if item:
                counter += 1
                total_price += ((item.price * (100 - item.discount)) / 100) * int(v)
                total_price_without_discount += item.price * int(v)
                orders.append(
                    Order(tables=table, number=int(v), status=False, users=request.user, menu_items=item,
                          receipts=receipt))
        final_discount = total_price_without_discount - total_price
        request.session['total_price'] = total_price
        request.session['total_price_without_discount'] = total_price_without_discount
        for order in orders:
            print(order.menu_items.image.url)
        return render(request, 'orders/orders.html', {'orders': orders,
                                                      'total_price': total_price,
                                                      'counter': counter, 'table': table,
                                                      'final_discount': final_discount})


class MenuView(LoginRequiredMixin, View):
    def get(self, request):
        menu_items = MenuItem.objects.filter()
        tables = Table.objects.filter()
        list_of_category = list(set([item.category for item in menu_items]))

        req = request.session.items()
        items = []
        count = []
        for k, v in req:
            item = MenuItem.objects.filter(slug=k).first()
            if item:
                items.append(item)
                count.append(v)
        pack = zip(items, count)
        price = []
        for j in menu_items:
            price.append(j.price * (100 - j.discount) / 100)
        pack2 = zip(menu_items, price)
        return render(request, 'orders/menu.html',
                      {'tables': tables, 'menu_items': menu_items, 'list_of_category': list_of_category,
                       'pack': pack})


class SetSessionView(View):
    def post(self, request):
        res = json.load(request)

        for k, v in res.items():
            request.session[k.replace('_', ' ')] = v
        return HttpResponse({"error": ""}, status=400)


class DelSessionView(View):
    def post(self, request):
        res = list(request.POST.dict().keys())[0]
        del request.session[res.replace('_', ' ')]
        return HttpResponse({"error": ""}, status=400)


class DownSessionView(View):
    def post(self, request):
        response = list(request.POST.dict().keys())[0]
        request.session[response.replace('_', ' ')] = str(int(request.session[response.replace('_', ' ')]) - 1)
        return HttpResponse({"error": ""}, status=400)


class UpSessionView(View):
    def post(self, request):
        response = list(request.POST.dict().keys())[0]
        request.session[response.replace('_', ' ')] = str(int(request.session[response.replace('_', ' ')]) + 1)
        return HttpResponse({"error": ""}, status=400)


class TableSessionView(View):
    def post(self, request):
        print(request)
        print(request.session.items())
        try:
            return HttpResponse(request.session['table'])
        except Exception as e:
            messages.info(request, """You didn"t select a table. Please select one.""", 'info')
            return HttpResponse({"error": ""}, status=400)


# MMERCHANT_ID = '41b3a452-5a8c-4f34-86d8-84ba6e87413d'  # Required
MERCHANT = '41b3a452-5a8c-4f34-86d8-84ba6e87413d'  # Required
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
# amount = 11000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# email = 'email@example.com'  # Optional
# mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
# to session ha 127.0.0.1:8000 ine inja ham ja localhost ino beza
CallbackURL = 'http://127.0.0.1:8000/orders/verify/'


class RequestView(View):
    def get(self, request):
        req_data = {
            "merchant_id": MERCHANT,
            "amount": int(request.session['total_price']),
            "callback_url": CallbackURL,
            "description": description,
            "metadata": {"mobile": request.user.phone_number, "email": request.user.email}
        }
        req_header = {"accept": "application/json", "content-type": "application/json'"}
        req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
            req_data), headers=req_header)
        # code etebariye zarinpal
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=str(authority)))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


class VerifyView(View):
    def get(self, request):
        t_authority = request.GET['Authority']
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json",
                          "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": int(request.session['total_price']),
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    messages.info(request, """Payment was successful. Your order is being processed.""", 'success')

                    receipt = Receipt(total_price=request.session['total_price_without_discount'],
                                      final_price=request.session['total_price'],
                                      users=request.user)
                    req = request.session.items()
                    lst = []
                    table_id = request.session["table"]
                    tables = Table.objects.get(id=table_id)
                    tables.use = True
                    receipt.save()
                    tables.save()
                    for k, v in req:
                        item = MenuItem.objects.filter(slug=k).first()
                        if item:
                            order = Order(tables=tables, number=int(v), status=True, users=request.user,
                                          menu_items=item,
                                          receipts=receipt)
                            order.save()
                            lst.append(k)

                    # Clearing session memory
                    for i in lst:
                        del request.session[i]

                    del request.session['total_price']
                    del request.session['total_price_without_discount']

                    return redirect('accounts:user_profile')
                elif t_status == 101:
                    # tekrari
                    return HttpResponse('Transaction submitted : ' + str(
                        req.json()['data']['message']
                    ))
                else:
                    # na movafagh
                    return HttpResponse('Transaction failed.\nStatus: ' + str(
                        req.json()['data']['message']
                    ))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
        else:
            return HttpResponse('Transaction failed or canceled by user')
