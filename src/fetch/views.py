# -*- coding: utf-8 -*-

"""ИРП-с мэдээлэл татах"""

import base64
import copy

from django.core.files.base import ContentFile
from django.db import connection as conn
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.conf import settings

from src.core.shortcuts import (
    xstring, get_object_or_none, get_object_or_create)
from src.company.models import Company
from src.warehouse.models import Warehouse
from src.employee.models import Position, Employee
from src.customer.models import Customer
from src.product.models import (
    Category, MeasuringType, Form, Product, Price, Stock)
from src.customer.cart import Cart

from .connection import Connection


def home(request):
    """
    ИРП-с мэдээлэл татах линкүүдийг харуулах
    """
    return render(request, 'api/home.html')


def update_company(request):
    """
    Компанийн мэдээлэл татаж хадгалах

    Хэрэв компани үүссэн байвал хамгийн сүүлд засагдсан компанийн засагдсан огноог авна

    Эсвэл компани үүсээгүй бол "2017-01-01 00:00:00" авна
    """

    if Company.objects.first():
        v_date = Company.objects.first().updated_at.strftime('%Y-%m-%d %H:%M:%S')
    else:
        v_date = '2017-01-01 00:00:00'

    # Гараас татах огноо оруулах
    if request.GET.get('v_date', None):
        v_date = request.GET.get('v_date') + ' 00:00:00'

    connection = Connection.get_instance()
    response = connection.update_company_list(v_date)
    print(response.json())
    if response.json().get('status') == 'success':
        for com in response.json().get('data'):
            if Company.objects.filter(id=com.get('id')).exists():
                company = Company.objects.get(id=com.get('id'))
            else:
                company = Company(id=com.get('id'))
            company.flag = com.get('flag')
            company.partner_id = com.get('partner_id')
            company.name = com.get('name')
            company.save()
    return JsonResponse({'status': response.json().get('status')})


def update_warehouse(request):
    """
    Агуулахын мэдээлэл татаж хадгалах
    """
    for company in Company.objects.all():
        whouse = Warehouse.objects.filter(company=company).first()
        if whouse:
            v_date = whouse.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            v_date = '2017-01-01 00:00:00'

        # Гараас татах огноо оруулах
        if request.GET.get('v_date', None):
            v_date = request.GET.get('v_date') + ' 00:00:00'

        connection = Connection.get_instance()
        response = connection.update_warehouse(v_date, company.id)
        print(response.json())
        if response.json().get('status') == 'success':
            for whouse in response.json().get('data'):
                if Warehouse.objects.filter(id=whouse.get('id')).exists():
                    warehouse = Warehouse.objects.get(id=whouse.get('id'))
                else:
                    warehouse = Warehouse(id=whouse.get('id'), company=company)
                warehouse.flag = whouse.get('flag')
                warehouse.name = whouse.get('name')
                warehouse.save()

    return JsonResponse({'status': response.json().get('status')})


def update_position(request):
    if Position.objects.first():
        v_date = Position.objects.first().updated_at.strftime('%Y-%m-%d %H:%M:%S')
    else:
        v_date = '2010-01-01 00:00:00'

    print(v_date)

    # Гараас татах огноо оруулах
    if request.GET.get('v_date', None):
        v_date = request.GET.get('v_date') + ' 00:00:00'

    connection = Connection.get_instance()
    response = connection.update_position(v_date)
    print(response.json())
    if response.json().get('status') == 'success':
        positions = response.json().get('data')
        for position in positions:
            obj = get_object_or_create(Position, id=position.get('id'))
            obj.name = position.get('name')
            obj.flag = position.get('flag')
            obj.save()
    return JsonResponse({'status': response.json().get('status')})


