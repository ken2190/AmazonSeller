import collections
import requests,time,json,pandas as pd
import script.data as dataScript
import my_mongo.my_mongo as my_mongo,pymongo
import datetime
def get_products(page_number):
    key_store = "https://f223e545dbcdd417c34600976a54f9f5:6d934aabfe39eaa27cfebc57e873c423878d906a39501a7b154a9a2e1d43b900@thirdfloor.onshopbase.com"
    url = "/admin/products.json?limit=250&page="+str(page_number)
    url = key_store+url
    print("Goto ",url)
    while True:
        try:
            response = requests.request("GET", url=url, timeout=5).json()
            break
        except Exception as  err:
            print('Time out', err)
            time.sleep(5)

    return ((response['products']))
    try:
        if len(response['products']) > 0:
            return response['orders']
        else:
            return None
    except :
        return None

def _run():
    key_store = "https://f223e545dbcdd417c34600976a54f9f5:6d934aabfe39eaa27cfebc57e873c423878d906a39501a7b154a9a2e1d43b900@thirdfloor.onshopbase.com"
    data = get_orders(1, key_store)
    getID = {}
    data_out = []
    for product in data:
        temp = {
            "id": str(product['id']),
            "title": product['title'],
            "image": product['image']['src'],
        }
        # getID.append(temp)
        getID[temp["image"]] = temp["id"]
        data_out.append(temp)

    df = pd.DataFrame(data_out)
    df.to_csv('18_06_shopbase.csv',index=False)  
    exit(0)
    data = pd.read_csv('data.csv')
    data = data.T.to_dict().values()

    data_out = []
    for item in data:
        temp = {
            "product_id": str(getID[item['image']]),
            "title": item['title'],
            "image": item['image'],
            "design": item['design'],
            "shop" : "thirdfloor",
            "shop_productID" : "thirdfloor_"+str(getID[item['image']])
        }
        data_out.append(temp)
        print(str(getID[item['image']]))

    # print(data_out)
    # dataScript.insertProduct(my_mongo,data_out)
# _run()

