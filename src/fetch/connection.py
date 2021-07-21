# -*- coding: utf-8 -*-

"""ИРП холболт"""

import json
import requests

from django.conf import settings


class Connection:
    """
    ИРП тай холболт үүсгэх
    """

    __instance = None

    def __init__(self, company_id=False):
        port_dict = {
            1: "8000",
        }
        if company_id:
            self.port = port_dict[company_id]
        else:
            self.port = settings.ERP_PORT

        self.host = settings.ERP_HOST

    @staticmethod
    def get_instance(company_id=False):
        """
        Singleton класс хэрэгжүүлж байна
        """
        # if Connection.__instance is None:
        #     Connection.__instance = Connection()
        # return Connection.__instance
        return Connection(company_id=company_id)

    def update_company(self, v_date):
        """
        Компанийн мэдээлэл шинэчлэх
        """
        url = "http://" + self.host + ":" + self.port + "/UpdateCompany"
        data = json.dumps({"V_DATE": v_date})
        response = requests.post(url, data=data)
        return response

    def update_position(self, v_date, company_id):
        """
        Ажилтны албан тушаалын мэдээлэл татах
        """
        url = "http://" + self.host + ":" + self.port + "/UpdatePosition"
        data = json.dumps({"V_DATE": v_date, "company_id": company_id})
        response = requests.post(url, data=data)
        return response

    def update_employee(self, v_date, company_id):
        """
        Ажилтны мэдээлэл татах
        """
        url = "http://" + self.host + ":" + self.port + "/UpdateEmployee"
        data = json.dumps({"V_DATE": v_date, "company_id": company_id})
        response = requests.post(url, data=data)
        return response

    def update_warehouse(self, v_date, company_id):
        """
        Агуулахын мэдээлэл шинэчлэх
        """
        url = "http://" + self.host + ":" + self.port + "/UpdateBranch"
        data = json.dumps({"V_DATE": v_date, "company_id": company_id})
        response = requests.post(url, data=data)
        return response

    def update_customer(self, v_date):
        """
        Харилцагчийн мэдээлэл шинэчлэх
        """
        url = "http://" + self.host + ":" + self.port + "/UpdateCustomer"
        data = json.dumps({"V_DATE": v_date})
        response = requests.post(url, data=data)
        return response

    def update_company_customer(self, v_date, company_id):
        """
        Харилцагчийн мэдээлэл шинэчлэх
        """
        url = "http://" + self.host + ":" + self.port + "/UpdateCustomerList"
        data = json.dumps({"V_DATE": v_date, "company_id": company_id})
        response = requests.post(url, data=data)
        return response

    def update_product_category(self, v_date):
        """
        Бүтээгдэхүүний ангилал шинэчлэх
        """
        url = "http://" + self.host + ":" + self.port + "/UpdateProdCategory"
        data = json.dumps({"V_DATE": v_date})
        response = requests.post(url, data=data)
        return response

    def update_measuring_type(self, v_date):
        """
        Хэмжих нэгж
        """
        url = "http://" + self.host + ":" + self.port + "/UpdateMeasuringType"
        data = json.dumps({"V_DATE": v_date})
        response = requests.post(url, data=data)
        return response

    def update_product_form(self, v_date):
        """
        Эмийн хэлбэр
        """
        url = "http://" + self.host + ":" + self.port + "/UpdateProdForm"
        data = json.dumps({"V_DATE": v_date})
        response = requests.post(url, data=data)
        return response

    def update_product(self, v_date, e_date=None):
        """
        Бүтээгдэхүүний мэдээлэл шинэчлэх
        """
        url = "http://" + self.host + ":" + self.port + "/UpdateProduct"
        data = json.dumps({"V_DATE": v_date})
        if e_date:
            data.update({"E_DATE": e_date})
        response = requests.post(url, data=data)
        return response

    def update_product_price(self, v_date, company_id, warehouse_id):
        """
        Бүтээгдэхүүний үнийн мэдээлэл
        """
        url = "http://" + self.host + ":" + self.port + "/UpdateProdPrice"
        data = json.dumps(
            {"V_DATE": v_date, "company_id": company_id, "warehouse_id": warehouse_id}
        )
        response = requests.post(url, data=data)
        return response

    def update_product_stock(self, v_date, company_id, warehouse_id, multi=0):
        """
        Бүтээгдэхүүний үлдэгдлийн мэдээлэл шинэчлэх
        """
        url = "http://" + self.host + ":" + self.port + "/UpdateProdStock"
        data = json.dumps(
            {
                "V_DATE": v_date,
                "company_id": company_id,
                "warehouse_id": warehouse_id,
                "multi": multi,
            }
        )
        response = requests.post(url, data=data)
        return response

    def order(self, order):
        """
        Захиалга
        """
        url = "http://" + self.host + ":" + self.port + "/OrderDraft"
        data = json.dumps(order)
        response = requests.post(url, data=data)
        return response

    def track_order(self, company_id, packing_list_ids):
        print(company_id)
        print(packing_list_ids)
        url = "http://" + self.host + ":" + self.port + "/TrackOrder"
        data = json.dumps(
            {"company_id": company_id, "packing_list_ids": packing_list_ids}
        )
        response = requests.post(url, data=data)
        print(response.json())
        return response
