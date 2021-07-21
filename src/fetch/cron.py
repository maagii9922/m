import re
import base64
import logging
import time
import pandas as pd
from datetime import datetime, timedelta


from django.core.files.base import ContentFile
from django.conf import settings
from django.db import connection as conn
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime

from src.company.models import Company
from src.warehouse.models import Warehouse
from src.employee.models import Position, Employee
from src.customer.models import Customer
from src.product.models import Category, MeasuringType, Form, Product, Price, Stock
from src.order.models import Order, OrderProduct
from src.core.shortcuts import get_object_or_create, get_object_or_none, xstring

from .connection import Connection

# Get an instance of a logger
logger = logging.getLogger(__name__)


def validate_date(date_string):
    """
    Он сар өдөр YYYY-MM-DD форматтайг шалгана
    """
    date_re = re.compile(r"(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$")
    match = date_re.match(date_string)
    if match:
        return True
    return False


def update_company(V_DATE=None):
    """
    Компанийн мэдээлэл татах

    V_DATE-д он-сар-өдөр дамжуулна эсвэл хоосон орхино

    Хэрэв компани үүссэн байвал хамгийн сүүлд засагдсан компанийн огноог авна

    Хэрэв компани үүсээгүй бол "2017-01-01 00:00:00" авна
    """

    if V_DATE:
        if validate_date(V_DATE):
            v_date = V_DATE + " 00:00:00"
        else:
            logger.warning("Invalid date")
            return
    elif Company.objects.first():
        v_date = Company.objects.first().updated_at.strftime("%Y-%m-%d %H:%M:%S")
    else:
        v_date = "2017-01-01 00:00:00"

    connection = Connection.get_instance()
    response = connection.update_company(v_date)

    if response.status_code == 200 and response.json().get("status") == "success":
        logger.info(response.json())
        for com in response.json().get("data"):
            company = get_object_or_create(Company, pk=com.get("id"))
            company.flag = com.get("flag")
            company.partner_id = com.get("partner_id")
            company.name = com.get("name")
            company.save()
        logger.info("Updated companies")
    else:
        logger.info("Something wrong company update!")


def update_warehouse(V_DATE=None):
    """
    Агуулахын мэдээлэл татах
    """

    company_id_list = Company.objects.values_list(
        "id", flat=True
    )  # Үүссэн компаниудын ID-г листээр авна

    if hasattr(settings, "COMPANY_IDS"):
        company_id_list = settings.COMPANY_IDS

    for company_id in company_id_list:
        whouse = Warehouse.objects.filter(company_id=company_id).first()
        if V_DATE:
            if validate_date(V_DATE):
                v_date = V_DATE + " 00:00:00"
            else:
                logger.warning("Invalid date")
                return
        elif whouse:
            v_date = whouse.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        else:
            v_date = "2017-01-01 00:00:00"

        connection = Connection.get_instance(company_id)
        response = connection.update_warehouse(v_date, company_id)
        logger.info(response.json())

        if response.status_code == 200 and response.json().get("status") == "success":
            for whouse in response.json().get("data"):
                warehouse = get_object_or_create(
                    Warehouse, id=whouse.get("id"), company_id=company_id
                )
                warehouse.flag = whouse.get("flag")
                warehouse.name = whouse.get("name")
                warehouse.save()
            logger.debug("Warehouses updated")
        else:
            logger.debug("Warehouses updated error")


def update_position(V_DATE=None):
    """
    Албан тушаал татах
    """

    company_id_list = Company.objects.values_list(
        "id", flat=True
    )  # Үүссэн компаниудын ID-г листээр авна

    if hasattr(settings, "COMPANY_IDS"):
        company_id_list = settings.COMPANY_IDS

    for company_id in company_id_list:

        if V_DATE:
            if validate_date(V_DATE):
                v_date = V_DATE + " 00:00:00"
            else:
                logging.warning("Invalid date")
                return
        else:
            v_date = "2017-01-01 00:00:00"

        connection = Connection.get_instance(company_id)
        response = connection.update_position(v_date, company_id)
        logger.debug(response.json())

        if response.status_code == 200 and response.json().get("status") == "success":
            positions = response.json().get("data")
            for position in positions:
                obj = get_object_or_create(Position, id=position.get("id"))
                obj.name = position.get("name")
                obj.flag = position.get("flag")
                obj.save()
            logger.debug("Positions updated")
        else:
            logger.warning("Positions not updated")

        # time.sleep(60)