def _run2():
    x = ['1000000187376738',
        '1000000190593499',
        '1000000190593502',
        '1000000190593503',
        '1000000190593505',
        '1000000190593511',
        '1000000190593517',
        '1000000190593518',
        '1000000190593519',
        '1000000190593520',
        '1000000190593521',
        '1000000190593522',
        '1000000190593523',
        '1000000190593526',
        '1000000190593527',
        '1000000190593528',
        '1000000190593529',
        '1000000190593533',
        '1000000190593534',
        '1000000190593535',
        '1000000190593536',
        '1000000190593540',
        '1000000190593541',
        '1000000190593542',
        '1000000190593543',
        '1000000190593544',
        '1000000190593545',
        '1000000190593550',
        '1000000190597065',
        '1000000190597079',
        '1000000190597093',
        '1000000190597096',
        '1000000190597103',
        '1000000190597109',
        '1000000190597113',
        '1000000190597118',
        '1000000190597119',
        '1000000190597128',
        '1000000190597130',
        '1000000190597134',
        '1000000190597135',
        '1000000190597142',
        '1000000190597143',
        '1000000190597146',
        '1000000190597147',
        '1000000190597157',
        '1000000190597158',
        '1000000190597159',
        '1000000190597170',
        '1000000190597177',
        '1000000190597178',
        '1000000190597179',
        '1000000190597200',
        '1000000190597201',
        '1000000190597206',
        '1000000190597211',
        '1000000190597212',
        '1000000190597216',
        '1000000190597225',
        '1000000190597230',
        '1000000190597237',
        '1000000190597243',
        '1000000190597249',
        '1000000190597259',
        '1000000190597260',
        '1000000190597263',
        '1000000190597273',
        '1000000190597279',
        '1000000190597297',
        '1000000190597298',
        '1000000190597301',
        '1000000190597308',
        '1000000190597311',
        '1000000190597312',
        '1000000190597313',
        '1000000190597324',
        '1000000190597325',
        '1000000190597331',
        '1000000190597342',
        '1000000190597343',
        '1000000190597345',
        '1000000190597357',
        '1000000190597363',
        '1000000190597369',
        '1000000190616201',
        '1000000190706242',
        '1000000190719494',
        '1000000190733607',
        '1000000190757755',
        '1000000190761503',
        '1000000190764232',
        '1000000190768852',
        '1000000190768853',
        '1000000190768854',
        '1000000190768855',
        '1000000190768856',
        '1000000190768857',
        '1000000190768858',
        '1000000190768861',
        '1000000190768862',
        '1000000190768863',
        '1000000190768864',
        '1000000190768865',
        '1000000190768866',
        '1000000190768867',
        '1000000190768869',
        '1000000190768871',
        '1000000190768872',
        '1000000190768873',
        '1000000190768874',
        '1000000190768876',
        '1000000190768877',
        '1000000190768878',
        '1000000190768879',
        '1000000190768880',
        '1000000190768881',
        '1000000190768882',
        '1000000190768885',
        '1000000190768886',
        '1000000190768887',
        '1000000190768888',
        '1000000190768889',
        '1000000190768890',
        '1000000190768891',
        '1000000190768892',
        '1000000190768893',
        '1000000190768894',
        '1000000190768895',
        '1000000190768896',
        '1000000190768897',
        '1000000190768898',
        '1000000190768901',
        '1000000190768902',
        '1000000190768903',
        '1000000190768904',
        '1000000190768905',
        '1000000190768906',
        '1000000190768907',
        '1000000190768908',
        '1000000190768909',
        '1000000190768910',
        '1000000190768911',
        '1000000190768914',
        '1000000190768915',
        '1000000190768916',
        '1000000190768917',
        '1000000190768918',
        '1000000190768921',
        '1000000190768923',
        '1000000190768924',
        '1000000190768925',
        '1000000190768926',
        '1000000190768929',
        '1000000190768930',
        '1000000190768931',
        '1000000190768932',
        '1000000190768935',
        '1000000190768936',
        '1000000190768938',
        '1000000190768939',
        '1000000190768941',
        '1000000190770894',
        '1000000190773860',
        '1000000190777150',
        '1000000190782266',
        '1000000190796746',
        '1000000190807197',
        '1000000190815233',
        '1000000190826657',
        '1000000190874241',
        '1000000190877095',
        '1000000190879122',
        '1000000190889118',
        '1000000190892976',
        '1000000190896390',
        '1000000190900648',
        '1000000190901946',
        '1000000190905189',
        '1000000190908283',
        '1000000190910556',
        '1000000190912609',
        '1000000190914545',
        '1000000190916341',
        '1000000190918204',
        '1000000190920570',
        '1000000190922636',
        '1000000190924149',
        '1000000190932183',
        '1000000190936893',
        '1000000195660684',
        '1000000195734389',
        '1000000195735918',
        '1000000195743445',
        '1000000195748378',
        '1000000195749561',
        '1000000195754116',
        '1000000197457159',
        '1000000197473091',
        '1000000197498547',
        '1000000197794861',
        '1000000198268567',
        '1000000198276027',
        '1000000198411088',
        '1000000198414539',
        '1000000198883493',
        '1000000198891855',
        '1000000198899255',
        '1000000198906832',
        '1000000198907187',
        '1000000198974538',
        '1000000198977054',
        '1000000198989245',
        '1000000199004824',
        '1000000199007562',
        '1000000199007906',
        '1000000199010851',
        '1000000199013403',
        '1000000199016403',
        '1000000199017008',
        '1000000199020388',
        '1000000199026375',
        '1000000199026528',
        '1000000199026552',
        '1000000199026656',
        '1000000199546870',
        '1000000199605138',
        '1000000199661675',
        '1000000199662701',
        '1000000199663170',
        '1000000199663466',
        '1000000199664058',
        '1000000199664284',
    ]
    data_1 = get_products(1)
    data_2 = get_products(2)
    data = data_1+data_2
    print(len(data))
    mydata = dataScript.getProductsImportShopbase(my_mongo,query={"design":{"$exists":1}})
    mydata = [i['product_id'] for i in mydata]
    data = [i for i in data if str(i['id']) not in mydata and str(i['id']) not in x]
    print(len(data))
    for product in data:
        id = str(product['id'])
        title = product['title'].replace(",","")
        image = product['image']['src']
        print(','.join([id,title,image]))

def _run3():
    data = pd.read_csv('./csv/ImportProducts.csv')
    data = data.T.to_dict().values()
    listID = [str(i['id']) for i in data]

    listOldID = []
    for item in dataScript.getProductsImportShopbase(my_mongo,query={
        "product_id":{"$in":listID}
        # "design":{"$exists":0}
        }):
        listOldID.append(item[str("product_id")])

    print(len(listID))
    print(len(listOldID))
    index=0

    data_out = []
    for item in data:
        if str(item['id']) not in listOldID:
            index+=1
            print(index,str(item['id']))

            temp = {
                "product_id" :str(item['id']),
                "title" : str(item['title']),
                "image" : str(item['image']),
                "shop" : "thirdfloor",
                "shop_productID" : "thirdfloor_"+str(item['id'])
            }
                # "design" : "https://trello-attachments.s3.amazonaws.com/60c714a9793cd250c8360fc7/60c7196ee30212820fb03fcb/7311cd92b386176a122b7dfec84bf4e3/Boxer-Hawaii-Merch.png",
            if str(item["design_1"]) != "nan":
                # print(str(item["design_1"]))
                temp["product_type"] = item['product_type']
                if item['product_type'] != "Flag":
                    print(item['product_type'])
                    temp["design"] =  str(item["design_1"])
                else:
                    data_type = {
                        "design_1":"Garden flag",
                        "design_2":"House flag",
                        "design_3":"Wall flag",
                    }
                    temp["design"] = {}
                    for key in data_type:
                        if str(item[key]) != "nan":
                            temp["design"][data_type[key]] = str(item[key])
                data_out.append(temp)
    print("data_out",len(data_out))
    # dataScript.insertProduct(my_mongo,data_out)