def update_employee(request):
    for company in Company.objects.all():
        v_date = '2017-01-01 00:00:00'

        # Гараас татах огноо оруулах
        if request.GET.get('v_date', None):
            v_date = request.GET.get('v_date') + ' 00:00:00'

        connection = Connection.get_instance()
        response = connection.update_employee(v_date, company.id)
        print(response.json())
        if response.json().get('status') == 'success':
            employees = response.json().get('data')
            for employee in employees:
                obj = get_object_or_create(Employee, erp_id=employee['id'])
                obj.family_name = employee['family_name']
                obj.last_name = employee['last_name']
                obj.first_name = employee['first_name']
                obj.birth_date = employee['birthday']
                obj.register_no = employee['registration_no']
                obj.email = employee['email']
                obj.gender = employee.get('gender') if employee.get(
                    'gender') != '' else None
                obj.company = company
                if employee['position_id']:
                    if Position.objects.filter(id=employee['position_id']).exists():
                        obj.position = get_object_or_404(
                            Position, id=employee['position_id'])
                obj.flag = employee['flag']
                obj.save()
                if employee['branch_id']:
                    if Warehouse.objects.filter(id=employee['branch_id']).exists():
                        obj.warehouses.add(get_object_or_404(
                            Warehouse, id=employee['branch_id']))

    return JsonResponse({'status': response.json().get('status')})


def update_customer(request):
    """
    Бүх харилцагчийн мэдээлэл компаниар татаж хадгалах
    """
    v_date = '2017-01-01 00:00:00'

    # Гараас татах огноо оруулах
    if request.GET.get('v_date', None):
        v_date = request.GET.get('v_date') + ' 00:00:00'

    connection = Connection.get_instance()
    response = connection.update_customer(v_date)
    print(response.json())
    if response.json().get('status') == 'success':
        for cust in response.json().get('data'):
            customer = get_object_or_create(Customer, id=cust.get('id'))
            customer.parent = get_object_or_none(
                Customer, id=cust.get('parent_id'))
            customer.name = xstring(cust.get('name', None))
            customer.register_no = xstring(cust.get('ref', None))
            customer.phone = xstring(cust.get('phone', None))
            customer.email = xstring(cust.get('email', None))
            customer.fax = xstring(cust.get('fax', None))
            customer.addr_country = xstring(cust.get('country', None))
            customer.addr_city = xstring(cust.get('state', None))
            customer.addr_district = xstring(cust.get('state_wall', None))
            customer.addr_street = xstring(cust.get('street', None))
            customer.addr_street2 = xstring(cust.get('street2', None))
            customer.longitude = cust.get('longitude') if cust.get(
                'longitude') and cust.get(
                'longitude').isdecimal() else None
            customer.latitude = cust.get('latitude') if cust.get(
                'latitude') and cust.get(
                'latitude').isdecimal() else None
            customer.is_supplier = xstring(cust.get('supplier', None))
            customer.is_factory = xstring(cust.get('manufacturer', None))
            # customer.is_customer =
            customer.flag = cust.get('flag')
            customer.save()
    return JsonResponse({'status': response.json().get('status')})


def update_company_customer(request):
    """
    Харилцагчийн мэдээлэл компаниар татаж хадгалах
    """

    for company in Company.objects.all():
        custo = Customer.objects.filter(company=company).first()
        if custo:
            v_date = custo.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            v_date = '2017-01-01 00:00:00'

        # Гараас татах огноо оруулах
        if request.GET.get('v_date', None):
            v_date = request.GET.get('v_date') + ' 00:00:00'

        connection = Connection.get_instance()
        response = connection.update_company_customer(v_date, company.id)
        print(response.json())
        if response.json().get('status') == 'success':
            for cust in response.json().get('data'):
                customer = get_object_or_create(Customer, id=cust.get('id'))
                customer.company = company
                customer.parent = get_object_or_none(
                    Customer, id=cust.get('parent_id'))
                customer.name = xstring(cust.get('name', None))
                customer.register_no = xstring(cust.get('ref', None))
                customer.phone = xstring(cust.get('phone', None))
                customer.email = xstring(cust.get('email', None))
                customer.fax = xstring(cust.get('fax', None))
                customer.addr_country = xstring(cust.get('country', None))
                customer.addr_city = xstring(cust.get('state', None))
                customer.addr_district = xstring(cust.get('state_wall', None))
                customer.addr_street = xstring(cust.get('street', None))
                customer.addr_street2 = xstring(cust.get('street2', None))
                customer.longitude = cust.get('longitude') if cust.get(
                    'longitude').isdecimal() else None
                customer.latitude = cust.get('latitude') if cust.get(
                    'latitude').isdecimal() else None
                customer.is_supplier = xstring(cust.get('supplier', None))
                customer.is_factory = xstring(cust.get('manufacturer', None))
                # customer.is_customer =
                customer.flag = cust.get('flag')
                customer.save()
    return JsonResponse({'status': response.json().get('status')})


