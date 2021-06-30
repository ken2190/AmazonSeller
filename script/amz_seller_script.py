import time,json,requests,os
from PIL import Image

def get_info_upload(driver, my_selenium_get):
    driver.get("https://merch.amazon.com/dashboard")
    temp = {
        'AVAILABLE SUBMISSIONS': my_selenium_get.get_value(driver,"account-status-v2 div.card-body > div > div:nth-child(1) .progress-summary span","text"),
        'PUBLISHED PRODUCTS': my_selenium_get.get_value(driver,"account-status-v2 div.card-body > div > div:nth-child(2) .progress-summary span","text"),
        'TIER': my_selenium_get.get_value(driver,"account-status-v2 div.card-body > div > div:nth-child(3) .progress-summary span","text"),
    }
    return temp

def check_data_daily(my_selenium_get, driver,my_selenium_generation):
    #Get info_upload
    data_info_upload = get_info_upload(driver, my_selenium_get)
    print("data_info_upload",data_info_upload)

    #Get Sales
    analyze = my_selenium_get.get_analyze(driver,my_selenium_generation)

    accountId = get_account_id(driver)
    print("accountId",accountId)
    
    #Get Design Status
    manage = my_selenium_get.get_manage(driver,my_selenium_generation,accountId)
    return (data_info_upload,analyze,manage)

def get_account_id(driver):
    for item in driver.find_elements_by_css_selector("script"):
        if "accountId" in item.get_attribute('innerHTML'):
            accountIdText = item.get_attribute('innerHTML')
            accountId = accountIdText.split('accountId":')[1].split('"')[1]
            return accountId

def addCustomize(driver,product,rootPath,my_selenium_set,my_selenium_click):
    driver.get("https://sellercentral.amazon.com/gestalt/managecustomization/index.html?sku="+str(product['sku']))
    (imageStatus,imagePath) = check_size(product)
    print(imageStatus,imagePath)
    if imageStatus:
        imagePath = rootPath+"/"+imagePath
        print(imagePath)
        #Import Image
        my_selenium_set.set_elem(driver,".drop-child-container input", "send_keys", imagePath)
        print(".sleep(10)")
        time.sleep(10)
        #Click more Option
        driver.execute_script("document.querySelector(\"[label='Add customization']\").scrollIntoView();")
        my_selenium_click.click_elem(driver,"[label='Add customization'] button",3)

        #Click option dropdown
        my_selenium_click.click_elem(driver,".choice-item__2xajw:nth-child(3)",2)
        #Confirm
        my_selenium_click.click_elem(driver,"kat-modal [label='Add customization'] button",3)

        #delete clone variant
        my_selenium_click.click_elem(driver,"[data-test-id=compact-option-list] [name=delete]",2)
        my_selenium_click.click_elem(driver,"[data-test-id=compact-option-list] [name=delete]",2)

        #Them option variant
        my_selenium_click.click_elem(driver,".compact-option-list-header__1MlEi .add-multiple-text__31prv",2)

        optionValueName = ",".join([i['Size'] for i in product["variants"]['variant']])
        my_selenium_set.set_elem(driver,"textarea[placeholder='Enter options']", "send_keys", optionValueName)

        time.sleep(1)
        my_selenium_click.click_elem(driver,".button-add-multiple__wZIZ5 button",2)

        for vatiantIndex,variant in enumerate(product["variants"]['variant']):
            css_vatiant = "[data-test-id=compact-option-list] [data-rbd-droppable-id] [data-rbd-draggable-context-id]:nth-child("+str(vatiantIndex+1)+") "
            css_vatiant += ".price-input input"
            value_variant = variant["Difference"]

            print(css_vatiant,value_variant)
            css_selector = css_vatiant
            driver.execute_script("document.querySelector(\""+css_selector+"\").scrollIntoView();")
            driver.find_element_by_css_selector(css_selector).clear()
            my_selenium_set.set_elem(driver,css_selector, "send_keys", value_variant)
            
            # my_selenium_set.set_elem(driver,css_vatiant, "send_keys", value_variant)
            str_script = "document.querySelector('"+css_vatiant+"').value = '"+str(value_variant)+"';"
            print("str_script",str_script)
            # driver.execute_script(str_script)
            time.sleep(0.5)

        
        #Click more Option
        driver.execute_script("document.querySelector(\"[label='Add customization']\").scrollIntoView();")
        my_selenium_click.click_elem(driver,"[label='Add customization'] button",3)

        #Click Data
        my_selenium_click.click_elem(driver,".choice-item__2xajw:nth-child(2)",2)
        #Confirm
        my_selenium_click.click_elem(driver,"kat-modal [label='Add customization'] button",3)


        css_selector = ".child-content__Vveby .text-input-label[value='Data 1'] input"
        script_ = "document.querySelector(\""+css_selector+"\").scrollIntoView();"
        print("\n",script_,"\n")
        driver.execute_script(script_)
        driver.find_element_by_css_selector(css_selector).clear()
        my_selenium_set.set_elem(driver,".child-content__Vveby .text-box-with-error input[placeholder=Label]", "send_keys", "Customized your text")
        # driver.execute_script("document.querySelector('.child-content__Vveby .text-input-label[value=\"Data 1\"] input').value='Customized your text';")
        time.sleep(1)

        css_selector = ".child-content__Vveby .text-input-label[value='Option Dropdown 1'] input"
        driver.execute_script("document.querySelector(\""+css_selector+"\").scrollIntoView();")
        driver.find_element_by_css_selector(css_selector).clear()
        my_selenium_set.set_elem(driver,".child-content__Vveby .text-box-with-error input[placeholder=Label]", "send_keys", "Choose your size")
        # driver.execute_script("document.querySelector('.child-content__Vveby .text-input-label[value=\"Option Dropdown 1\"] input').value='Choose your size';")
        time.sleep(1)

        #Publish
        my_selenium_click.click_elem(driver,"#gc-control-panel .save-button button",3)
        

def check_size(product):
    path = 'product_image/'+str(product['sku'])+"."+product['image'].split("?")[0].split(".")[-1]
    download_image(product['image'],path)

    image = Image.open(path)
    (width, height) = image.size
    return (width == height,path)

def download_image(pic_url,path):
    os.system("rm product_image/*")
    with open(path, 'wb') as handle:
        response = requests.get(pic_url, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)


