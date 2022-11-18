from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time


# 取得餐廳名稱
def get_place_name(driver):
    place_name_XPATH = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1'
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, place_name_XPATH)))
    
    place_name = driver.find_element(By.XPATH, place_name_XPATH).text
    place_name = place_name.replace('/', ' ')
    place_name = place_name.replace('|', ' ')

    print('正在獲取{}的評論'.format(place_name))

    return place_name


def get_user_rating_total(driver):
    user_ratings_total_element =  driver.find_element(
                By.CLASS_NAME, 'jANrlb')
    
    user_ratings_soup = BeautifulSoup(user_ratings_total_element.get_attribute('innerHTML'), "html.parser")

    user_ratings_total = int(user_ratings_soup.find('div', class_='fontBodySmall').text.split(' ')[0].replace(',', ''))
    return user_ratings_total
    

# 取得 user 名稱
def get_user_name(soup):
    user_name = soup.find('div', class_ = 'd4r55').text

    return user_name


# 取得 user 個人檔案的 URL
def get_user_profile_url(soup):
    user_profile_url = soup.find('div', class_ = 'WNxzHc qLhwHc').find('a').get('href')
    
    return user_profile_url
    

# 取得評級
def get_rating(soup):
    try:
        rating = soup.find('div', class_ = 'DU9Pgb').find("span", class_="kvMYJc").get("aria-label")
        rating = rating.replace('顆星', '')
        rating = rating.replace(' ', '')
        
    except:
        rating = float('nan')
        
    return rating


# 取得在地嚮導的狀態和評論數
def get_local_guide_and_comment_num(soup):
    try:
        local_guide_and_comment_num = soup.find('div', class_='RfnDt').text.split('·')
        # 判斷是否有「在地嚮導」的稱號
        if len(local_guide_and_comment_num) == 1:
            local_guide = False  # 非為在地嚮導
            comment_num = local_guide_and_comment_num[0]

        elif len(local_guide_and_comment_num) == 2:
            local_guide = True  # 為在地嚮導
            comment_num = local_guide_and_comment_num[1]

        # 去除文字，僅保留數值
        comment_num = comment_num.replace('在地嚮導', '')   
        comment_num = comment_num.replace('則評論', '')
        comment_num = comment_num.replace(' ', '')

    except: 
        local_guide = float('nan')
        comment_num = float('nan')
    
    return local_guide, comment_num
    

# 取得評論內文
def get_comment_text(soup):
    comment_text = soup.find('div' ,class_ = 'MyEned').text
    comment_text = comment_text.replace(' ', '')

    return comment_text