def update_product_category(request):
    """
    Бүтээгдэхүүний ангиллын татах
    """
    if Category.objects.last():
        v_date = Category.objects.first().updated_at.strftime('%Y-%m-%d %H:%M:%S')
    else:
        v_date = '2017-01-01 00:00:00'

    # Гараас татах огноо оруулах
    if request.GET.get('v_date', None):
        v_date = request.GET.get('v_date') + ' 00:00:00'

    connection = Connection.get_instance()
    response = connection.update_product_category(v_date)
    print(response.json())
    if response.json().get('status') == 'success':
        for pcategory in response.json().get('data'):
            if Category.objects.filter(id=pcategory.get('id', None)).exists():
                category = Category.objects.get(id=pcategory.get('id'))
            else:
                category = Category(id=pcategory.get('id'))

            if pcategory.get('parent_id'):
                category.parent = Category.objects.get(
                    id=pcategory.get('parent_id', None)[0])
            category.name = pcategory.get('name', None)
            category.flag = pcategory.get('flag', None)
            category.save()
    return JsonResponse({'status': response.json().get('status')})


def update_measuring_type(request):
    """
    Хэмжих нэгж
    """
    v_date = '2017-01-01 00:00:00'

    # Гараас татах огноо оруулах
    if request.GET.get('v_date', None):
        v_date = request.GET.get('v_date') + ' 00:00:00'

    connection = Connection.get_instance()
    response = connection.update_measuring_type(v_date)
    print(response.json())
    if response.json().get('status') == 'success':
        for measuring in response.json().get('data'):
            measuring_type = get_object_or_create(
                MeasuringType,
                id=xstring(measuring.get('id', None))
            )

            measuring_type.name = xstring(measuring.get('name', None))
            measuring_type.factor = measuring.get('factor', None)
            measuring_type.flag = xstring(measuring.get('flag', None))
            measuring_type.save()

    return JsonResponse({'status': 'success'})


def update_product_form(request):
    """
    Бүтээгдэхүүний хэлбэр
    """
    v_date = '2017-01-01 00:00:00'

    # Гараас татах огноо оруулах
    if request.GET.get('v_date', None):
        v_date = request.GET.get('v_date') + ' 00:00:00'

    connection = Connection.get_instance()
    response = connection.update_product_form(v_date)
    print(response.json())
    if response.json().get('status') == 'success':
        for form in response.json().get('data'):
            product_form = get_object_or_create(
                Form,
                id=xstring(form.get('id', None))
            )

            product_form.name = xstring(form.get('name', None))
            product_form.flag = xstring(form.get('flag', None))
            product_form.save()

    return JsonResponse({'status': 'success'})


