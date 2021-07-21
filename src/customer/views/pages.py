from django.db import connection
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from src.advertisement.models import Advertisement
from src.warehouse.models import Warehouse
from src.post.models import Post

from src.customer.views import core as c


__all__ = [
    "Login",
    "Logout",
    "PasswordChange",
    "Home",
    "ContactUs",
    "TermsAndConditions",
    "PrivacyPolicy",
]


class Login(LoginView):
    template_name = "customer/pages/login.html"

    def get_success_url(self):
        if not settings.WAREHOUSE_SESSION_ID in self.request.session:
            session = self.request.session
            user = self.request.user
            session[settings.WAREHOUSE_SESSION_ID] = user.customer.warehouses.first().id
        url = self.get_redirect_url()
        return url or reverse_lazy("customer-home")

    def form_valid(self, form):
        user = form.get_user()
        if not user.customer.warehouses.all():
            form.add_error(
                "",
                "Харилцагчид агуулах тохируулаагүй байна. \
            Менежерт хандаж агуулахаа тохируулна уу",
            )
            return self.form_invalid(form)
        return super(Login, self).form_valid(form)


class Logout(LogoutView):
    next_page = reverse_lazy("customer-login")


class PasswordChange(c.LoginRequired, PasswordChangeView):
    template_name = "customer/pages/password_change.html"
    success_url = reverse_lazy("customer-home")


class Home(c.TemplateView):
    template_name = "customer/pages/home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        warehouse_id = self.request.session[settings.WAREHOUSE_SESSION_ID]
        warehouse = get_object_or_404(Warehouse, pk=warehouse_id)

        customer = self.request.user.customer
        customer_category = customer.customer_category
        customer_id = customer.id
        warehouse_id = warehouse.id

        if not customer_category:
            customer_category_id = "Null"
        else:
            customer_category_id = customer_category.id

        context["banners"] = Advertisement.objects.filter(
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
            | Q(implement_type=3, customers=customer, is_implement=True)
            | Q(~Q(customers=customer), implement_type=3, is_implement=False)
            | Q(
                implement_type=4,
                warehouses__in=customer.warehouses.all(),
                is_implement=True,
            )
            | Q(
                ~Q(warehouses__in=customer.warehouses.all()),
                implement_type=4,
                is_implement=False,
            ),
            is_active=True,
        )
        cursor = connection.cursor()
        cursor.execute(
            """
            (SELECT p.id, p.name, p.image, s.in_stock, pr.price FROM product_product as p 
            INNER JOIN product_stock AS s ON p.id=s.product_id 
            INNER JOIN product_price AS pr ON p.id=pr.product_id 
            WHERE s.warehouse_id={2} AND pr.warehouse_id={2} and p.flag = 1 AND p.image IS NOT NULL
            LIMIT 5)
            UNION ALL
            (SELECT product.id, product.name, product.image, s.in_stock, pr.price FROM product_product as product 
            INNER JOIN product_stock AS s ON product.id=s.product_id 
            INNER JOIN product_price AS pr ON product.id=pr.product_id 
            INNER JOIN promotion_promotion_products ppp ON ppp.product_id = product.id
            INNER JOIN promotion_promotion p ON ppp.promotion_id = p.id
            LEFT JOIN promotion_promotion_customer_categories cc
            ON p.id=cc.promotion_id
            LEFT JOIN promotion_promotion_customers c
            ON p.id=c.promotion_id
            LEFT JOIN promotion_promotion_warehouses w
            ON p.id=w.promotion_id
            WHERE s.warehouse_id={2} AND pr.warehouse_id={2} and product.flag = 2
            AND p.promotion_type = 1 AND p.percent >= 10
            AND product.image IS NOT NULL



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
                )



            LIMIT 5)
            """.format(
                customer_category_id, customer_id, warehouse_id
            )
        )
        rows = cursor.fetchall()
        product_list = []
        keys = ["id", "name", "image", "stock", "price"]
        for row in rows:
            product = {}
            for counter, key in enumerate(keys):
                if key == "image":
                    if row[counter] != "":
                        product[key] = "media/" + row[counter]
                        print("*******", row[counter])
                    else:
                        product[key] = "https://via.placeholder.com/300"
                else:
                    product[key] = row[counter]
            product_list.append(product)
        context["products"] = product_list
        context["posts"] = Post.objects.filter(is_active=True)[:10]
        return context


class ContactUs(c.TemplateView):
    template_name = "customer/pages/contact_us.html"


class TermsAndConditions(c.TemplateView):
    template_name = "customer/pages/terms_and_conditions.html"


class PrivacyPolicy(c.TemplateView):
    template_name = "customer/pages/privacy_policy.html"
