#Import all the libraries. I have used selenium to individually load and capture data from each file.
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

#Set-up all the elements of opening and closing the webpage.
driver = webdriver.Chrome(executable_path='C:\\Users\\ARYAN\\Downloads\\chromedriver')
url = 'https://www.amazon.in/alm/category/?_encoding=UTF8&almBrandId=ctnow&node=4859479031&pf_rd_p=cefc1b78-88f9-45f8-bbd6-24e2f5e8980d&pf_rd_r=HNCTW1AQC1126WYHERZ8&pf_rd_s=nowstore-desktop-food-content-1&pf_rd_t=SubnavFlyout&ref_=sn_gfs_co_nowstore-subnav-food_Ce_2'
a = ActionChains(driver)
driver.get(url)
driver.maximize_window()

#Short loop to find all the categories on the home page.
categories = driver.find_elements_by_class_name('a-size-large')
print('Loading the page...')
for cat in categories:
    a.move_to_element(cat).perform()
    cat.click()
    driver.implicitly_wait(1)

#Main loop where all the items are found, stored and printed.
print('Finding the elements...')
for cat, l in zip(categories, range(0, len(categories))):
    temp = cat.text.strip().split('See')[0]
    print("Category: {}".format(temp))
    head = driver.find_element_by_id('anonCarousel{}'.format(l+1))
    child = head.find_elements_by_xpath('//*[@id="anonCarousel{}"]/ol'.format(l+1))
    #As there are many categories we are looping over, I've used the ID to separate each category with its different items.
    catalogue = []
    for c in child:
        prod = []
        link = []
        products = c.find_elements_by_xpath('./child::*')
        for p in products:
            if p.text.strip() != '':
                prod.append(p.text.strip().split(',' or  '|' or ':')[0])
        
        for i in range(1,8):
            href = c.find_elements_by_xpath('//*[@id="anonCarousel{}"]/ol/li[{}]/div[1]/div[3]/a'.format((l+1), i))
            for h in href:
                s = h.get_attribute('href')
                if s != '':
                    link.append(s)
            
        details = {'Name':prod, 'Link':link}
        df = pd.DataFrame(details)
        #print(df)
        
        li = df['Link']
        for l in li:
            driver.execute_script("window.open('%s', '_blank')" % l)
            driver.switch_to.window(driver.window_handles[1])
            driver.implicitly_wait(5)
            
            #We've used the try-except blocks for avoiding any errors or any missing entries.
            try:
                id = driver.find_element_by_xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody/tr[1]/td')
            except:
                id = driver.find_element_by_xpath('//*[@id="detailBullets_feature_div"]/ul/li[5]/span/span[2]')
            Title = driver.find_element_by_xpath('//*[@id="productTitle"]')
            try: 
                MRP = driver.find_element_by_xpath('//*[@id="almDetailPagePrice_basis_price"]/td[2]/span')
            except:
                MRP = 'None'
            try: 
                Price = driver.find_element_by_xpath('//*[@id="priceblock_ourprice"]')
            except:
                Price = 'None'
            try:
                Availibility = driver.find_element_by_xpath('//*[@id="availability-string"]/span')
            except:
                Availibility = 'None'
            try:
                place = driver.find_element_by_xpath('//*[@id="fresh-merchant-info"]/a')
            except:
                place = 'None'

            #Pardon the naming, this is just to make it easier to understand.
            a = id.text.strip()
            b = Title.text.strip()
            if MRP != 'None': 
                c = MRP.text.strip().split('₹')[1]
            else:
                c = MRP
            if Price != 'None':
                d = Price.text.strip().split('₹')[1]
            else:
                d = Price
            if Availibility != 'None':
                e = Availibility.text.strip()
            else:
                e = Availibility
            if place != 'None':
                f = place.text.strip()
            else:
                f = place
            
            catalogue.append({'ID':a, 'Name':b, 'MRP':c, 'Price to Customer':d, 'Availibility':e, 'Listing Place':f})

            driver.close()
            driver.switch_to.window(driver.window_handles[0])     
        
        for item in catalogue:
            print(item)
