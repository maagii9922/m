# -*- coding:utf-8 -*-

"""
Customer Product View
"""

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage
from django.db import connection
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.html import strip_tags, mark_safe

from src.core import constant as const
from src.warehouse.models import Warehouse
from src.customer.models import Customer
from src.product.models import Product, Price, Stock

from src.customer.forms import CartQuantityForm
from src.customer.cart import Cart
from .core import TemplateView, ListView, DetailView


__all__ = ["Products", "ProductDetail", "ProductQuickView"]


class Products(TemplateView):
    template_name = "customer/product/list.html"

    def get_context_data(self, **kwargs):
        context = super(Products, self).get_context_data(**kwargs)
        warehouse_id = self.request.session[settings.WAREHOUSE_SESSION_ID]

        condition = "ps.warehouse_id = {0} AND pp.warehouse_id = {0}".format(
            warehouse_id
        )

        # Ангиллаар шүүх
        if "category_id" in self.kwargs:
            condition = condition + " AND pcat.id = {0}".format(
                self.kwargs.get("category_id")
            )

        # Хайлтын формоор шүүх
        if "search" in self.request.GET:
            search = self.request.GET.get("search")
            condition = condition + " AND LOWER(p.name) LIKE '%{0}%'".format(
                search.lower()
            )

        # Үйлдэрлэгчээр шүүх
        if "manufacturer" in self.request.GET:
            manufacturers_id = self.request.GET.getlist("manufacturer")
            condition = condition + " AND pm.id in {0}".format(tuple(manufacturers_id))

        products_base_query = """
            SELECT p.id, p.name, p.image, pm.name, pse.name, pmt.name, pf.name, pp.price, ps.in_stock
            FROM product_product as p
            INNER JOIN product_price as pp ON p.id = pp.product_id
            INNER JOIN product_stock as ps ON p.id = ps.product_id
            LEFT JOIN customer_customer as pm ON p.manufacturer_id = pm.id
            LEFT JOIN customer_customer as pse ON p.seller_id = pse.id
            LEFT JOIN product_measuringtype as pmt ON p.measuring_type_id = pmt.id
            LEFT JOIN product_form as pf ON p.form_id = pf.id
            INNER JOIN product_category as pcat ON p.category_id = pcat.id
            WHERE {0} ORDER BY p.name
            """.format(
            condition
        )

        cursor = connection.cursor()  # Өгөгөдлийн сантай connection үүсгэж байна
        cursor.execute(products_base_query)

        products = cursor.fetchall()
        product_list = []
        for (
            id_,
            name,
            image,
            manufacturer,
            seller,
            measuring_type,
            form,
            price,
            stock,
        ) in products:
            product = {}
            product["id"] = id_
            product["name"] = name
            # product["description"] = description #+ '\n' + 'Зааварчилгаа:\n' + instruction
            product["image"] = (
                "/media/" + image if image else "https://via.placeholder.com/300"
            )
            product["manufacturer"] = manufacturer
            product["seller"] = seller
            product["measuring_type"] = measuring_type
            product["form"] = form
            product["price"] = price
            product["stock"] = stock
            product_list.append(product)

        # Бүтээгдэхүүн хуудаслалт
        page = self.request.GET.get("page", 1)
        paginator = Paginator(product_list, 12)
        try:
            products_ = paginator.page(page)
        except PageNotAnInteger:
            products_ = paginator.page(1)
        except EmptyPage:
            products_ = paginator.page(paginator.num_pages)

        for object_ in products_:
            product = get_object_or_404(Product, pk=object_["id"])
            discount, discounted_price = product.get_promotion(
                self.request, warehouse_id, object_["price"]
            )
            object_["is_discounted"] = discounted_price != object_["price"]
            object_["discounted_price"] = discounted_price

        cursor.execute(
            """
            SELECT manu.id, manu.name FROM customer_customer as manu
            INNER JOIN product_product as p ON manu.id=p.manufacturer_id
            INNER JOIN product_price as pp ON p.id=pp.product_id
            INNER JOIN product_stock as ps ON p.id=ps.product_id
            WHERE pp.warehouse_id={0} AND ps.warehouse_id={0}
            GROUP BY manu.id ORDER BY manu.name
        """.format(
                warehouse_id
            )
        )
        manufacturers = dict(cursor.fetchall())

        cursor.execute(
            """
            SELECT seller.id, seller.name FROM customer_customer as seller
            INNER JOIN product_product as p ON seller.id=p.seller_id
            INNER JOIN product_price as pp ON p.id=pp.product_id
            INNER JOIN product_stock as ps ON p.id=ps.product_id
            WHERE pp.warehouse_id={0} AND ps.warehouse_id={0}
            GROUP BY seller.id ORDER BY seller.name
        """.format(
                warehouse_id
            )
        )

        sellers = dict(cursor.fetchall())

        # Template уруу дамжуулах
        context["is_paginated"] = products_.has_other_pages()
        context["products"] = products_  # Бүтээгдэхүүнүүд
        context["manufacturers"] = manufacturers  # Үйлдвэрлэгчид
        context["sellers"] = sellers  # Борлуулагчид
        context["layout"] = self.request.session.get(
            "product_layout", None
        )  # Бүтээгдэхүүний харагдац
        context["features"] = self.request.session.get(
            "product_features", None
        )  # Бүтээгдэхүүний харагдац

        return context


