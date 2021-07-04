
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from tqdm.notebook import tqdm
import re
import math



options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/opt/homebrew/bin/chromedriver',options=options) 


def getStars(STARs, IDs):
  stars = driver.find_elements_by_css_selector('#cdtl_cmt_tbody td.star > div > span > span > span > em')
  ids = driver.find_elements_by_css_selector('#cdtl_cmt_tbody td.user > div')
    
  for star in stars:
      STARs.append(int(star.text))
  for ID in ids:
      IDs.append(re.sub('[*]', '', ID.text))

  return STARs,IDs


code = 'A01' ## 과일 

keyword = ['사과','바나나','참외','키위','포도','복숭아','자두','수박','멜론','토마토','귤','오렌지','블루베리','자몽']
items = {}
reviews = {}
store_info = []

for key in range(len(keyword[:1])):

  img_arr = []
  name_arr = []
  price_arr = []
  star_arr = []
  origin_arr = []
  number_arr = []
  store_arr = []
  code_arr = []

  url="http://emart.ssg.com/search.ssg?target=all&query=%EA%B3%BC%EC%9D%BC&include={}&ctgId=6000095739&ctgLv=1".format(keyword[key])

  driver.get(url)
  driver.implicitly_wait(4) # 암묵적으로 웹 자원을 (최대) 3초 기다리기

  links = driver.find_elements_by_css_selector('div.cunit_info > div.cunit_md.notranslate > div > a') ## 

  length = 0
  if len(links)>=5:
    length = 5
  else:
    length = len(links)

  for i in range(2):
    links[i].send_keys(Keys.COMMAND +"\n")
    time.sleep(4)
    driver.switch_to.window(driver.window_handles[-1])
    
    img = driver.find_element_by_css_selector('#mainImg').get_attribute("src")
    name = driver.find_element_by_css_selector('div.cdtl_cm_detail.ty_ssg.react-area > div.cdtl_row_top > div.cdtl_col_rgt > div.cdtl_prd_info > h2').text

    stars = driver.find_element_by_css_selector('#content > div.cdtl_cm_detail.ty_ssg.react-area > div.cdtl_row_top > div.cdtl_col_lft > div.cdtl_lst > div:nth-child(1) > div > dl > dd > div > a > div > span.cdtl_grade_num > em')
    origin = driver.find_element_by_css_selector('div.cdtl_cont_info > div > table > tbody > tr:nth-child(5) > td > div').text

    number = driver.find_element_by_css_selector('div.cdtl_cont_info > div > table > tbody > tr:nth-child(12) > td > div').text

    name = name.split('\n')[0]
    name_arr.append(name)
    img_arr.append(img)
    star_arr.append(stars.text)
    origin_arr.append(origin)
    number_arr.append(number)
    store_arr.append(name.split()[0])
  
    name = re.sub('[()]','',name)
    priceTag = driver.find_element_by_css_selector('#content > div.cdtl_cm_detail.ty_ssg.react-area > div.cdtl_row_top > div.cdtl_col_rgt > div.cdtl_info_wrap > div.cdtl_optprice_wrap > div > span.cdtl_new_price.notranslate > em').text.replace(',','')
    
    if re.search('kg', name) == None:
      price = (int(priceTag)/int(name.split('g')[0].split()[-1])) * 100
  
    else:
      price = int((int(priceTag)/ math.floor((float(name.split('kg')[0].split()[-1]))*1000)) * 100)
      

    price_arr.append(price)


    STARs = []
    IDs = []
    STARs, IDs = getStars(STARs, IDs)

    driver.find_element_by_css_selector('#comment_navi_area > a:nth-child(2)').click()
    time.sleep(1)

    STARs, IDs = getStars(STARs, IDs)
    reviews[i] = STARs, IDs


    detail_code = str(key+1).zfill(4)
    code_arr.append(code + detail_code)

    store_info.append(name.split()[0]+' '+number)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)

  items['code'] = code_arr
  items['name'] = name_arr
  items['price'] = price_arr
  items['origin'] = origin_arr
  items['star'] = star_arr
  items['img'] = img_arr
  items['store'] = store_arr
  




print(items)
print(reviews)
print(store_info)

