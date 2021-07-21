import json
import copy

from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse

from src.warehouse.models import Warehouse
from src.product.models import Product

from src.customer.cart import Cart
from src.customer.views import core as c
from src.order.models import Order as OrderModel, OrderProduct
from src.core import constant as const
from src.fetch.connection import Connection


class Order(c.TemplateView):
    template_name = "customer/order.html"

    def dispatch(self, request, *args, **kwargs):
        self.warehouse = get_object_or_404(
            Warehouse, pk=self.request.session[settings.WAREHOUSE_SESSION_ID]
        )
        return super(Order, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Order, self).get_context_data(**kwargs)
        context["warehouses"] = self.request.user.customer.warehouses.all()
        context["warehouse_id"] = self.warehouse.id
        return context


# @require_POST
def ajax_create_order(request):
    """
    Захиалгын мэдээлэл татаж хадгалах
    """

    order = {}
    warehouse_id = request.session[settings.WAREHOUSE_SESSION_ID]
    warehouse = get_object_or_404(Warehouse, pk=warehouse_id)
    seller = warehouse.company.employees.filter(user__isnull=False).first()

    created_order = OrderModel.objects.create(
        customer=request.user.customer,
        warehouse=warehouse,
        seller=seller,
        status=const.ORDERED,
    )

    cart = Cart(request)
    products = copy.deepcopy(cart.order)
    product_list = [item for item in products.values()]

    for product in product_list:
        p = get_object_or_404(Product, pk=product["id"])
        product["prod_id"] = product.pop("id")
        product["prod_price"] = product.pop("price")
        product["reduced_price"] = product.pop("discounted_price")
        product["uom_id"] = p.measuring_type.id
        product["expire_range_id"] = ""
        del product["category"]
        del product["manufacturer"]
        del product["seller"]
        del product["name"]
        del product["image"]
        del product["stock"]
        del product["measuring_type"]
        del product["form"]
        del product["discount"]
        del product["total"]

    order["warehouse_id"] = warehouse.id
    order["seller_emp_id"] = seller.erp_id
    order["customer_org_id"] = request.user.customer.id
    order["company_id"] = warehouse.company.id
    order["sales_type"] = "credit"
    order["prod_list"] = product_list
    order["crm_order_id"] = str(created_order.id)
    order["no_tax"] = 0
    order["vat_bill_id"] = ""
    order["vat_qr_data"] = ""
    order["vat_bill_type"] = ""
    order["vat_tax_type"] = ""

    connection = Connection.get_instance(warehouse.company.id)
    response = connection.order(order)
    print("****************************")
    print(response.json())

    if response.status_code == 200 and response.json().get("status") == "success":

        created_order.packing_list_id = (
            response.json().get("data").get("packing_list_id")
        )
        created_order.save()
        cart.clear()

        for key, item in cart.order.items():
            product = get_object_or_404(Product, pk=int(key))
            OrderProduct.objects.create(
                order=created_order,
                product=product,
                quantity=item["quantity"],
                price=item["price"],
                discount=item.get("discount"),
                discount_package=item.get("discount_package"),
                discounted_price=item.get("discounted_price"),
                total=item["total"],
            )

        messages.success(request, "Захиалга амжилттай хийгдлээ")

    else:
        created_order.delete()
        return JsonResponse({"status": "error"})
    # print(response.json())
    return JsonResponse(response.json())


def warehouse_change_ajax_view(request, warehouse_id):
    cart = Cart(request)
    cart.clear()
    request.session[settings.WAREHOUSE_SESSION_ID] = warehouse_id
    return redirect("customer-order")


@require_POST
def cart_add_products_ajax_view(request):
    cart = Cart(request)
    hidden = request.POST.get("hidden")
    products = json.loads(hidden)
    for pk in products:
        product = get_object_or_404(Product, pk=pk)
        if pk in cart.cart:
            cart.add(product=product, quantity=1, update_quantity=False)
        else:
            cart.add(product=product, quantity=1, update_quantity=True)
    return redirect("customer-order")


def cart_ajax_load(request):
    return render(request, "customer/cart.html")
