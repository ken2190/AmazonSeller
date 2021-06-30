import getOrderShopbase
import fulfilMerchize
import getTracking
import importProductShopbase
import time,datetime

while True:
    print("importProductShopbase")
    time.sleep(5)
    importProductShopbase.importShopbae()

    print("getOrderShopbase")
    time.sleep(5)
    getOrderShopbase._run()

    print("fulfilMerchize")
    time.sleep(5)
    fulfilMerchize._run()

    print("getTracking")
    time.sleep(5)
    getTracking._run()

    print(datetime.datetime.now())
    time.sleep(600)

# pm2 start /root/Facebook/_main.py --interpreter python3 --interpreter-args -u --restart-delay 1000