class ProductDetail(DetailView):
    model = Product
    template_name = "customer/product/detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        warehouse = get_object_or_404(
            Warehouse, pk=self.request.session[settings.WAREHOUSE_SESSION_ID]
        )

        cart = Cart(self.request)
        if str(self.object.id) in cart.cart.keys():
            quantity = cart.cart[str(self.object.id)]["quantity"]
            cart_product_form = CartQuantityForm(
                initial={"quantity": quantity, "update": True}
            )
        else:
            cart_product_form = CartQuantityForm()
        context["cart_product_form"] = cart_product_form

        context["pk"] = self.object.pk
        context["name"] = self.object.name
        context["image"] = self.object.image
        context["price"] = get_object_or_404(
            Price, warehouse=warehouse, product=self.object
        ).price
        context["stock"] = get_object_or_404(
            Stock, warehouse=warehouse, product=self.object
        ).in_stock
        context["description"] = (
            strip_tags(self.object.description) if self.object.description else "-"
        )
        context["ingredients"] = (
            strip_tags(self.object.ingredients) if self.object.ingredients else "-"
        )
        context["instruction"] = (
            strip_tags(self.object.instruction) if self.object.instruction else "-"
        )
        context["warning"] = (
            strip_tags(self.object.warning) if self.object.warning else "-"
        )
        return context


class ProductQuickView(DetailView):
    model = Product
    template_name = "customer/product/ajax/quickview.html"

    def get_context_data(self, **kwargs):
        context = super(ProductQuickView, self).get_context_data(**kwargs)
        warehouse = get_object_or_404(
            Warehouse, pk=self.request.session[settings.WAREHOUSE_SESSION_ID]
        )

        cart = Cart(self.request)
        if str(self.object.id) in cart.cart.keys():
            quantity = cart.cart[str(self.object.id)]["quantity"]
            cart_product_form = CartQuantityForm(
                initial={"quantity": quantity, "update": True}
            )
        else:
            cart_product_form = CartQuantityForm()
        context["cart_product_form"] = cart_product_form

        context["pk"] = self.object.pk
        context["name"] = self.object.name
        context["price"] = get_object_or_404(
            Price, warehouse=warehouse, product=self.object
        ).price
        context["stock"] = get_object_or_404(
            Stock, warehouse=warehouse, product=self.object
        ).in_stock
        context["description"] = strip_tags(self.object.description)
        context["manufacturer"] = (
            self.object.manufacturer.name if self.object.manufacturer else ""
        )
        context["seller"] = self.object.seller.name if self.object.seller else ""

        context["promotion"] = self.object.get_promotion_text(self.request, warehouse)

        return context


def product_ajax(request):
    if request.is_ajax():
        warehouse_id = request.session[settings.WAREHOUSE_SESSION_ID]
        warehouse = get_object_or_404(Warehouse, pk=warehouse_id)

        manifacturer = ""
        name = ""

        if "manifacturer" in request.GET:
            manifacturer = request.GET.get("manifacturer")

        if "name" in request.GET:
            name = request.GET.get("name")

        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT p.id, pc.name, pm.name, ps.name, p.name, p.image, st.in_stock,
            pr.price, mt.name, pf.name, p.description
            FROM product_product as p
            LEFT JOIN product_category as pc ON pc.id = p.category_id
            LEFT JOIN customer_customer as pm ON pm.id = p.manufacturer_id
            LEFT JOIN customer_customer as ps ON ps.id = p.seller_id
            LEFT JOIN product_measuringtype as mt ON mt.id = p.measuring_type_id
            LEFT JOIN product_form as pf ON pf.id = p.form_id
            INNER JOIN product_stock AS st ON p.id=st.product_id
            INNER JOIN product_price AS pr ON p.id=pr.product_id
            WHERE st.warehouse_id={0}
            AND pr.warehouse_id={0}
            AND pm.name ILIKE '%{1}%'
            AND p.name ILIKE '%{2}%'
            ORDER BY p.name
            """.format(
                warehouse_id, manifacturer, name
            )
        )
        rows = cursor.fetchall()
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
            "description"
        ]
        product_list = []
        for row in rows:
            product = {}
            for count, field in enumerate(fields):
                if field == 'description':
                    product[field] = strip_tags(row[count]) if row[count] else "-" 
                else:
                    product[field] = row[count]
            product_list.append(product)
        page = request.GET.get("page", 1)

        paginator = Paginator(product_list, 20)
        try:
            products = paginator.page(page)
            for product_ in products.object_list:
                product = get_object_or_404(Product, pk=product_["id"])
                discount, discounted_price = product.get_promotion(
                    request, warehouse_id, product_["price"]
                )
                product_["is_discounted"] = discounted_price != product_["price"]
                product_["discount"] = discount
                product_["discounted_price"] = discounted_price
            # print(products.object_list)
        except InvalidPage:
            # Return 404 if the page doesn't exist
            raise Http404

        # if 'manifacturer' in request.GET:
        #     return JsonResponse(products.object_list, safe=False)

        if (
            "page" in request.GET
            or "manifacturer" in request.GET
            or "name" in request.GET
        ):
            return JsonResponse(products.object_list, safe=False)

        return render(
            request, "customer/product/ajax/list.html", {"products": products}
        )
    else:
        return HttpResponse(
            mark_safe('<div style="height:200 margin:20px;">Системд алдаа гарлаа</div>')
        )


def product_layout_change_ajax_view(request):
    layout = request.GET.get("layout")
    features = request.GET.get("features")
    request.session["product_layout"] = layout
    request.session["product_features"] = features
    return JsonResponse({"status": "success"})