def update_employee(V_DATE=None):
    """
    Ажилтан татах
    """
    company_id_list = Company.objects.values_list("id", flat=True)

    if hasattr(settings, "COMPANY_IDS"):
        company_id_list = settings.COMPANY_IDS

    for company_id in company_id_list:
        employee = Employee.objects.filter(company_id=company_id).first()

        if V_DATE:
            if validate_date(V_DATE):
                v_date = V_DATE + " 00:00:00"
            else:
                logger.warning("Invalid date")
                return
        elif employee:
            v_date = employee.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        else:
            v_date = "2017-01-01 00:00:00"

        connection = Connection.get_instance(company_id)
        response = connection.update_employee(v_date, company_id)
        logger.info(response.json())

        if response.status_code == 200 and response.json().get("status") == "success":
            employees = response.json().get("data")
            for employee in employees:
                obj = get_object_or_create(Employee, erp_id=employee["id"])
                obj.family_name = employee["family_name"]
                obj.last_name = employee["last_name"]
                obj.first_name = employee["first_name"]
                obj.birth_date = employee["birthday"]
                obj.register_no = employee["registration_no"]
                obj.email = employee["email"]
                obj.gender = (
                    employee.get("gender") if employee.get("gender") != "" else None
                )
                obj.flag = employee["flag"]
                obj.company = get_object_or_404(Company, pk=company_id)
                if (
                    employee["position_id"]
                    and Position.objects.filter(id=employee["position_id"]).exists()
                ):
                    obj.position = get_object_or_404(
                        Position, id=employee["position_id"]
                    )
                obj.save()
                if (
                    employee["branch_id"]
                    and Warehouse.objects.filter(id=employee["branch_id"]).exists()
                ):
                    obj.warehouses.add(
                        get_object_or_404(Warehouse, id=employee["branch_id"])
                    )
            logger.info("Employees updated")
        else:
            logger.info("Employees not updated")

        # time.sleep(60)


def update_customer(V_DATE=None):
    """
    Бүх харилцагчийн мэдээлэл татах
    """
    customer = Customer.objects.first()
    if V_DATE:
        if validate_date(V_DATE):
            v_date = V_DATE + " 00:00:00"
        else:
            logger.warning("Invalid date")
            return
    elif customer:
        v_date = customer.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    else:
        v_date = "2017-01-01 00:00:00"

    connection = Connection.get_instance()
    response = connection.update_customer(v_date)
    logger.info(response.json())

    if response.status_code == 200 and response.json().get("status") == "success":
        for cust in response.json().get("data"):
            customer = get_object_or_create(Customer, id=cust.get("id"))
            customer.parent = get_object_or_none(Customer, id=cust.get("parent_id"))
            customer.name = xstring(cust.get("name", None))
            customer.register_no = xstring(cust.get("ref", None))
            customer.phone = xstring(cust.get("phone", None))
            customer.email = xstring(cust.get("email", None))
            customer.fax = xstring(cust.get("fax", None))
            customer.addr_country = xstring(cust.get("country", None))
            customer.addr_city = xstring(cust.get("state", None))
            customer.addr_district = xstring(cust.get("state_wall", None))
            customer.addr_street = xstring(cust.get("street", None))
            customer.addr_street2 = xstring(cust.get("street2", None))
            customer.longitude = (
                cust.get("longitude")
                if cust.get("longitude") and cust.get("longitude").isdecimal()
                else None
            )
            customer.latitude = (
                cust.get("latitude")
                if cust.get("latitude") and cust.get("latitude").isdecimal()
                else None
            )
            customer.is_supplier = xstring(cust.get("supplier", None))
            customer.is_factory = xstring(cust.get("manufacturer", None))
            customer.flag = cust.get("flag")
            customer.save()
        logger.debug("Customers updated")
    else:
        logger.debug("Customers not updated")


