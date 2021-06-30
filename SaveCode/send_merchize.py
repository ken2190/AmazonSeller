import get_order_shopbase
def create_mongo(ip, MONGO_DB):
    client = pymongo.MongoClient('mongodb://localhost:27017/') # server.local_bind_port is assigned local port
    db = client[MONGO_DB]

    return [client, db]

def get_data_orders():
    [myclient, mydb] = create_mongo("173.249.11.123", "Listing_Wish_Crawl")

    query = { 
        "sync_merchize" : {
            "$exists": 0
        }
    }

    projection = {
        "_id": 1,
        "ShippingDetail": 1,
        "product_name": 1,
        "quantity": 1,
        "product_image_url": 1,
        "size": 1,
        "price": 1,
        "product_id": 1,
        "wish_store": 1,
        "order_id": 1
        
    }
    
    list_id_old = []
    for order in mydb['orders'].find(query, projection):
        list_id_old.append(order)

    myclient.close()
    return list_id_old

def send_merchize(data):
    key_api="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2MDdkMzhhZDUyNzZhOTkwNzVkMjgzOTkiLCJlbWFpbCI6Imh1bmdAY2VudHoudm4iLCJpYXQiOjE2MjEzMjYwOTYsImV4cCI6MTYyMzkxODA5Nn0.L7HwSgUqEKnAQ5dHV755h2sng8pjl_WAZiQuOfwtg1E"

    url = "https://w-centz.merchize.store/bo-api/order/external/orders"

    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer "+str(key_api)
    }

    response = requests.request("POST", url, data=json.dumps(data), headers=headers)
    
    try:
        temp = {
            "status": response.json()['success']
        }
        if temp['status'] is False:
            temp["error"] = response.text
    except :
        temp= {"error": response.text}
    # print(json.dumps(temp))
    return temp

def update_order_merchize(_id, data):
    [myclient, mydb] = create_mongo("173.249.11.123", "Listing_Wish_Crawl")

    query = { 
        "_id": _id
    }
    
    mydb['orders'].update_one(query, {"$set": {"sync_merchize": data}})

    myclient.close()

def insert_orders(list_orders):
    [myclient, mydb] = create_mongo("173.249.11.123", "Listing_Wish_Crawl")

    mydb['orders'].insert_many(list_orders)

    myclient.close()

def check_id_had(list_id):
    [myclient, mydb] = create_mongo("173.249.11.123", "Listing_Wish_Crawl")

    query = { 
        "order_id": {
            "$in": list_id
        }
    }

    projection = {
        "_id": 0,
        "order_id": 1
    }
    
    list_id_old = []
    for order in mydb['orders'].find(query, projection):
        list_id_old.append(order['order_id'])

    myclient.close()
    
    list_id_new = [i for i in list_id if i not in list_id_old]
    return list_id_new

def get_orders(access_token, limit, start_num):
    url = "https://merchant.wish.com/api/v2/order/get-fulfill"
    
    params = {
        "access_token": access_token,
        "format": "json",
        "locale": "en",
        "limit": limit,
        "start": start_num
    }

    r = requests.get(url, params=params).json()
    if r['code'] == 0:
        return r['data']
    else:
        print(r['message'], access_token)
        return None

