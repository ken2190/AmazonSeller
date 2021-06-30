import selenium
import my_gologin.gologinSelenium as gologinSelenium
import threading,time,datetime,os

import my_mongo.my_mongo as my_mongo
import my_selenium.get as my_selenium_get
import my_selenium.set as my_selenium_set
import my_selenium.click as my_selenium_click
import my_selenium.generation as my_selenium_generation

# import script.merchAmazon as my_script
# import data.data_amz_merch as data_amz_merch

import data.data_amz_seller as data_amz_amz_seller
import script.amz_seller_script as amz_seller_script

def divide_chunks(l, n): 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

def _run(profile,port,product):
    # Khởi tạo selenium
    (gl,driver)= gologinSelenium.createSelenium(profile,port)
    rootPath = str(os.getcwd()).replace("\\","/")
    amz_seller_script.addCustomize(driver,product,rootPath,my_selenium_set,my_selenium_click)
    # Lấy data hàng ngày
    # try:
        # (data_info_upload,analyze,manage) = my_script.check_data_daily(my_selenium_get,driver,my_selenium_generation)
        # data_amz_merch.updateManage(my_mongo,profile,manage)
        # submitTime = datetime.datetime.now()
        # dataSet = {
        #     "updateTime": submitTime,
        #     "publish": data_info_upload,
        #     "analyze": {},
        # }
        # data_amz_merch.updateAccount(my_mongo,profile["id"],dataSet)
        # data_amz_merch.update_sale(my_mongo,analyze,profile["name"])
    print("time.sleep")
    time.sleep(1)
    # except:
    #     dataSet = {"countError": profile['countError']+1}
    #     data_amz_merch.updateAccount(my_mongo,profile["id"],dataSet)

    # driver.close()
    # gl.stop()
    # print("gl.stop()")

class myThread (threading.Thread):
    def __init__(self, profile,indexThread,product):
        threading.Thread.__init__(self)
        self.profile = profile
        self.indexThread = indexThread
        self.product = product

    def run(self):
        _run(self.profile,5100+self.indexThread,self.product)

# Lấy Danh sách Store
dataStore = data_amz_amz_seller.getAccount(my_mongo)
dataVariant = data_amz_amz_seller.getVariant(my_mongo)
dataProducts = data_amz_amz_seller.getProducts(my_mongo)

dataProducts = list(divide_chunks(dataProducts,4))
print(dataProducts)
for indexList,list_data in enumerate(dataProducts):
    threads=[]
    for indexThread,product in enumerate(list_data):
        profile = product["Account"]
        profile = dataStore[profile]
        product["variants"] = dataVariant[product["ower"]][product["product_type"]]
        indexThread +=indexList*10
        thread = myThread(profile=profile,indexThread=indexThread,product=product)
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()
        print("Finish ",t.profile["id"])


exit(0)
# dataStore = data_amz_merch.getAccount(my_mongo,listStore=["M100"])

#Chia danh sách thành nhóm 10 store
dataStore = list(divide_chunks(dataStore,4))

time.sleep(60)