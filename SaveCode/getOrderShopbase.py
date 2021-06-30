import requests,time,json

import my_mongo.my_mongo as my_mongo
import script.orders_shopbase as orders_shopbase
import script.data as dataScript

def get_orders(page_number, key_store):

    url = "/admin/orders.json?limit=250&orderstatus=open&page="+str(page_number)
    url = key_store+url
    print("Goto ",url)
    while True:
        try:
            response = requests.request("GET", url=url, timeout=5).json()
            break
        except Exception as  err:
            print('Time out', err)
            time.sleep(5)


    try:
        if len(response['orders']) > 0:
            return response['orders']
        else:
            return None
    except :
        return None

def _run_get_orders(account):
    name_store,key_store = account["sub_domain"],account["url"]
    index=1

    while(1):
        list_orders_request = get_orders(index, key_store)
        if list_orders_request is not None:
            list_orders = []
            for order in list_orders_request:
                temp = {
                    'id': str(order['id']),
                    'id_order': name_store+'_'+ str(order['id']),
                    'shop' : name_store,
                    'shopbase_name' : order['name'],
                    'first_name': order['shipping_address']['first_name'],
                    'last_name': order['shipping_address']['last_name'],
                    'address': order['shipping_address']['address1'],
                    'address2': order['shipping_address']['address2'],
                    'postcode': order['shipping_address']['zip'],
                    'state': order['shipping_address']['province'],
                    'city': order['shipping_address']['city'],
                    'country': order['shipping_address']['country'],
                    'phone': order['shipping_address']['phone'],
                    'email': order['email'],
                    'date_created':  order['created_at'],
                    'status': 1,
                    'order_number': str(order['order_number']),
                    'shipping': order['shipping_lines'][0]['title'],
                    'list_product' : [
                        {
                            'shop': name_store,
                            'product_id': product['product_id'],
                            'quantity': product['quantity'],
                            'size': product['variant_title'],
                            'title': product['title'],
                            'sku': product['sku'],
                            'image': product['image_src'],
                            'vendor': product['vendor'],
                            'id': product['id']
                            
                        } for product in order['line_items']
                    ]
                }            
                list_orders.append(temp)
                
            #Insert ideas  
            if len(list_orders)> 0:
                list_id = [i['id_order'] for i in list_orders]
                temp = dataScript.getOrderShopbaseCheck(my_mongo,listIn=list_id)
                list_id_old = [i['id_order'] for i in temp]
                print(len(list_id_old))

                orders_import = [i for i in list_orders if i['id_order'] not in list_id_old]
                if len(orders_import) > 0:
                    print(len(orders_import))
                    dataScript.insertOrder(my_mongo,orders_import)

            print(len(list_orders))
            index+=1
        else:
            break

def _run():
    list_account = dataScript.getAccountShopbase(my_mongo)
    for accountIndex,account in enumerate(list_account):
        print(accountIndex, '/', len(list_account), account['sub_domain'])
        _run_get_orders(account)

# _run()