def update_product(request):
    """
    Бүтээгдэхүүний мэдээлэл татаж хадгалах

    Хэрэв хамгийн сүүлд шинэчлэгдсэн бүтээгдэхүүн байвал сүүлд өөрчлөгдсөн
    огноог авна эсвэл 2017-01-01 авна
    """

    if Product.objects.order_by('-updated_at').first():
        v_date = Product.objects.order_by(
            '-updated_at').first().updated_at.strftime('%Y-%m-%d %H:%M:%S')
    else:
        v_date = '2000-01-01 00:00:00'

    # Гараас татах огноо оруулах
    if request.GET.get('v_date', None):
        v_date = request.GET.get('v_date') + ' 00:00:00'

    connection = Connection.get_instance()
    response = connection.update_product(v_date)

    if response.json().get('status') == 'success':
        for prod in response.json().get('data'):
            product = get_object_or_create(Product, id=prod.get('id'))
            product.category = Category.objects.get(id=prod.get('categ_id'))
            product.name = xstring(prod.get('name', None))
            product.eng_name = xstring(prod.get('eng_name', None))
            product.generic_name = xstring(prod.get('generic_name', None))
            product.internal_code = xstring(prod.get('internal_code', None))
            product.barcode = xstring(prod.get('barcode', None))
            product.seller = get_object_or_none(
                Customer,
                id=xstring(prod.get('seller_id', None))
            )
            product.manufacturer = get_object_or_none(
                Customer,
                id=xstring(prod.get('manufacturer_id', None))
            )
            product.measuring_type = get_object_or_none(
                MeasuringType,
                id=xstring(prod.get('uom_id', None))
            )
            product.form = get_object_or_none(
                Form,
                id=xstring(prod.get('form_id', None))
            )
            product.ingredients = xstring(prod.get('ingredients', None))
            product.volume = xstring(prod.get('volume', None))
            product.is_exclusive = prod.get('is_exclusive', None) != ''
            product.description = xstring(prod.get('description', None))
            product.instruction = xstring(prod.get('instruction', None))
            product.warning = xstring(prod.get('warning', None))
            product.flag = xstring(prod.get('flag', None))
            product.save()

            if xstring(prod.get('image', None)):
                imgstr = prod.get('image')
                image = ContentFile(base64.b64decode(imgstr))
                product.image.save('product.jpeg', image, save=True)

    return JsonResponse({'status': response.json().get('status')})


def update_product_price(request):
    """
    Бүтээгдэхүүний үнийн мэдээлэл татаж хадгалах

    Хэрэв хамгийн сүүлд шинэчлэгдсэн бүтээгдэхүүн байвал сүүлд өөрчлөгдсөн
    огноог авна эсвэл 2017-01-01 авна
    """

    cursor = conn.cursor()

    for company in Company.objects.all():
        for warehouse in company.warehouses.all():
            connection = Connection.get_instance()

            price = Price.objects.filter(
                company=company, warehouse=warehouse).first()
            if price:
                v_date = price.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            else:
                v_date = '2017-01-01 00:00:00'

            # Гараас татах огноо оруулах
            if request.GET.get('v_date', None):
                v_date = request.GET.get('v_date') + ' 00:00:00'

            response = connection.update_product_price(
                v_date, company.id, warehouse.id)

            print(response.json())
            prod_data = response.json().get('data')
            print(prod_data)
            prod_ids = tuple(prod_data.keys())
            cursor.execute(
                '''
                SELECT id, company_id, warehouse_id, product_id
                FROM product_price
                WHERE company_id={0} and warehouse_id={1} and product_id in {2}
                '''.format(company.id, warehouse.id, prod_ids)
            )
            rows = cursor.fetchall()
            exist_dict = {}
            for pid, cid, wid, ppd in rows:
                if cid not in exist_dict:
                    exist_dict[cid] = {}
                if wid not in exist_dict[cid]:
                    exist_dict[cid][wid] = {}
                if ppd not in exist_dict[cid][wid]:
                    exist_dict[cid][wid][ppd] = pid

            for key, item in prod_data.items():
                cost = 0
                price = item.get("price")
                if item.get('cost', None) != {}:
                    cost = next(iter(item.get('cost').values()))

                if Product.objects.filter(id=int(key)).exists():

                    if company.id in exist_dict and warehouse.id in exist_dict[company.id] \
                            and int(key) in exist_dict[company.id][warehouse.id]:
                        price_id = exist_dict[company.id][warehouse.id][int(
                            key)]
                        cursor.execute(
                            " \
                            UPDATE product_price \
                            SET price=%s, cost=%s, updated_at=NOW() \
                            WHERE id=%s \
                            " % (price, cost, price_id)
                        )
                    else:
                        cursor.execute(
                            '''
                            INSERT INTO product_price
                            (company_id, warehouse_id, product_id, price, cost, is_active, created_at, updated_at)
                            VALUES ({0}, {1}, {2}, {3}, {4}, TRUE, NOW(), NOW())
                            '''.format(company.id, warehouse.id, key, price, cost)
                        )

    return JsonResponse({'status': response.json().get('status')})


