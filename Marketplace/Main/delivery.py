import time
def in_transit(product):
    time.sleep(120)
    product.order_process_status = "in-transit"
    product.save()

def delivered(product):
    time.sleep(120)
    product.order_process_status = "delivered"
    product.save()