def _run_get_orders(info_account):
    access_token = info_account['access_token']
    limit = 500
    index_page = 0
    while True:
        start_num = limit*index_page
        print(start_num)
        list_orders = get_orders(access_token, limit, start_num)
        if len(list_orders) == 0:
            print("End!")
            return "End!"

        list_id = [i['Order']['order_id'] for i in list_orders]

        # print(list_id)

        list_id_new = check_id_had(list_id)
        if len(list_id_new) == 0:
            print("list_id_new is empty!")
            # exit(0)
        else:
            
            list_import = []
            for order in list_orders:
                if order['Order']['order_id'] in list_id_new:
                    temp = order['Order']
                    print(order['Order']['order_id'])
                    if 'hours_to_fulfill' in order['Order']:
                        temp['status'] = "NEW"
                    else:
                        temp['status'] = "OLD"
                    
                    if 'product_image_url' in temp:
                        temp['product_image_url'] = temp['product_image_url'].split("?")[0].replace("normal.jpg", "original.jpg")
                    
                    if 'size' in temp:
                        temp['size'] = temp['size'].replace("&#39;&#39;", "")

                        
                    
                    temp['order_time_filter'] = datetime.datetime.strptime(temp['order_time'], '%Y-%m-%dT%H:%M:%S')
                    temp['note'] = ""
                    temp['wish_store'] = info_account['name']

                    
                    
                    # print(temp['order_time'])
                    list_import.append(temp)

            insert_orders(list_import)
            print(len(list_orders))
        index_page +=1

def _run():
    print("Run Sync...")
    data_orders = get_data_orders()
    for order in data_orders:
        temp_1c = {
            # "order_id": order['wish_store']+"_"+str(order['_id']),
            "order_id": order['order_id'],
            "identifier": order['wish_store'],
            "shipping_info": {
                "full_name": order['ShippingDetail']['name'],
                "address_1": order['ShippingDetail']['street_address1'],
                "address_2": "",
                "city": "",
                "state": "",
                "postcode": order['ShippingDetail']['zipcode'],
                "country": order['ShippingDetail']['country'],
                "email": "",
                "phone": ""
            },
            "items": [
                {
                    "name": " ",
                    "product_id": order['product_id'],
                    "sku": " ",
                    "quantity": order['quantity'],
                    "price": order['price'],
                    "currency": "USD",
                    "image": order['product_image_url'],
                    "design_front": "",
                    "design_back": "",
                    "attributes": [
                        {
                            "name": "Size",
                            "option": order['size']
                        }
                    ]
                }
            ]
        }

        list_key = {
            "address_2": "street_address2",
            "phone": "phone_number",
            "state": "state",
            "city": "city",
        }
        for key in list_key:
            if key in order['ShippingDetail']:
                temp_1c['shipping_info'][list_key[key]] = order['ShippingDetail'][key]

        print(temp_1c)

        x = send_merchize(temp_1c)
        print(x)
        update_order_merchize(order['_id'],x)
    print("Done Sync")

def send_merchize(data):
    key_api = DB_get_key_merchize()
    url = "https://phantrunghai.merchize.store/bo-api/order/external/orders"

    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer "+str(key_api)
    }

    response = requests.request("POST", url, data=json.dumps(data), headers=headers)
    
    try:
        temp = {
            "status": response.json()['success']
        }
        if temp['status'] is False:
            temp["error"] = response.text
    except :
        temp["error"] = response.text
    
    print(json.dumps(temp))
    return temp

data = {
    "order_id": order_id,
    "shipping_info": {
        "full_name": buyer_detail["Full Name"],
        "address_1": buyer_detail["Address"],
        "address_2": buyer_detail["Address 2"],
        "city": buyer_detail["City"],
        "state": buyer_detail["State"],
        "postcode": buyer_detail["Zip"],
        "country": buyer_detail["Country"],
        "email": "",
        "phone": buyer_detail["Phone"]
    },
    "items": [
        {
            "quantity": product_quantity,
            "image": product_image,
            "attributes": [
                {
                    "name": "product",
                    "option": product_type
                },
                {
                    "name": "Color",
                    "option": product_color
                },
                {
                    "name": "Size",
                    "option": product_size
                }
            ]
        }
    ]
}

data['items'][0]["design_front"] = $(".url-design[index=1]").val();
data['items'][0]["design_back"] = $(".url-design[index=2]").val();
data['items'][0]["design_sleeve"] = $(".url-design[index=3]").val();
data['items'][0]["design_hood"] = $(".url-design[index=4]").val();

if(data['items'][0]["design_front"] == "" and data['items'][0]["design_back"] == ""){