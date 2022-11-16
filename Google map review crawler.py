#!/usr/bin/env python
# coding: utf-8

# 引入套件
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from tqdm.notebook import tqdm
from bs4 import BeautifulSoup

from info_tool import (get_place_name, get_user_rating_total, get_user_name, get_user_profile_url, 
                          get_rating, get_local_guide_and_comment_num, get_comment_text)

from driver_action import click_on_comment_button, scroll_comment_section, expand_full_comment
from utilities import save2csv, drop_no_comment, get_file_already_exist, whether_file_exist, read_csv2df

import pandas as pd
import time
import math
import os

# 讓 pandas 顯示出所有 row，而不會只顯示頭和尾的幾個 row。
pd.set_option('display.max_rows', None)


# 定義取得評論資訊、取得餐廳評論、取得清單中所有餐廳評論的 function 
# 取得評論資訊（評論者、評分、評論內容等...）
def get_all_comment_info(driver):
    comment_info_list = []
    comment_frame_list = driver.find_elements(By.CLASS_NAME,"jftiEf")
    
    # 取得評論進度條
    print('取得評論中...')
    commment_process = tqdm(total=len(comment_frame_list))
    
    for comment_frame in comment_frame_list:
        soup = BeautifulSoup(comment_frame.get_attribute('innerHTML'), "html.parser") 
        
        user_name = get_user_name(soup)  # 取得 user 名稱 
        user_profile_url = get_user_profile_url(soup)  # 取得 user 個人檔案的 URL
        rating = get_rating(soup)  # 取得評級
        local_guide, comment_num = get_local_guide_and_comment_num(soup)  # 取得在地嚮導的狀態和評論數
        comment_text = get_comment_text(soup)# 取得評論內文

        
        comment_info = {
                'user_name': user_name,
                'user_profile_url': user_profile_url,
                'rating': rating,
                'local_guide': local_guide,
                'comment_num': comment_num,
                'comment_text': comment_text
            }

        comment_info_list.append(comment_info)
        commment_process.update(1)

    return comment_info_list

# 取得餐廳評論
def get_restaurant_comment(place_id):
    start_time = time.time()

    options = webdriver.ChromeOptions()
    # options.add_argument('--disable-gpu')   # 如果 window 系統無法正確運作，uncomment 這一行試試看。
    options.add_argument('--headless')  # 讓 Chromedriver 在背景執行
    
    # 前往指定餐廳的 google map 頁面
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = 'https://www.google.com/maps/search/?api=1&query=Google&query_place_id={}'.format(place_id)
    driver.get(url)
    
    # 取得餐廳名稱
    place_name = get_place_name(driver)
    
    # 點擊「評論」按鈕
    click_on_comment_button(driver)
    
    # 滑動評論區塊加載評論
    scroll_comment_section(driver)

    # 展開評論全文
    expand_full_comment(driver)
    
    # 取得所有評論的資訊
    comment_info_list = get_all_comment_info(driver)
    comment_info_list_pd = pd.DataFrame.from_dict(comment_info_list)
    
    # 顯示執行時間
    spending_time = time.time() - start_time
    spending_time = round(spending_time, 2)
    print('執行時間：{} 秒'.format(spending_time))
    
    return comment_info_list_pd, place_name


# 取得清單中所有餐廳的評論
# restaurant_list_csv 的檔名無需帶 '.csv'
def get_all_restaurant_comment(restaurant_list_csv: str): 
    main_start_time = time.time()
    
    # 判斷是否有同名的資料夾，決定是否要創建資料夾。
    exist_file_id_list = whether_file_exist(restaurant_list_csv)
    
    # 讀入餐廳清單 csv 檔
    restaurant_list_df = read_csv2df('/restaurant_spilt_list', restaurant_list_csv)
    
    for i in range(len(restaurant_list_df)):
        place_id = restaurant_list_df['place_id'][i]
        
        # 如果已經有該餐廳的評論資料，便跳過。
        if place_id in exist_file_id_list:
            continue
        
        comment_info_list_df, place_name = get_restaurant_comment(place_id)
        comment_info_list_df = drop_no_comment(comment_info_list_df)
        
        file_name = place_name + "-----" + place_id
        
        save2csv(restaurant_list_csv, comment_info_list_df, file_name)
    
    # 顯示執行時間
    main_spending_time = time.time() - main_start_time
    main_spending_time = round(main_spending_time, 2)
    print('執行時間：{} 秒'.format(main_spending_time))


# 執行
'''
get_all_restaurant_comment() 會從 /restaurant_spilt_list 這個資料夾中讀取指定的餐廳清單。
餐廳的所有評論會存入 /result 資料夾中與餐廳清單同名的資料夾。
在 restaurant_spilt_list 中有 70 份餐廳清單，除了 'restaurant_list70.csv' 之外，所有清單都含有 93 間餐廳的資訊。
如果在爬蟲過程中中斷的話也沒關係，程式會自動確認清單中有哪些餐廳是已經爬過的，而不會重複爬取。
'''
get_all_restaurant_comment('restaurant_list1')

