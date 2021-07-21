# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import connection
# from django.shortcuts import get_object_or_404


# from src.warehouse.models import Warehouse
# from src.product.models import Category
from src.customer.cart import Cart


def categories(request):
    if hasattr(request.user, 'customer'):
        warehouse_id = request.session[settings.WAREHOUSE_SESSION_ID]

        cursor = connection.cursor()
        cursor.execute('''
            SELECT pc.id, pc.name FROM product_category AS pc
            INNER JOIN product_product AS p ON pc.id=p.category_id
            INNER JOIN product_price AS pp ON p.id=pp.product_id
            INNER JOIN product_stock AS ps ON p.id=ps.product_id
            WHERE pp.warehouse_id={0}
            AND ps.warehouse_id={0}
            AND pc.parent_id IS NULL
            GROUP BY pc.id;
        '''.format(warehouse_id))
        parent_result = cursor.fetchall()

        categories_dict = {}

        for category_id, name in parent_result:
            categories_dict[category_id] = {'id': category_id, 'name': name}
            cursor.execute('''
                SELECT pc.id, pc.name FROM product_category AS pc
                INNER JOIN product_product AS p ON pc.id=p.category_id
                INNER JOIN product_price AS pp ON p.id=pp.product_id
                INNER JOIN product_stock AS ps ON p.id=ps.product_id
                WHERE pp.warehouse_id={0}
                AND ps.warehouse_id={0}
                AND pc.parent_id={1}
                GROUP BY pc.id;
            '''.format(warehouse_id, category_id))
            child_result = cursor.fetchall()
            if not len(child_result) is 0:
                categories_dict[category_id]['sub_categories'] = dict(
                    child_result)
        return {'categories': categories_dict}
    return {}


def cart(request):
    if hasattr(request.user, 'customer'):
        return {'cart': Cart(request)}
    return {}
