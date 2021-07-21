
from django.urls import path

from src.core.urls import Nurl

from src.customer.views import cart, product, order, feedback, core


urlpatterns = [
    Nurl('login/') > 'src.customer.views.Login',
    Nurl('logout/') > 'src.customer.views.Logout',
    Nurl('password-change/') > 'src.customer.views.PasswordChange',
    Nurl('') > 'src.customer.views.Home',

    Nurl('order/') > 'src.customer.views.Order',
    path('ajax/create/order/', order.ajax_create_order, name='ajax_create_order'),
    path('ajax/warehouse/change/<int:warehouse_id>/', order.warehouse_change_ajax_view,
         name='warehouse_change_ajax_view'),
    path('ajax/cart/add/products/', order.cart_add_products_ajax_view,
         name='cart_add_products_ajax_view'),
    path('ajax/cart/load/', order.cart_ajax_load, name='cart_ajax_load'),

    Nurl('track-order/') > 'src.customer.views.TrackOrder',
    Nurl('track-order/<int:status>/') > 'src.customer.views.TrackOrder',
    Nurl('track-order/<int:pk>/detail/') > 'src.customer.views.TrackOrderDetail',

    Nurl('posts/') > 'src.customer.views.Posts',
    Nurl('posts/<int:pk>/detail/') > 'src.customer.views.PostDetail',
    Nurl('contact-us/') > 'src.customer.views.ContactUs',
    Nurl('terms-and-conditions/') > 'src.customer.views.TermsAndConditions',
    Nurl('privacy-policy/') > 'src.customer.views.PrivacyPolicy',

    Nurl('products/') > 'src.customer.views.Products',
    Nurl('products/<int:category_id>/') > 'src.customer.views.Products',
    Nurl('product/<int:pk>/') > 'src.customer.views.ProductDetail',
    Nurl('ajax/product/<int:pk>/') > 'src.customer.views.ProductQuickView',
    path('ajax/product/', product.product_ajax, name='customer_product_ajax'),
    path('ajax/product/layout/change/', product.product_layout_change_ajax_view,
         name='product_layout_change_ajax_view'),


    path('cart/add/<int:product_id>/', cart.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', cart.cart_remove, name='cart_remove'),
    path('cart/clear/', cart.cart_clear, name='cart_clear'),
    path('cart/add/ajax/<int:product_id>/',
         cart.cart_add_ajax, name='cart_add_ajax'),
    path('cart/update/ajax/<int:product_id>/',
         cart.cart_update_ajax, name='cart_update_ajax'),
    path('cart/remove/ajax/<int:product_id>/',
         cart.cart_remove_ajax, name='cart_remove_ajax'),
    path('cart/header/ajax/', cart.cart_header_ajax, name='cart_header_ajax'),

    path('feedback/create/', feedback.create_feedback, name='create_feedback')
]

handler404 = 'src.customer.views.core.error_404'
handler500 = 'src.customer.views.core.error_500'
