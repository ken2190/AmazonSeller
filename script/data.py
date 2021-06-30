import datetime
#GET
def getAccountShopbase(my_mongo,listStore=None,limit=0):
    myclient = my_mongo.create_mongo()
    if listStore is None:
        query = {
            "source" : "shopbase"
        }
    else:
        query = {
            "source" : "shopbase",
            "sub_domain": {"$in":listStore},
        }

    # query = {}
    data = my_mongo.find(myclient,"AmazonSeller","Accounts",query,{"sub_domain":1,"url":1,"_id":1},limit=limit)
    # data = my_mongo.find(myclient,"amz_merch","Account",{"status":"Active","name":'M75',"dataTimeZone":{"$exists":1}},{"name":1,"id":1,"_id":0,"dataTimeZone":1})
    my_mongo.close_mongo(myclient)

    return data

def getAccountMerchize(my_mongo,listStore=None,limit=0):
    myclient = my_mongo.create_mongo()
    if listStore is None:
        query = {
            "source" : "merchize"
        }
    else:
        query = {
            "source" : "merchize",
            "sub_domain": {"$in":listStore},
        }
    data = my_mongo.find(myclient,"AmazonSeller","Accounts",query,{"base_url":1,"access-token":1,"_id":1},limit=limit)
    my_mongo.close_mongo(myclient)

    return data

def getOrderShopbaseCheck(my_mongo,listIn=None,query=None,listNotIn=None,limit=0):
    myclient = my_mongo.create_mongo()
    if query is None:
        query = {}
        if listIn is not None:
            query["id_order"] = {"$in":listIn}

    # query = {}
    data = my_mongo.find(myclient,"AmazonSeller","Orders",query,{"id_order":1,"_id":1},limit=limit)
    # data = my_mongo.find(myclient,"amz_merch","Account",{"status":"Active","name":'M75',"dataTimeZone":{"$exists":1}},{"name":1,"id":1,"_id":0,"dataTimeZone":1})
    my_mongo.close_mongo(myclient)

    return data


def getOrderShopbaseSendMerchize(my_mongo,listIn=None,query={},listNotIn=None,limit=0):
    myclient = my_mongo.create_mongo()
    # if query is None:
    # query = {}
    if listIn is not None:
        query["id_order"] = {"$in":listIn}
    
    projection = {
    }
    data = my_mongo.find(myclient,"AmazonSeller","Orders",query,projection,limit=limit)
    my_mongo.close_mongo(myclient)

    return data

def getAllVariant(my_mongo,query={},limit=0):
    myclient = my_mongo.create_mongo()
    projection= {}
    data = {}
    for item in  my_mongo.find(myclient,"AmazonSeller","ProductVariants",query,projection,limit=limit):
        if item['shop'] not in data:
            data[item['shop']] = {}
        product_type = item['productType']
        data[item['shop']][product_type] = item
    my_mongo.close_mongo(myclient)
    return data

def getOrderShopbaseGetTrackingMerchize(my_mongo,listIn=None,query=None,listNotIn=None,limit=0):
    myclient = my_mongo.create_mongo()
    if query is None:
        query = {}
        if listIn is not None:
            query["id_order"] = {"$in":listIn}
    
    projection = {
        "_id":1,
        "shopbase_name":1,
    }
    data = []
    for item in my_mongo.find(myclient,"AmazonSeller","Orders",query,projection,limit=limit):
        item["shopbase_name"] = item["shopbase_name"][1:]
        data.append(item)
    my_mongo.close_mongo(myclient)

    return data

def getOrderSendTrackingShopbase(my_mongo,listIn=None,query=None,listNotIn=None,limit=0):
    myclient = my_mongo.create_mongo()
    if query is None:
        query = {}
        if listIn is not None:
            query["id_order"] = {"$in":listIn}
    
    projection = {
        "_id":1,
        "id":1,
        "list_product":1,
        "tracking":1,
        "id_order":1,
        "date_created":1,
    }
    data = []
    for item in my_mongo.find(myclient,"AmazonSeller","Orders",query,projection,limit=limit):
        data.append(item)
    my_mongo.close_mongo(myclient)

    return data

def getProductsImportShopbase(my_mongo,query={},limit=0):
    myclient = my_mongo.create_mongo()
    data = my_mongo.find(myclient,"AmazonSeller","Products",query,{},limit=limit)
    my_mongo.close_mongo(myclient)

    return data

def checkListHanle(my_mongo,query={},limit=0):
    myclient = my_mongo.create_mongo()
    data = []
    for item in my_mongo.find(myclient,"AmazonSeller","Products",query,{"handle":1},limit=limit):
        data.append(item['handle'])
    my_mongo.close_mongo(myclient)
    return data

#SET
def updateOrder(my_mongo,order_id,dataSet):
    myclient = my_mongo.create_mongo()
    my_mongo.update(myclient,"AmazonSeller","Orders",{"_id":order_id},dataSet)
    my_mongo.close_mongo(myclient)

def updateProduct(my_mongo,product_id,dataSet):
    myclient = my_mongo.create_mongo()
    my_mongo.update(myclient,"AmazonSeller","Products",{"_id":product_id},dataSet)
    my_mongo.close_mongo(myclient)

#INSERT
def insertOrder(my_mongo,list_orders):
    myclient = my_mongo.create_mongo()
    my_mongo.insert(myclient,"AmazonSeller","Orders",list_orders,multi=True)
    my_mongo.close_mongo(myclient)

def insertProduct(my_mongo,list_products):
    myclient = my_mongo.create_mongo()
    my_mongo.insert(myclient,"AmazonSeller","Products",list_products,multi=True)
    my_mongo.close_mongo(myclient)

def insertVariant(my_mongo,list_products):
    myclient = my_mongo.create_mongo()
    my_mongo.insert(myclient,"AmazonSeller","ProductVariants",list_products,multi=True)
    my_mongo.close_mongo(myclient)

#Remove
def removeAllVariant(my_mongo):
    myclient = my_mongo.create_mongo()
    my_mongo.remove(myclient,"AmazonSeller","ProductVariants",{})
    my_mongo.close_mongo(myclient)


#Script
def getProductDesign(my_mongo,listOrder):
    list_product = []
    listProductsKey = []
    for order in listOrder:
        for product in order['list_product']:
            if product['product_id'] not in list_product:
                list_product.append(product['product_id'])
                listProductsKey.append(order["shop"]+"_"+str(product['product_id']))

    myclient = my_mongo.create_mongo()
    query = {
        "shop_productID": {"$in":listProductsKey},
        "design": {"$exists":1}
    }
    # query = {}
    print("query",query)
    data = {}
    for product in my_mongo.find(myclient,"AmazonSeller","Products",query,{"shop_productID":1,"design":1,"product_type":1}):
        data[product["shop_productID"]] = product
    my_mongo.close_mongo(myclient)

    return data

