import requests,json,pymongo,time,datetime
import script.data as dataScript
import my_mongo.my_mongo as my_mongo

def generationPayload(order):
    line_items = []
    for item in order["list_product"]:
        temp = {
            "id": item['id'],
            "quantity": item['quantity']
        }
        line_items.append(temp)

    payload = {
        "fulfillment": {
            "line_items": line_items,
            "notify_customer": True,
            "service": "merchize",
            "tracking_company": "",
            "tracking_number": "",
            "tracking_url": ""
        }
    }
    tracking = order['tracking']
    for key in ['tracking_number','tracking_url','tracking_company']:
        if key in tracking:
            payload["fulfillment"][key] = tracking[key]
            
    return payload

def get_tracking(account, order_id):
    base_url,key_api = account["base_url"],account["access-token"]
  
    order_search = order_id
    
    while True:
        try:
            response = requests.get(
                url = base_url+'/order/external/orders/tracking?external_number=' + order_search,
                
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': "Bearer " +str(key_api)
                }
            )
            
            break
        except Exception as  err:
            print('Time out', err)
            time.sleep(5)

    try:
        if 'success' in response.json() and response.json()['success'] == True and response.json()['data'][0]['has_tracking'] == True:
            responseData = response.json()['data'][0]
            tracking = {}
            for key in ['tracking_number','tracking_url','tracking_company']:
                if key in responseData:
                    tracking[key] = responseData[key]
            return tracking
        else:
            # print(response.json())
            return None
    except:
        return None
    
def add_tracking(key_store, order):
    order_id = order['id']
    url = "/admin/orders/"+str(order_id)+"/fulfillments.json"

    url = key_store+url

    # payload = "{\"fulfillment\":{\"tracking_number\":\""+str(tracking_number)+"\",\"tracking_company\":\""+data_company[str(shipping_code)]+"\",\"line_items\":[{\"id\":"+str(line_items['id'])+",\"quantity\":"+str(line_items['quantity'])+"}],\"notify_customer\":true,\"order_id\":"+str(order_shopbase_id)+",\"service\":\"shopbase\",\"tracking_url\":\"\"}}"
    payload = generationPayload(order)
    
    headers = {
        'Content-Type': "text/plain;charset=UTF-8",
        }

    while True:
        try:
            response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
            break
        except Exception as  err:
            print('Time out', err)
            time.sleep(5)

    return (response.text)

def _getTrackingMerchize():
    query = { 
        "tracking" : {
            "$exists": 0
        }
    }
    #Danh sach order chua sysc
    listOrder = dataScript.getOrderShopbaseGetTrackingMerchize(my_mongo,query=query)
    #Lay accect-token Merchize
    merchizeAccount = dataScript.getAccountMerchize(my_mongo,listStore=["i-want-this.merchize.store"])[0]

    for index_order,order in enumerate(listOrder):
        id_order = order['shopbase_name']
        print(index_order+1,len(listOrder),id_order)
        tracking = get_tracking(merchizeAccount, id_order)
        print(tracking)
        if tracking is not None:
            dataScript.updateOrder(my_mongo,order['_id'],{"tracking":tracking})

def _sendTrackingShopbase(account):
    name_store,key_store = account["sub_domain"],account["url"]
    query = { 
        "tracking" : {
            "$exists": 1
        },
        "sendTrackingShopbase" : {
            "$exists": 0
        },
        "shop": name_store
    }
    # Danh sach order chua sysc
    listOrder = dataScript.getOrderSendTrackingShopbase(my_mongo,query=query)
    for index_order,order in enumerate(listOrder):
        print(index_order+1,len(listOrder),order['id_order'])

        date_created = datetime.datetime.strptime(order['date_created'].split("+")[0], '%Y-%m-%dT%H:%M:%S')
        if (date_created+datetime.timedelta(days = 5) < datetime.datetime.now()):
            add_tracking(key_store, order)
            dataScript.updateOrder(my_mongo,order['_id'],{"sendTrackingShopbase":"Done"})

def _run():
    print("_getTrackingMerchize")
    _getTrackingMerchize()
    time.sleep(3)
    print("_sendTrackingShopbase")

    list_account = dataScript.getAccountShopbase(my_mongo)
    for accountIndex,account in enumerate(list_account):
        print(accountIndex, '/', len(list_account), account['sub_domain'])
        _sendTrackingShopbase(account)

# _run()