def update_company_customer(V_DATE=None):
    """
    Харилцагчийн мэдээлэл компаниар татаж хадгалах
    """

    company_id_list = Company.objects.values_list("id", flat=True)

    if hasattr(settings, "COMPANY_IDS"):
        company_id_list = settings.COMPANY_IDS

    for company_id in company_id_list:
        custo = Customer.objects.filter(company_id=company_id).first()
        if V_DATE:
            if validate_date(V_DATE):
                v_date = V_DATE + " 00:00:00"
            else:
                logger.warning("Invalid date")
                return
        elif custo:
            v_date = custo.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        else:
            v_date = "2017-01-01 00:00:00"

        connection = Connection.get_instance(company_id)
        response = connection.update_company_customer(v_date, company_id)

        if response.status_code == 200 and response.json().get("status") == "success":
            logger.info(response.json())
            for cust in response.json().get("data"):
                customer = get_object_or_create(Customer, id=cust.get("id"))
                customer.company = get_object_or_404(Company, pk=company_id)
                customer.parent = get_object_or_none(Customer, id=cust.get("parent_id"))
                customer.name = xstring(cust.get("name", None))
                customer.register_no = xstring(cust.get("ref", None))
                customer.phone = xstring(cust.get("phone", None))
                customer.email = xstring(cust.get("email", None))
                customer.fax = xstring(cust.get("fax", None))
                customer.addr_country = xstring(cust.get("country", None))
                customer.addr_city = xstring(cust.get("state", None))
                customer.addr_district = xstring(cust.get("state_wall", None))
                customer.addr_street = xstring(cust.get("street", None))
                customer.addr_street2 = xstring(cust.get("street2", None))
                customer.longitude = (
                    cust.get("longitude") if cust.get("longitude").isdecimal() else None
                )
                customer.latitude = (
                    cust.get("latitude") if cust.get("latitude").isdecimal() else None
                )
                customer.is_supplier = xstring(cust.get("supplier", None))
                customer.is_factory = xstring(cust.get("manufacturer", None))
                # customer.is_customer =
                customer.flag = cust.get("flag")
                customer.save()

            logger.debug("Company customers updated")
        else:
            logger.debug("Company customers not updated")

        # time.sleep(60)


def update_product_category(V_DATE=None):
    """
    Бүтээгдэхүүний ангиллын татах
    """
    if V_DATE:
        if validate_date(V_DATE):
            v_date = V_DATE + " 00:00:00"
        else:
            logger.warning("Invalid date")
            return
    elif Category.objects.first():
        v_date = Category.objects.first().updated_at.strftime("%Y-%m-%d %H:%M:%S")
    else:
        v_date = "2017-01-01 00:00:00"

    connection = Connection.get_instance()
    response = connection.update_product_category(v_date)
    logger.info(response.json())

    if response.status_code == 200 and response.json().get("status") == "success":
        for pcategory in response.json().get("data"):
            if Category.objects.filter(id=pcategory.get("id", None)).exists():
                category = Category.objects.get(id=pcategory.get("id"))
            else:
                category = Category(id=pcategory.get("id"))

            if pcategory.get("parent_id"):
                category.parent = Category.objects.get(
                    id=pcategory.get("parent_id", None)[0]
                )
            category.name = pcategory.get("name", None)
            category.flag = pcategory.get("flag", None)
            category.save()
        logger.debug("Product categories updated")
    else:
        logger.debug("Product categories not updated")