def update_product_stock(request):
    """
    Бүтээгдэхүүний үлдэгдэл татаж хадгалах

    Хэрэв хамгийн сүүлд шинэчлэгдсэн бүтээгдэхүүн байвал сүүлд өөрчлөгдсөн
    огноог авна эсвэл 2017-01-01 авна
    """
    v_date = '2019-07-01 00:00:00'

    # Гараас татах огноо оруулах
    if request.GET.get('v_date', None):
        v_date = request.GET.get('v_date') + ' 00:00:00'

    for warehouse in Warehouse.objects.all():
        if Stock.objects.filter(warehouse=warehouse).first():
            v_date = Stock.objects.filter(warehouse=warehouse).first(
            ).updated_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            v_date = '2019-07-01 00:00:00'

        connection = Connection.get_instance()
        response = connection.update_product_stock(v_date, warehouse.id)

        stock_data = response.json().get('data')
        prod_list = list(map(lambda x: x['prod_id'], stock_data))

        Stock.objects.filter(warehouse=warehouse).exclude(
            product__id__in=prod_list).update(in_stock=0)

        if response.json().get('status') == 'success':
            for stck in response.json().get('data'):
                stock = get_object_or_create(
                    Stock,
                    warehouse=warehouse,
                    product=Product.objects.get(
                        id=xstring(stck.get('prod_id', None))
                    )
                )
                expiration_date = xstring(stck.get('expiration_date', None))
                if expiration_date:
                    expiration_date = parse_datetime(expiration_date)

                stock.lot_name = xstring(stck.get('lot_name', None))
                stock.in_stock = xstring(stck.get('in_stock', None))
                stock.expiration_date = expiration_date
                stock.flag = xstring(stck.get('flag', None))
                stock.save()
    return JsonResponse({'status': response.json().get('status')})


def order(request):
    """
    Захиалгын мэдээлэл татаж хадгалах
    """

    order = {}
    warehouse_id = request.session[settings.WAREHOUSE_SESSION_ID]
    warehouse = get_object_or_404(Warehouse, pk=warehouse_id)
    seller = warehouse.company.employees.filter(user__isnull=False).first()

    cart = Cart(request)
    products = copy.deepcopy(cart.order)
    product_list = [item for item in products.values()]
    for product in product_list:
        p = get_object_or_404(Product, pk=product['id'])
        product['prod_id'] = product.pop('id')
        product['prod_price'] = product.pop('price')
        product['reduced_price'] = product.pop('discounted_price')
        product['uom_id'] = p.measuring_type.id
        product['expire_range_id'] = ''
        del product['category']
        del product['manufacturer']
        del product['seller']
        del product['name']
        del product['image']
        del product['stock']
        del product['measuring_type']
        del product['form']
        del product['discount']
        del product['total']

    order['seller_emp_id'] = seller.id
    order['customer_org_id'] = request.user.customer.id
    order['company_id'] = warehouse.company.id
    order['sales_type'] = 'credit'
    order['prod_list'] = product_list
    order['crm_order_id'] = 1
    order['no_tax'] = 0
    order['vat_bill_id'] = ''
    order['vat_qr_data'] = ''
    order['vat_bill_type'] = ''
    order['vat_tax_type'] = ''

    connection = Connection.get_instance()
    response = connection.order(order)
    print(response)
    print(response.json())
    return JsonResponse(response.json())


