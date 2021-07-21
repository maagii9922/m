# -*- coding: utf-8 -*-

import copy
from decimal import Decimal
from collections import OrderedDict

from django.conf import settings
from django.db import connection
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

from src.core import constant as const
from src.warehouse.models import Warehouse
from src.product.models import Product, Stock
from src.promotion.models import Promotion


class Cart(object):
    def __init__(self, request):
        self.request = request
        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

        warehouse_id = self.session.get(settings.WAREHOUSE_SESSION_ID)
        if warehouse_id:
            self.warehouse = get_object_or_404(Warehouse, pk=warehouse_id)

        self.order = copy.deepcopy(self.cart)
        self.get_update_order()
        self.get_package_promotion()

        self.check_order = self.get_check_order()

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0}
        if quantity == 0:
            self.cart[product_id]["quantity"] = 1
        if quantity > 0:
            if update_quantity:
                self.cart[product_id]["quantity"] = int(quantity)
            else:
                self.cart[product_id]["quantity"] += int(quantity)
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        order = OrderedDict(sorted(self.order.items(), key=lambda x: x[1]["name"]))
        for item in order.values():
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        self.get_update_order()
        self.get_package_promotion()
        return int(
            sum(
                Decimal(item["discounted_price"]) * item["quantity"]
                for item in self.order.values()
            )
        )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_product(self, product_id):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT p.id, pc.name, pm.name, ps.name, p.name, p.image, st.in_stock,
            pr.price, mt.name, pf.name
            FROM product_product as p
            LEFT JOIN product_category as pc ON pc.id = p.category_id
            LEFT JOIN customer_customer as pm ON pm.id = p.manufacturer_id
            LEFT JOIN customer_customer as ps ON ps.id = p.seller_id
            LEFT JOIN product_measuringtype as mt ON mt.id = p.measuring_type_id
            LEFT JOIN product_form as pf ON pf.id = p.form_id
            INNER JOIN product_stock AS st ON p.id=st.product_id
            INNER JOIN product_price AS pr ON p.id=pr.product_id
            WHERE p.id={1} and pr.warehouse_id={0} and st.warehouse_id={0}
            """.format(
                self.warehouse.id, product_id
            )
        )
        rows = cursor.fetchone()

        fields = [
            "id",
            "category",
            "manufacturer",
            "seller",
            "name",
            "image",
            "stock",
            "price",
            "measuring_type",
            "form",
        ]

        product = {}
        for count, field in enumerate(fields):
            val = rows[count]
            if field == "image":
                if val == "":
                    val = "https://via.placeholder.com/500"
                else:
                    val = "/media/" + val
            product[field] = val

        return product

    def get_promotions(self):
        if hasattr(self.request.user, "customer"):

            customer = self.request.user.customer
            now = timezone.now()

            promotions = Promotion.objects.filter(
                Q(implement_type=1)
                | Q(
                    implement_type=2,
                    customer_categories=customer.customer_category,
                    is_implement=True,
                )
                | Q(
                    ~Q(customer_categories=customer.customer_category),
                    implement_type=2,
                    is_implement=False,
                )
                | Q(customers=customer, implement_type=3, is_implement=True)
                | Q(~Q(customers=customer), implement_type=3, is_implement=False)
                | Q(warehouses=self.warehouse, implement_type=4, is_implement=True)
                | Q(
                    ~Q(warehouses=self.warehouse), implement_type=4, is_implement=False
                ),
                start_date__lte=now,
                end_date__gte=now,
                is_active=True,
            )
            return promotions

    def get_product_promotion(self, product_id, price, quantity):
        pduct = Product.objects.get(id=product_id)
        if hasattr(pduct, "seller") and pduct.seller:
            seller_id = pduct.seller.id
        else:
            seller_id = 1

        if hasattr(self.request.user, "customer"):

            customer = self.request.user.customer
            customer_category = customer.customer_category

            customer_id = customer.id
            warehouse_id = self.warehouse.id

            if not customer_category:
                customer_category_id = "Null"
            else:
                customer_category_id = customer_category.id

            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT p.above_the_price, p.promotion_implement_type, p.percent, p.price, p.above_the_number, product.seller_id, product.seller_id
                FROM promotion_promotion AS p
                LEFT JOIN promotion_promotion_customer_categories AS cc
                ON p.id=cc.promotion_id
                LEFT JOIN promotion_promotion_customers AS c
                ON p.id=c.promotion_id
                LEFT JOIN promotion_promotion_warehouses AS w
                ON p.id=w.promotion_id
                LEFT JOIN promotion_promotion_products AS pp
                ON p.id=pp.promotion_id
                LEFT JOIN product_product AS product
                ON pp.product_id=product.id
                WHERE p.is_active=TRUE
                AND p.start_date<=NOW()
                AND p.end_date>=NOW()
                AND (p.implement_type=1
                    OR (p.implement_type=2
                        AND p.is_implement=TRUE
                        AND cc.customercategory_id={0})
                    OR (p.implement_type=3
                        AND p.is_implement=TRUE AND
                        c.customer_id={1})
                    OR (p.implement_type=4
                        AND p.is_implement=TRUE AND
                        w.warehouse_id={2})
                    OR (p.implement_type=2
                        AND p.is_implement=FALSE
                        AND cc.customercategory_id!={0}
                        AND p.id NOT IN (SELECT DISTINCT promotion_id
                                        FROM promotion_promotion_customer_categories cc
                                        WHERE cc.customercategory_id={0}))
                    OR (p.implement_type=3
                        AND p.is_implement=FALSE 
                        AND c.customer_id!={1}
                        AND p.id NOT IN (SELECT DISTINCT promotion_id
                                        FROM promotion_promotion_customers c
                                        WHERE c.customer_id={1}))
                    OR (p.implement_type=4
                        AND p.is_implement=FALSE
                        AND w.warehouse_id!={2}
                        AND p.id NOT IN (SELECT DISTINCT promotion_id
                                        FROM promotion_promotion_warehouses w
                                        WHERE w.warehouse_id={2}))
                )
                AND ((p.product_type=1 AND p.promotion_type=1)
                    OR (p.product_type=2 AND pp.product_id={3} AND p.promotion_type=1)
                    OR (p.product_type=3 
                        AND pp.product_id!={3}
                        AND p.promotion_type=1
                        AND p.id NOT IN (SELECT DISTINCT promotion_id
                                        FROM promotion_promotion_products pp
                                        WHERE pp.product_id={3})
                    )
                    OR (p.product_type=1 
                        AND p.promotion_type=3 
                        AND p.supplier_id={4})
                    OR (p.product_type=2
                        AND p.promotion_type=3 
                        AND product.id={3}
                        AND p.supplier_id={4})
                    OR (p.product_type=3
                        AND p.promotion_type=3 
                        AND p.supplier_id={4}
                        AND product.id!={3}
                        AND p.id NOT IN (SELECT DISTINCT promotion_id
                                        FROM promotion_promotion_products pp
                                        WHERE pp.product_id={3})
                        )
                ) ORDER BY p.order
            """.format(
                    customer_category_id,
                    customer_id,
                    warehouse_id,
                    product_id,
                    seller_id,
                )
            )
            response = cursor.fetchall()
            print(response)

        promotions = (
            response  # Бүтээгдэхүүнд хэрэгжих боломжтой бүх урамшууллыг авчирсан
        )

        discount = 0  # Бүтээгдэхүүний анхны хямдарлын үнэ
        discounted_price = price  # Хямдарсан үнийг анхны үнээр зарлаж байна
        for (
            above_the_price,
            promotion_implement_type,
            percent,
            promotion_price,
            above_the_number,
            seller_id,
            seller,
        ) in promotions:
            if above_the_price:  # Үнийн дүнгээс дээш нөхцөл байвал
                if (
                    price * quantity > above_the_price
                ):  # Бүтээгдэхүүний нийт дүн үнийн дүнгээс дээш дүнгээс илүү байвал
                    # Урамшууллын төрөл хувь байвал
                    if (
                        promotion_implement_type
                        == const.PROMOTION_IMPLEMENT_TYPE_PERCENT
                    ):
                        discount = "{}%".format(percent)
                        discounted_price = price * (100 - percent) / 100
                    # Урамшууллын төрөл үнээр байвал
                    elif (
                        promotion_implement_type == const.PROMOTION_IMPLEMENT_TYPE_PRICE
                    ):
                        discount = "{}₮".format(price)
                        discounted_price = price - promotion_price
                    # Урамшуулал тооноос дээш байвал
                    elif (
                        promotion_implement_type
                        == const.PROMOTION_IMPLEMENT_TYPE_ABOVE_THE_NUMBER
                    ):
                        if quantity >= above_the_number:
                            discount = "{}%".format(percent)
                            discounted_price = price * (100 - percent) / 100
            else:
                # Урамшууллын төрөл хувь байвал
                if promotion_implement_type == const.PROMOTION_IMPLEMENT_TYPE_PERCENT:
                    discount = "{}%".format(percent)
                    discounted_price = price * (100 - percent) / 100
                # Урамшууллын төрөл үнээр байвал
                elif promotion_implement_type == const.PROMOTION_IMPLEMENT_TYPE_PRICE:
                    discount = "{}₮".format(price)
                    discounted_price = price - promotion_price
                # Урамшуулал тооноос дээш байвал
                elif (
                    promotion_implement_type
                    == const.PROMOTION_IMPLEMENT_TYPE_ABOVE_THE_NUMBER
                ):
                    if quantity >= above_the_number:
                        discount = "{}%".format(percent)
                        discounted_price = price * (100 - percent) / 100
            # if discounted_price != price:
            break
        return {
            "discount": discount,
            "discounted_price": discounted_price,
            "is_package": False,
        }

    def get_update_order(self):
        for key, item in self.order.items():
            product_dict = self.get_product(int(key))
            item.update(product_dict)
            price = item["price"]
            quantity = item["quantity"]
            discount_dict = self.get_product_promotion(int(key), price, quantity)
            item.update(discount_dict)
            item["total"] = item["quantity"] * item["discounted_price"]
            if item["stock"] < item["quantity"]:
                item["check_order"] = True

    def get_package_promotion(self):
        # Харилцагчид хэрэгжих боломжтэй багцийн урамшуулал шүүж авна
        promotions = self.get_promotions().filter(
            promotion_type=const.PROMOTION_TYPE_PACKAGE, is_active=True
        )

        # Багцийн урамшууллыг давтана
        for promotion in promotions:
            is_implement = True  # Урамшуулал хэрэгжих эсхийг тодорхойлно
            products = promotion.promotion_products.values(
                "product_id", "quantity"
            )  # Урамшууллын багцад хамаарсан бүтээгдэхүүн сонгоно

            all_quantity = 0

            # Багцад хамаарсан бүтээгдэхүүнээр давтана
            for product in products:

                product_id = str(product["product_id"])

                # Хэрэв багцийн бүтээгдэхүүн сагсанд байхгүй бол урамшуулал хэрэгжихгүй
                if not product_id in self.order:
                    is_implement = False
                    break

                # Хэрэв багцийн бүтээгдэхүүн сагсанд байвал тус бүрийн тоо
                # хэмжээ багцийн тоо хэмжээнээс их багын шалгана
                elif (
                    not promotion.quantity
                    and self.order[product_id]["quantity"] < product["quantity"]
                ):
                    is_implement = False
                    break

                if product_id in self.order:
                    all_quantity = all_quantity + self.order[product_id]["quantity"]

            if promotion.quantity and promotion.quantity > all_quantity:
                is_implement = False

            if is_implement:
                percent = promotion.percent
                for product in products:
                    product_id = str(product["product_id"])
                    prod = self.order[product_id]
                    if prod["is_package"]:
                        continue
                    prod["is_package"] = True
                    prod["discount_package"] = "{}%".format(percent)
                    prod["discounted_price"] = (
                        prod.pop("discounted_price") * (100 - percent) / 100
                    )
                    prod["total"] = prod["discounted_price"] * prod["quantity"]
                break

    def get_acc_promotion_products(self):
        promotions = self.get_promotions().filter(
            promotion_type=const.PROMOTION_TYPE_ACC
        )
        for promotion in promotions:
            is_implement = True
            products = promotion.promotion_products.filter(is_not_bonus=True).values(
                "product_id", "quantity"
            )
            for product in products:
                product_id = str(product["product_id"])
                if not product_id in self.order:
                    is_implement = False
                    break
                elif self.order[product_id]["quantity"] < product["quantity"]:
                    is_implement = False
                    break

            if is_implement:
                promotion_products = promotion.promotion_products.filter(
                    is_not_bonus=False
                )
                for promotion_product in promotion_products:
                    yield promotion_product

    def get_check_order(self):
        for product_id, item in self.order.items():
            stock = get_object_or_404(
                Stock, warehouse=self.warehouse, product_id=product_id
            )
            if stock.in_stock < item["quantity"]:
                return True
        return False