def update_measuring_type(V_DATE=None):
    """
    Хэмжих нэгж
    """
    measuring_type = MeasuringType.objects.first()
    if V_DATE:
        if validate_date(V_DATE):
            v_date = V_DATE + " 00:00:00"
        else:
            logger.warning("Invalid date")
            return
    elif measuring_type:
        v_date = measuring_type.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    else:
        v_date = "2017-01-01 00:00:00"

    connection = Connection.get_instance()
    response = connection.update_measuring_type(v_date)
    logger.info(response.json())

    if response.status_code == 200 and response.json().get("status") == "success":
        for measuring in response.json().get("data"):
            measuring_type = get_object_or_create(
                MeasuringType, id=xstring(measuring.get("id", None))
            )

            measuring_type.name = xstring(measuring.get("name", None))
            measuring_type.factor = measuring.get("factor", None)
            measuring_type.flag = xstring(measuring.get("flag", None))
            measuring_type.save()
        logger.debug("Measuring types updated")
    else:
        logger.debug("Measuring types not updated")


def update_product_form(V_DATE=None):
    """
    Бүтээгдэхүүний хэлбэр
    """
    form = Form.objects.first()
    if V_DATE:
        if validate_date(V_DATE):
            v_date = V_DATE + " 00:00:00"
        else:
            logger.warning("Invalid date")
            return
    if form:
        v_date = form.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    else:
        v_date = "2017-01-01 00:00:00"

    connection = Connection.get_instance()
    response = connection.update_product_form(v_date)
    logger.info(response.json())

    if response.status_code == 200 and response.json().get("status") == "success":
        for form in response.json().get("data"):
            product_form = get_object_or_create(Form, id=xstring(form.get("id", None)))
            product_form.name = xstring(form.get("name", None))
            product_form.flag = xstring(form.get("flag", None))
            product_form.save()
        logger.debug("Product forms updated")
    else:
        logger.debug("Product forms not updated")


def update_product(V_DATE=None):
    """
    Бүтээгдэхүүний мэдээлэл татаж хадгалах

    Хэрэв хамгийн сүүлд шинэчлэгдсэн бүтээгдэхүүн байвал сүүлд өөрчлөгдсөн
    огноог авна эсвэл 2017-01-01 авна
    """
    if V_DATE:
        if validate_date(V_DATE):
            v_date = V_DATE + " 00:00:00"
        else:
            logger.warning("Invalid date")
            return
    elif Product.objects.first():
        v_date = (
            Product.objects.order_by("-updated_at")
            .first()
            .updated_at.strftime("%Y-%m-%d %H:%M:%S")
        )
    else:
        v_date = "2017-01-01 00:00:00"

    connection = Connection.get_instance()
    response = connection.update_product(v_date)

    if response.status_code == 200 and response.json().get("status") == "success":
        for prod in response.json().get("data"):
            product = get_object_or_create(Product, id=prod.get("id"))
            product.category = Category.objects.get(id=prod.get("categ_id"))
            product.name = xstring(prod.get("name", None))
            product.eng_name = xstring(prod.get("eng_name", None))
            product.generic_name = xstring(prod.get("generic_name", None))
            product.internal_code = xstring(prod.get("internal_code", None))
            product.barcode = xstring(prod.get("barcode", None))
            product.seller = get_object_or_none(
                Customer, id=xstring(prod.get("seller_id", None))
            )
            product.manufacturer = get_object_or_none(
                Customer, id=xstring(prod.get("manufacturer_id", None))
            )
            product.measuring_type = get_object_or_none(
                MeasuringType, id=xstring(prod.get("uom_id", None))
            )
            product.form = get_object_or_none(
                Form, id=xstring(prod.get("form_id", None))
            )
            product.ingredients = xstring(prod.get("ingredients", None))
            product.volume = xstring(prod.get("volume", None))
            product.is_exclusive = prod.get("is_exclusive", None) != ""
            product.description = xstring(prod.get("description", None))
            product.instruction = xstring(prod.get("instruction", None))
            product.warning = xstring(prod.get("warning", None))
            product.flag = xstring(prod.get("flag", None))
            product.save()

            if xstring(prod.get("image", None)):
                imgstr = prod.get("image")
                image = ContentFile(base64.b64decode(imgstr))
                product.image.save("product.jpeg", image, save=True)
        logger.debug("Products updated")
    else:
        logger.debug("Products not updated")


