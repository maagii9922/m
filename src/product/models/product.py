# -*- coding:utf-8 -*-

"""
Бүтээгдэхүүн
"""
from datetime import datetime

from django.conf import settings
from django.db import models, connection

from src.core import constant as const
from src.customer.models import Customer
from src.product.models import Category, MeasuringType, Form

# from src.promotion.models import Promotion


class Product(models.Model):
    """
    Бүтээгдэхүүн
    """

    category = models.ForeignKey(
        Category,
        verbose_name="Ангилал",
        on_delete=models.CASCADE,
        related_name="products",
    )
    name = models.CharField(verbose_name="Нэр", max_length=512)
    eng_name = models.CharField(
        verbose_name="Англи нэр", max_length=512, null=True, blank=True
    )
    generic_name = models.CharField(
        verbose_name="Олон улсын нэршил", max_length=512, null=True, blank=True
    )
    internal_code = models.CharField(
        verbose_name="Дотоод код", max_length=64, null=True, blank=True
    )
    barcode = models.CharField(
        verbose_name="Баркод", max_length=64, null=True, blank=True
    )
    seller = models.ForeignKey(
        Customer,
        verbose_name="Борлуулагч",
        on_delete=models.CASCADE,
        related_name="seller_products",
        null=True,
        blank=True,
    )
    manufacturer = models.ForeignKey(
        Customer,
        verbose_name="Үйлдвэрлэгч",
        on_delete=models.CASCADE,
        related_name="manufacturer_products",
        null=True,
        blank=True,
    )
    measuring_type = models.ForeignKey(
        MeasuringType,
        verbose_name="Хэмжих нэгж",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    form = models.ForeignKey(
        Form, verbose_name="Хэлбэр", on_delete=models.CASCADE, null=True, blank=True
    )
    image = models.ImageField(
        verbose_name="Зураг", upload_to="product/", null=True, blank=True
    )
    volume = models.CharField(
        verbose_name="Эзлэхүүн", max_length=512, null=True, blank=True
    )
    is_exclusive = models.BooleanField(verbose_name="Is exclusive", default=False)
    description = models.TextField(verbose_name="Тайлбар", null=True, blank=True)
    ingredients = models.TextField(
        verbose_name="Орц", max_length=512, null=True, blank=True
    )
    instruction = models.TextField(verbose_name="Заавар", null=True, blank=True)
    warning = models.TextField(verbose_name="Анхааруулга", null=True, blank=True)
    flag = models.IntegerField(verbose_name="Флаг")
    is_active = models.BooleanField(verbose_name="Идэвхитэй", default=True)
    created_at = models.DateTimeField(verbose_name="Үүссэн огноо", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Зассан огноо", auto_now=True)

    class Meta:
        ordering = ["name", "id"]
        verbose_name = "Бүтээгдэхүүн"
        verbose_name_plural = "Бүтээгдэхүүнүүд"

    def __str__(self):
        return "[{0}] {1}".format(self.internal_code, self.name)

    def get_promotion(self, request, warehouse_id, price, quantity=1):
        seller_id = self.seller.id if self.seller else "null"

        if hasattr(request.user, "customer"):

            customer = request.user.customer
            customer_category = customer.customer_category

            customer_id = customer.id

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
                    customer_category_id, customer_id, warehouse_id, self.id, seller_id
                )
            )
            response = cursor.fetchall()

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
        return discount, discounted_price

    def get_promotion_text(self, request, warehouse):
        # Тухайн хэрэглэгчийн акц, багцийн урамшууллын мэдээлэл татах
        with connection.cursor() as cr:
            text = ""
            customer = request.user.customer
            customer_category = customer.customer_category
            customer_id = customer.id
            warehouse_id = warehouse.id

            if not customer_category:
                customer_category_id = "Null"
            else:
                customer_category_id = customer_category.id

            cr.execute(
                """
                SELECT p.id, p.promotion_type, p.quantity, p.percent FROM promotion_promotion p
                LEFT JOIN promotion_promotion_customer_categories cc
                ON p.id=cc.promotion_id
                LEFT JOIN promotion_promotion_customers c
                ON p.id=c.promotion_id
                LEFT JOIN promotion_promotion_warehouses w
                ON p.id=w.promotion_id
                LEFT JOIN promotion_promotionproduct pp
                ON p.id = pp.promotion_id
                WHERE p.promotion_type IN (2, 4) 
                AND pp.is_not_bonus = TRUE
                AND pp.product_id = {3}
                AND p.start_date < NOW() AND p.end_date > NOW()
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
                ) ORDER BY p.order ASC LIMIT 1
                """.format(
                    customer_category_id, customer_id, warehouse_id, self.id
                )
            )
            promotion_id = cr.fetchone()
            if promotion_id:
                cr.execute(
                    """
                    SELECT p.name, pp.quantity, pp.is_not_bonus 
                    FROM promotion_promotionproduct pp
                    INNER JOIN product_product p
                    ON p.id = pp.product_id
                    WHERE pp.promotion_id = {0}
                    """.format(
                        promotion_id[0]
                    )
                )
                rows = cr.fetchall()
                if promotion_id[1] == 2:
                    if promotion_id[2]:
                        products = list(map(lambda x: x[0], rows))
                        text = ", ".join(products)
                        text += " бүтээгдэхүүнүүдээс нийт %sш авбал %s% хямдарна." % (
                            promotion_id[2],
                            promotion_id[3],
                        )
                    else:
                        products = list(
                            map(lambda x: x[0] + "-с " + str(x[1]) + "ш", rows)
                        )
                        text = ", ".join(products)
                        text += " авбал %s% хямдарна."
                elif promotion_id[1] == 4:
                    buy_products = list(filter(lambda x: x[2] == True, rows))
                    buy_products = list(
                        map(lambda x: x[0] + "-с " + str(x[1]) + "ш", buy_products)
                    )
                    buy_text = ", ".join(buy_products) + " авбал."
                    bonus_products = list(filter(lambda x: x[2] == False, rows))
                    bonus_products = list(
                        map(lambda x: x[0] + "-с " + str(x[1]) + "ш", bonus_products)
                    )
                    bonus_text = ", ".join(bonus_products) + " өгнө."
                    text = buy_text + bonus_text
            return text
