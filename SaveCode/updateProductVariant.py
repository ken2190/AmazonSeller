import requests,time,json,pandas as pd
import script.data as dataScript
import my_mongo.my_mongo as my_mongo

def getProduct(key_store, productID):
    url = "/admin/products/"+str(productID)+".json"
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
        if "id" in response['product']:
            return response['product']
        else:
            return None
    except :
        return None

list_account = dataScript.getAccountShopbase(my_mongo)
list_accountToken = {i['sub_domain']:i for i in list_account}

data = pd.read_csv('./csv/ProductType.csv')
data = data.T.to_dict().values()

design_len = 3
data_out = []
for item in data:
    temp = {
        "productType" :str(item['productType']),
        "SKU Variants" : str(item['SKU Variants']),
        "productID" : str(item['productID']),
        "shop" : str(item['shop']),
        "tags" : str(item['tags']),
    }

    tempDesign = {}
    for key in range(1,design_len+1):
        key = "design_"+str(key)
        if str(item[key]) != "nan":
            tempDesign[key] = item[key]
    
    if len(tempDesign) > 0:
        temp['design'] = tempDesign

    productClone = getProduct(list_accountToken[temp['shop']]['url'], temp['productID'])
    for option in productClone["options"]:
        del option['product_id']

    for variant in productClone["variants"]:
        del variant['attachment']
        del variant['created_at']
        del variant['id']
        del variant['image_id']
        del variant['image_src']
        del variant['metafields']
        del variant['product_id']
        del variant['sync_cache_time']
        del variant['updated_at']

    template = {
        "product": {
            "body_html": productClone["body_html"],
            "custom_options": productClone["custom_options"],
            "display_options": productClone["display_options"],
            "handle": "",
            "images": [ ],
            "metafields_global_description_tag": productClone["metafields_global_description_tag"],
            "metafields_global_title_tag": productClone["metafields_global_title_tag"],
            "options": productClone["options"],
            "product_availability": productClone["product_availability"],
            "product_type":productClone["product_type"],
            "published":productClone["published"],
            "published_at": 0,
            "tags": productClone["tags"],
            "title": "",
            "variants": productClone["variants"],
            "vendor":productClone["vendor"],
        }
    }

    temp['shopbaseProductTemplate'] = template
    data_out.append(temp)
    time.sleep(2)

dataScript.removeAllVariant(my_mongo)
dataScript.insertVariant(my_mongo,data_out)