def update_company_warehouse_product_price(request, company_id, warehouse_id):
    connection = Connection.get_instance()
    cursor = conn.cursor()
    company = get_object_or_404(Company, id=company_id)
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)
    price = Price.objects.filter(
        company=company, warehouse=warehouse).first()
    if price:
        v_date = price.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    else:
        v_date = '2017-01-01 00:00:00'

    # Гараас татах огноо оруулах
    if request.GET.get('v_date', None):
        v_date = request.GET.get('v_date') + ' 00:00:00'

    response = connection.update_product_price(
        v_date, company.id, warehouse.id)

    print(response.json())
    prod_data = response.json().get('data')
    print(prod_data)
    prod_ids = tuple(prod_data.keys())
    cursor.execute(
        '''
        SELECT id, company_id, warehouse_id, product_id
        FROM product_price
        WHERE company_id={0} and warehouse_id={1} and product_id in {2}
        '''.format(company.id, warehouse.id, prod_ids)
    )
    rows = cursor.fetchall()
    exist_dict = {}
    for pid, cid, wid, ppd in rows:
        if cid not in exist_dict:
            exist_dict[cid] = {}
        if wid not in exist_dict[cid]:
            exist_dict[cid][wid] = {}
        if ppd not in exist_dict[cid][wid]:
            exist_dict[cid][wid][ppd] = pid

    for key, item in prod_data.items():
        cost = 0
        price = item.get("price")
        if item.get('cost', None) != {}:
            cost = next(iter(item.get('cost').values()))

        if Product.objects.filter(id=int(key)).exists():

            if company.id in exist_dict and warehouse.id in exist_dict[company.id] \
                    and int(key) in exist_dict[company.id][warehouse.id]:
                price_id = exist_dict[company.id][warehouse.id][int(
                    key)]
                cursor.execute(
                    " \
                    UPDATE product_price \
                    SET price=%s, cost=%s, updated_at=NOW() \
                    WHERE id=%s \
                    " % (price, cost, price_id)
                )
            else:
                cursor.execute(
                    '''
                    INSERT INTO product_price
                    (company_id, warehouse_id, product_id, price, cost, is_active, created_at, updated_at)
                    VALUES ({0}, {1}, {2}, {3}, {4}, TRUE, NOW(), NOW())
                    '''.format(company.id, warehouse.id, key, price, cost)
                )

    return JsonResponse({'status': response.json().get('status')})


def update_company_warehouse_product_stock(request, warehouse_id):
    """
    Бүтээгдэхүүний үлдэгдэл татаж хадгалах

    Хэрэв хамгийн сүүлд шинэчлэгдсэн бүтээгдэхүүн байвал сүүлд өөрчлөгдсөн
    огноог авна эсвэл 2017-01-01 авна
    """
    v_date = '2019-07-01 00:00:00'

    warehouse = get_object_or_404(Warehouse, pk=warehouse_id)
    if Stock.objects.filter(warehouse=warehouse).first():
        v_date = Stock.objects.filter(warehouse=warehouse).first(
        ).updated_at.strftime('%Y-%m-%d %H:%M:%S')
    else:
        v_date = '2019-07-01 00:00:00'

    # Гараас татах огноо оруулах
    if request.GET.get('v_date', None):
        v_date = request.GET.get('v_date') + ' 00:00:00'

    print(v_date)

    connection = Connection.get_instance()
    response = connection.update_product_stock(v_date, warehouse.id)

    if response.json().get('status') == 'success':
        for stck in response.json().get('data'):
            stock = get_object_or_create(
                Stock,
                warehouse=warehouse,
                product=Product.objects.get(
                    id=xstring(stck.get('prod_id', None))
                )
            )
            expiration_date = xstring(stck.get('expiration_date', None))
            if expiration_date:
                expiration_date = parse_datetime(expiration_date)

            stock.lot_name = xstring(stck.get('lot_name', None))
            stock.in_stock = xstring(stck.get('in_stock', None))
            stock.expiration_date = expiration_date
            stock.flag = xstring(stck.get('flag', None))
            stock.save()
    return JsonResponse({'status': response.json().get('status')})