def _run4():
    mydata = dataScript.getProductsImportShopbase(my_mongo,query={"design":{"$exists":1}})
    myID = {str(i['product_id']):i for i in mydata}

    data_1 = get_products(1)
    data_2 = get_products(2)
    data = data_1+data_2
    data_out = []
    for item in data:
        temp = {
            "id": str(item["id"]),
            "image": item["image"]["src"],
            "title": item["title"]
        }
        if temp["id"] in myID:
            if myID[temp["id"]]["product_type"] == "Flag":
                temp.update(myID[temp["id"]]["design"])
            else:
                temp["design"] = (myID[temp["id"]]["design"])
                print(temp)
        data_out.append(temp)
    print(len(data_out))
    df = pd.DataFrame(data_out)
    df.to_csv('shopbase.csv',index=False)

def create_mongo(ip, MONGO_DB):
    from sshtunnel import SSHTunnelForwarder

    # [server, myclient, mydb] = create_mongo("173.249.11.123", "Facebook")

    data = {
        "173.249.11.123": {
            "MONGO_USER" : "root",
            "MONGO_PASS" : "tumotdenchin",
        }
    }

    MONGO_HOST = ip
    MONGO_USER = data[ip]["MONGO_USER"]
    MONGO_PASS = data[ip]["MONGO_PASS"]
    MONGO_DB = MONGO_DB

    server = SSHTunnelForwarder(
        MONGO_HOST,
        ssh_username=MONGO_USER,
        ssh_password=MONGO_PASS,
        remote_bind_address=('127.0.0.1', 27017)
    )

    server.start()

    client = pymongo.MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port
    db = client[MONGO_DB]

    return [server, client, db]

[server, myclient, mydb] = create_mongo("173.249.11.123", "Facebook")
old_myclient =  my_mongo.create_mongo()
_collections = "Products"

mydata = my_mongo.find(old_myclient,"Facebook",_collections,{})
print(len(mydata))
mydb[_collections].insert_many(mydata)
exit(0)
query = { 
    "tracking" : {
        "$exists": 1
    },
    "id_order": 'thirdfloor_9712241'
}
# Danh sach order chua sysc
listOrder = dataScript.getOrderSendTrackingShopbase(my_mongo,query=query)
for order in listOrder:
    date_created = datetime.datetime.strptime(order['date_created'].split("+")[0], '%Y-%m-%dT%H:%M:%S')
    print(date_created)
    print(date_created+datetime.timedelta(days = 30)< datetime.datetime.now())
    exit(0)

print(len(listOrder))
data = pd.read_csv('data2.csv')
data = data.T.to_dict().values()

data_out = []
for item in data:
    # temp = {
    #     "product_id": str([item['image']]),
    #     "title": item['title'],
    #     "image": item['image'],
    #     "design": item['design'],
    #     "shop" : "thirdfloor",
    #     "shop_productID" : "thirdfloor_"+str([item['image']])
    # }
    # data_out.append(temp)

    temp = {
        "product_id" :str(item['id']),
        "title" : str(item['title']),
        "image" : str(item['image']),
        "shop" : "thirdfloor",
        "shop_productID" : "thirdfloor_"+str(item['id'])
    }
        # "design" : "https://trello-attachments.s3.amazonaws.com/60c714a9793cd250c8360fc7/60c7196ee30212820fb03fcb/7311cd92b386176a122b7dfec84bf4e3/Boxer-Hawaii-Merch.png",
    if str(item["design_1"]) != "nan":
        # print(str(item["design_1"]))
        temp["product_type"] = item['product_type']
        if item['product_type'] != "Flag":
            print(item['product_type'])
            temp["design"] =  str(item["design_1"])
        else:
            data_type = {
                "design_1":"Garden flag",
                "design_2":"House flag",
                "design_3":"Wall flag",
            }
            temp["design"] = {}
            for key in data_type:
                if str(item[key]) != "nan":
                    temp["design"][data_type[key]] = str(item[key])
        data_out.append(temp)

dataScript.insertProduct(my_mongo,data_out)
  # print(str(item['id']),str(item['product_type']))
