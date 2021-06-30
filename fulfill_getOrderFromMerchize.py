import requests,json,pymongo,time,datetime
import pandas as pd
from requests.models import Response
import script.data as dataScript
import my_mongo.my_mongo as my_mongo
import threading

def divide_chunks(l, n): 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

class myThread (threading.Thread):
    def __init__(self, account,order):
        threading.Thread.__init__(self)
        self.account = account
        self.order = order
        self.result = None

    def run(self):
        self.result = unpack_data(account=self.account, order=self.order)

def getItem(account, orderID):
    base_url,key_api = account["base_url"],account["access-token"]
    
    while True:
        try:
            response = requests.get(
                url = base_url+'/order/orders/'+str(orderID)+'/items',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': "Bearer " +str(key_api)
                }
            )
            return response.json()["data"]
        except Exception as  err:
            print('Error get_sale', response.text)
            return None

def get_sale(account, queryMore,page):
    query = {
        "payment_status":"paid",
        "code":"",
        "page":int(page),
        "limit":100
    }
    query.update(queryMore)
    base_url,key_api = account["base_url"],account["access-token"]
    
    while True:
        try:
            response = requests.post(
                url = base_url+'/order/v2/orders/search',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': "Bearer " +str(key_api)
                },
                data=json.dumps(query)
            )
            return (response.json()["data"]["orders"],response.json()["data"]["pages"])
        except Exception as  err:
            print('Error get_sale', response.text)
            return (None,None)

def unpack_data(account,order):
    dataUnpack = []
    responseItem = getItem(account, order["_id"])
    if responseItem is not None:
        for item in responseItem:
            temp = {
                "Order ID": order["external_order_number"],
                "Created": order["created"],
                "Store": [i['title'] for i in order["tags"] if "amazon_" in i["title"]][0],
                "First Name": order["shipping_address"]["full_name"].title().split(" ")[0],
                "Last Name": " ".join(order["shipping_address"]["full_name"].title().split(" ")[1:]),
                "Address": order["shipping_address"]["address"],
                "Address2": order["shipping_address"]["address2"],
                "City": order["shipping_address"]["city"],
                "State": order["shipping_address"]["state"],
                "Country": order["shipping_address"]["country_code"],
                "Zipcode": order["shipping_address"]["postal_code"],
                "Phone": order["shipping_address"]["phone"],
                "Email": order["shipping_address"]["email"],
                
                #Items
                "Product name": item["product"]["title"],
                "Mockup": item["image"],
                "Size": item["variant"]["title"],
                "Quantity": item["quantity"],

                #
                "Sup":"",
                "Design":"",
                "Line Dreamship":"",
                "Type 1C":"",
            }
            dataUnpack.append(temp)

    return dataUnpack

def getData(account, query):
    (data,pages) = get_sale(account, query,1)
    for page in range(2,pages+1):
        (_data,_) = get_sale(account, query,page)

        data +=_data

    print(data)
    print(len(data))
    if data is not None:
        dataReturn = []
        dataList = list(divide_chunks(data,5))
        for data in dataList:
            threads=[]
            for order in data:
                print(order["_id"])
                thread = myThread(account=account, order=order)
                thread.start()
                threads.append(thread)
            for t in threads:
                t.join()
                dataReturn += t.result
            time.sleep(1)
        return dataReturn

def dataAmazonSellerToCsv(_from,_to):
    data_out = []
    headerCSV = ["Store","Order ID","Product name","Mockup","Size","Quantity","Created","First Name","Last Name","Address","Address2","City","State","Country","Zipcode","Phone","Email","Sup","Design","Line Dreamship","Type 1C"]
    list_account = dataScript.getAccountMerchize(my_mongo)

    for accountIndex,account in enumerate(list_account):
        print(accountIndex, '/', len(list_account), account)
        query = {
            "paid_at":{
                "from":_from,
                "to":_to
            }
        }
        data_out += getData(account, query)


    print("data_out",len(data_out))
    list_data = pd.DataFrame(data_out)

    path = _from.replace("/","_")+"-"+_to.replace("/","_")
    list_data.to_csv(path+'.csv',index=False,columns=headerCSV)

_from ="01/06/2021"
_to ="05/06/2021"
dataAmazonSellerToCsv(_from,_to)
