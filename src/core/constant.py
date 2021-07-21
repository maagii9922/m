
PROMOTION_TYPE_PRODUCT = 1
PROMOTION_TYPE_PACKAGE = 2
PROMOTION_TYPE_SUPPLIER = 3
PROMOTION_TYPE_ACC = 4
PROMOTION_TYPE = (
    (PROMOTION_TYPE_PRODUCT, 'Бүтээгдэхүүн'),
    (PROMOTION_TYPE_PACKAGE, 'Багц'),
    (PROMOTION_TYPE_SUPPLIER, 'Нийлүүлэгч'),
    (PROMOTION_TYPE_ACC, 'Акц'),
)

PROMOTION_IMPLEMENT_TYPE_PERCENT = 1
PROMOTION_IMPLEMENT_TYPE_PRICE = 2
PROMOTION_IMPLEMENT_TYPE_ABOVE_THE_NUMBER = 3
PROMOTION_IMPLEMENT_TYPE = (
    (PROMOTION_IMPLEMENT_TYPE_PERCENT, 'Хувь'),
    (PROMOTION_IMPLEMENT_TYPE_PRICE, 'Үнэ'),
    (PROMOTION_IMPLEMENT_TYPE_ABOVE_THE_NUMBER, 'Тооноос дээш'),
)

PRODUCT_TYPE_ALL = 1
PRODUCT_TYPE_IMPLEMENT = 2
PRODUCT_TYPE_NOT_IMPLEMENT = 3
PRODUCT_TYPE = (
    (PRODUCT_TYPE_ALL, 'Бүгд'),
    (PRODUCT_TYPE_IMPLEMENT, 'Сонгосон бүтээгдэхүүнд хэрэгжинэ'),
    (PRODUCT_TYPE_NOT_IMPLEMENT, 'Сонгосон бүтээгдэхүүнд хэрэгжихгүй'),
)

IMPLEMENT_TYPE_ALL = 1
IMPLEMENT_TYPE_CUSTOMER_CATEGORY = 2
IMPLEMENT_TYPE_CUSTOMER = 3
IMPLEMENT_TYPE_WAREHOUSE = 4
IMPLEMENT_TYPE = (
    (IMPLEMENT_TYPE_ALL, 'Бүгд'),
    (IMPLEMENT_TYPE_CUSTOMER_CATEGORY, 'Харилцагчийн төрөл'),
    (IMPLEMENT_TYPE_CUSTOMER, 'Харилцагчид'),
    (IMPLEMENT_TYPE_WAREHOUSE, 'Агуулах'),
)

ORDERED = 1
PACKED = 2
DELIVERY = 3
DELIVERED = 4
RECEIVED = 5
RETURNED = 6
ORDER_STATUS = (
    (ORDERED, 'Захиалагдсан'),
    (PACKED, 'Савлагдсан'),
    (DELIVERY, 'Хүргэлтээр гарсан'),
    (DELIVERED, 'Хүргэлт хийгдсэн'),
    (RECEIVED, 'Хүлээн авсан'),
    (RETURNED, 'Буцаасан')
)