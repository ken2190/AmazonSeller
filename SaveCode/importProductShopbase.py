import requests,time,json,pandas as pd
import script.data as dataScript
import my_mongo.my_mongo as my_mongo
import threading

class myThread (threading.Thread):
    def __init__(self, key_store,variantID,template):
        threading.Thread.__init__(self)
        self.key_store = key_store
        self.variantID = variantID
        self.template = template

    def run(self):
        updateVariant(key_store=self.key_store, variantID=self.variantID, template=self.template)

def updateVariant(key_store, variantID, template):
    url = "/admin/variants/"+str(variantID)+".json"
    url = key_store+url
    headers = {
        "Content-Type": "application/json"
    }
    print("Goto ",url)
    while True:
        try:
            requests.request("PUT", url=url,headers=headers,data=json.dumps(template), timeout=5).json()
            break
        except Exception as  err:
            print('Time out', err)
            time.sleep(5)

def createProduct(key_store, template):
    url = "/admin/products.json"
    url = key_store+url

    headers = {
        "Content-Type": "application/json"
    }
    print("Goto ",url)
    while True:
        try:
            response = requests.request("POST", url=url,headers=headers,data=json.dumps(template), timeout=5).json()
            break
        except Exception as  err:
            print('Time out', err)
            time.sleep(5)


    try:
        if "id" in response['product']:
            return response['product']
        else:
            return None
    except :
        return None

def importCSV():
    print("importCSV")
    #Get data variants
    dataVariant = dataScript.getAllVariant(my_mongo)

    data = pd.read_csv('./csv/Template_ImportProducts.csv')
    data = data.T.to_dict().values()

    data_out = []
    checkListHanle = []
    for item in data:
        temp = {
            "title" :str(item['title']),
            "product_type" : str(item['product_type']),
            "shop" : str(item['shop']),
            "handle" : str(item['handle']),
            "tags" : str(item['tags']),
        }
        checkListHanle.append(str(item['handle']))

        #Product Design
        if "design" in dataVariant[temp['shop']][temp['product_type']]:
            temp["design"] = {}
            tempDesign = dataVariant[temp['shop']][temp['product_type']]['design']
            for key in tempDesign:
                if key in item:
                    temp["design"][tempDesign[key]] = item[key]
        else:
            temp["design"] = item["design_1"]

        #Product Images
        temp["image"] = {
            "main": item['image_main'],
        }
        if "design" in dataVariant[temp['shop']][temp['product_type']]:
            temp["image"]["thumb"] = {}

            tempDesign = dataVariant[temp['shop']][temp['product_type']]['design']
            for key in tempDesign:
                if key in item:
                    if str(item[key.replace("design","image")])  !='nan':
                        temp["image"]["thumb"][tempDesign[key]] = item[key.replace("design","image")]
                
        else:
            temp["image"]["thumb"] = []

            for key in item:
                if "image_" in key and key != "image_main":
                    if str(item[key]) != "nan":
                        temp["image"]["thumb"].append(item[key])
        # print(temp["image"]["thumb"])
        data_out.append(temp)

    # check Duplicate
    myListHanle = dataScript.checkListHanle(my_mongo,{"handle":{"$in": checkListHanle}})
    print("data_out", len(data_out))
    data_out = [i for i in data_out if i["handle"] not in myListHanle]
    print("data_out", len(data_out))

    if len(data_out)>0:
        dataScript.insertProduct(my_mongo,data_out)

def importShopbae():
    print("importShopbae")
    #Get data Token
    list_account = dataScript.getAccountShopbase(my_mongo)
    list_accountToken = {i['sub_domain']:i for i in list_account}

    #Get data variants
    dataVariant = dataScript.getAllVariant(my_mongo)

    query = {
        "sync_shopbase": {"$exists":0},
        "product_id": {"$exists":0},
        "oldProduct": {"$exists":0}
    }
    list_products = dataScript.getProductsImportShopbase(my_mongo,query)
    for productIndex,product in enumerate(list_products):
        template = dataVariant[product['shop']][product['product_type']]['shopbaseProductTemplate']
        templateProduct = template['product']

        #title
        templateProduct['title'] = product['title']
        #handle
        print(product)
        templateProduct['handle'] = product['handle']
        #tags
        _tags = dataVariant[product['shop']][product['product_type']]['tags']+","+product['tags']
        templateProduct['tags'] = _tags.replace(",,",",")
        #image
        listImage= [product['image']['main']]
        images= []
        imagePosion = {}

        for img in product['image']['thumb']:
            try:
                # print(img,product['image']['thumb'][img] not in listImage)
                if product['image']['thumb'][img] not in listImage:
                    listImage.append(product['image']['thumb'][img])
            except:
                if img not in listImage:
                    listImage.append(img)
        print(productIndex,len(list_products),listImage)
        images= []
        for _index,image in enumerate(listImage):
            images.append({
                "position": _index+1,
                "src": image,
            })
            if "design" in dataVariant[product['shop']][product['product_type']]:
                for img in product['image']['thumb']:
                    if image == product['image']['thumb'][img]:
                        imagePosion[img] = _index+1

        templateProduct['images'] = images

        #Import product shopbase
        responseProduct = createProduct(key_store=list_accountToken[product['shop']]['url'],template=template)
        if "design" in dataVariant[product['shop']][product['product_type']]:
            print(imagePosion)
            threads=[]
            for _variant in responseProduct['variants']:
                variantName = _variant['option1']
                variantID = _variant['id']
                if variantName in imagePosion:
                    _position = imagePosion[variantName]
                    imageID = [i['id'] for i in responseProduct['images'] if i['position'] == _position][0]
                    template = {
                        "duplicate_from_variant": True,
                        "variant": {
                            "image_id": imageID,
                        }
                    }
                    _variant['image_id'] = imageID

                    thread = myThread(key_store=list_accountToken[product['shop']]['url'], variantID=variantID, template=template)
                    thread.start()
                    threads.append(thread)
            
            for t in threads:
                t.join()

        dataScript.updateProduct(my_mongo,product['_id'],{
            "sync_shopbase":responseProduct,
            "product_id":str(responseProduct["id"]),
            "shop_productID":str(product['shop'])+"_"+str(responseProduct["id"]),
            })

# importShopbae()
# importCSV()
