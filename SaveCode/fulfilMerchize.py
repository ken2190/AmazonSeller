import requests,time,json,pandas as pd
import script.data as dataScript
import my_mongo.my_mongo as my_mongo

def send_merchize(account,data,order_id):
    base_url,key_api = account["base_url"],account["access-token"]
    url = base_url+"/order/external/orders"

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
            dataScript.updateOrder(my_mongo,order_id,{"sync_merchize":"Error"})
        else:
            dataScript.updateOrder(my_mongo,order_id,{"sync_merchize":response.json()["data"]})
    except :
        temp= {"error": response.text}
        dataScript.updateOrder(my_mongo,order_id,{"sync_merchize":"Error"})
    print("response",json.dumps(temp))
    return temp

def _run():
    query = { 
        "sync_merchize" : {
            "$exists": 0
        }
    }
   
    #Danh sach order chua sysc
    listOrder = dataScript.getOrderShopbaseSendMerchize(my_mongo,query=query)
    #Lay accect-token Merchize
    merchizeAccount = dataScript.getAccountMerchize(my_mongo,listStore=["i-want-this.merchize.store"])[0]

    #Lay design 
    listProductsKey = dataScript.getProductDesign(my_mongo,listOrder)
    for order in listOrder:
        temp_1c = {
            "order_id": order['shopbase_name'],
            # "identifier": order['shopbase_name'][:4],
            "shipping_info": {
                "full_name": order['first_name'] +" "+ order['last_name'],
                "address_1": order['address'],
                "address_2": order['address2'],
                "city": order['city'],
                "state": order['state'],
                "postcode": order['postcode'],
                "country": order['country'],
                "email": order['email'],
                "phone": order['phone'],
            },
            "items": []
        }

        for item in order['list_product']:
            if item['vendor'] == "Merchize":
                print("\n\nItem image",item['image'])
                tempItem = {
                    "name":item['sku'],
                    "product_id": item['product_id'],
                    "sku": item['sku'],
                    "quantity": item['quantity'],
                    "price": 0,
                    "currency": "USD",
                    "image": item['image'],
                    "design_front": "",
                    "design_back": "",
                    "attributes": [
                        {
                            "name": "Size",
                            "option": item['size']
                        }
                    ]
                }

                shop_productID = order["shop"]+"_"+str(item['product_id'])
                _status = False
                if shop_productID in listProductsKey:
                    if listProductsKey[shop_productID]["design"] not in ["Flag"]:
                        tempItem["design_front"] = listProductsKey[shop_productID]["design"]
                    else:
                        tempItem["design_front"] = listProductsKey[shop_productID]["design"][item['size']]
                    _status = True
                temp_1c["items"].append(tempItem)
        
        if len(temp_1c["items"]) > 0:
            print(temp_1c)
            requestsStatus = send_merchize(merchizeAccount,temp_1c,order["_id"])
            time.sleep(5)

    print("Done Sync")

# _run()

def export_products():
    query = { 
        "sync_merchize" : {
            "$exists": 0
        }
    }
    listOrder = dataScript.getOrderShopbaseSendMerchize(my_mongo,query=query,limit=1)
    list_product = []
    data_out = []
    for order in listOrder:
        for product in order['list_product']:
            if product['product_id'] not in list_product:
                temp = {
                    "product_id": product['product_id'],
                    "title": product['title'],
                    "image": product['image'],
                    "shop": order['shop'],
                    "shop_productID": order['shop']+"_"+str(product['product_id'])
                }
                list_product.append(product['product_id'])
                data_out.append(temp)
    return data_out
    
# data_out = export_products()

# dataScript.insertProduct(my_mongo,data_out)
# print(json.dumps(data_out))
# df = pd.DataFrame(data_out)
# df.to_csv('14_06_shopbase.csv',index=False)         