def update_product_price(V_DATE=None):
    """
    Бүтээгдэхүүний үнийн мэдээлэл татаж хадгалах

    Хэрэв хамгийн сүүлд шинэчлэгдсэн бүтээгдэхүүн байвал сүүлд өөрчлөгдсөн
    огноог авна эсвэл 2017-01-01 авна
    """
    cursor = conn.cursor()

    # Компани ID жагсаалтаар авна
    company_id_list = Company.objects.values_list("id", flat=True)

    if hasattr(settings, "COMPANY_IDS"):
        company_id_list = settings.COMPANY_IDS

    for company_id in company_id_list:
        for warehouse in Warehouse.objects.filter(company_id=company_id):

            price = Price.objects.filter(
                company_id=company_id, warehouse=warehouse
            ).first()
            if V_DATE:
                if validate_date(V_DATE):
                    v_date = V_DATE + " 00:00:00"
                else:
                    logger.warning("Invalid date")
                    return
            elif Price.objects.filter(
                company_id=company_id, warehouse=warehouse
            ).exists():
                v_date = (
                    Price.objects.filter(company_id=company_id, warehouse=warehouse)
                    .first()
                    .updated_at.strftime("%Y-%m-%d %H:%M:%S")
                )
            else:
                v_date = "2017-01-01 00:00:00"

            connection = Connection.get_instance(company_id)
            response = connection.update_product_price(v_date, company_id, warehouse.id)
            # logger.info(response.json())

            if (
                response.status_code == 200
                and response.json().get("status") == "success"
            ):
                prod_data = response.json().get("data")
                prod_ids = tuple(prod_data.keys())
                cursor.execute(
                    """
                    SELECT id, company_id, warehouse_id, product_id
                    FROM product_price
                    WHERE company_id={0} and warehouse_id={1} and product_id in {2}
                    """.format(
                        company_id, warehouse.id, prod_ids
                    )
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
                    if item.get("cost", None) != {}:
                        cost = next(iter(item.get("cost").values()))

                    if Product.objects.filter(id=int(key)).exists():

                        if (
                            company_id in exist_dict
                            and warehouse.id in exist_dict[company_id]
                            and int(key) in exist_dict[company_id][warehouse.id]
                        ):
                            price_id = exist_dict[company_id][warehouse.id][int(key)]
                            cursor.execute(
                                " \
                                UPDATE product_price \
                                SET price=%s, cost=%s, updated_at=NOW() \
                                WHERE id=%s \
                                "
                                % (price, cost, price_id)
                            )
                        else:
                            cursor.execute(
                                """
                                INSERT INTO product_price
                                (company_id, warehouse_id, product_id, price,
                                cost, is_active, created_at, updated_at)
                                VALUES ({0}, {1}, {2}, {3}, {4}, TRUE, NOW(), NOW())
                                """.format(
                                    company_id, warehouse.id, key, price, cost
                                )
                            )

                    else:
                        print("Product id: ", key)
                logger.debug("Product prices updated")
            else:
                logger.debug("Product prices not updated")

            # time.sleep(60)


def update_product_stock(V_DATE=None):
    """
    Бүтээгдэхүүний үлдэгдэл татаж хадгалах

    Хэрэв хамгийн сүүлд шинэчлэгдсэн бүтээгдэхүүн байвал сүүлд өөрчлөгдсөн
    огноог авна эсвэл 2017-01-01 авна
    """
    cursor = conn.cursor()

    # Компани ID жагсаалтаар авна
    company_id_list = Company.objects.values_list("id", flat=True)

    if hasattr(settings, "COMPANY_IDS"):
        company_id_list = settings.COMPANY_IDS

    for company_id in company_id_list:

        for warehouse in Warehouse.objects.filter(company_id=company_id):
            if V_DATE:
                if validate_date(V_DATE):
                    v_date = V_DATE + " 00:00:00"
                else:
                    logger.warning("Invalid date")
                    return
            if Stock.objects.filter(warehouse=warehouse).first():
                v_date = (
                    Stock.objects.filter(warehouse=warehouse)
                    .first()
                    .updated_at.strftime("%Y-%m-%d %H:%M:%S")
                )
            else:
                v_date = "2017-01-01 00:00:00"

            connection = Connection.get_instance(company_id)
            response = connection.update_product_stock(v_date, company_id, warehouse.id)
            # logger.info(response.json())

            if (
                response.status_code == 200
                and response.json().get("status") == "success"
            ):

                stock_data = response.json().get("data")
                prod_list = list(map(lambda x: x["prod_id"], stock_data))

                Stock.objects.filter(warehouse=warehouse).exclude(
                    product__id__in=prod_list
                ).update(in_stock=0)

                df = pd.DataFrame(stock_data)
                g = df.groupby(["prod_id"], as_index=False)["in_stock"].sum()

                stocks = g.to_dict("r")

                for stck in stocks:
                    if Product.objects.filter(
                        id=xstring(stck.get("prod_id", None))
                    ).exists():
                        stock = get_object_or_create(
                            Stock,
                            warehouse=warehouse,
                            product=Product.objects.get(
                                id=xstring(stck.get("prod_id", None))
                            ),
                        )
                        # expiration_date = xstring(
                        #     stck.get('expiration_date', None))
                        # if expiration_date:
                        #     expiration_date = parse_datetime(expiration_date)

                        # stock.lot_name = xstring(stck.get('lot_name', None))
                        stock.in_stock = xstring(stck.get("in_stock", None))
                        # stock.expiration_date = expiration_date
                        stock.flag = 1  # xstring(stck.get('flag', None))
                        stock.save()
                    else:
                        print(stck.get("prod_id", None))

                logger.debug("Product stocks updated")
            else:
                logger.debug("Product stocks not updated")

            # time.sleep(60)


def track_order(V_DATE=None):
    # Компани ID жагсаалтаар авна
    company_id_list = Company.objects.values_list("id", flat=True)

    if hasattr(settings, "COMPANY_IDS"):
        company_id_list = settings.COMPANY_IDS

    for company_id in company_id_list:
        if V_DATE:
            if validate_date(V_DATE):
                v_date = V_DATE + " 00:00:00"
            else:
                logger.warning("Invalid date")
                return
        elif Order.objects.filter(warehouse__company_id=company_id).first():
            v_date = Order.objects.filter(
                warehouse__company_id=company_id
            ).first().updated_at - timedelta(days=2)
            v_date = v_date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            v_date = "2017-01-01 00:00:00"

        packing_list_ids = list(
            Order.objects.filter(
                packing_list_id__isnull=False,
                updated_at__gte=v_date,
                warehouse__company_id=company_id,
            ).values_list("packing_list_id", flat=True)
        )

        connection = Connection.get_instance(company_id)
        response = connection.track_order(company_id, packing_list_ids)

        if response.status_code == 200 and response.json().get("status") == "success":
            for erp_order in response.json().get("data"):
                order = get_object_or_404(
                    Order, packing_list_id=erp_order["packing_list_id"]
                )
                # order.status = erp_order['status']
                # order.save()
                for prod in erp_order["prod_list"]:
                    if OrderProduct.objects.filter(
                        order=order, product_id=prod["prod_id"]
                    ).exists():
                        order_product = OrderProduct.objects.get(
                            order=order, product_id=prod["prod_id"]
                        )
                        print(order_product)
                    else:
                        print(prod)

                # print("##################")

        # time.sleep(20)

    # print(v_date)
