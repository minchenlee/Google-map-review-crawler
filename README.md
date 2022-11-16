# Google-map-review-crawler
### 介紹
這個程式能根據 goolge map 中的 place_id 爬取指定店家的評論，包含評論者的名稱、評論者個人頁面的 url 等資訊，並以 csv 的形式儲存。  


### Dependency 
Selenium: https://pypi.org/project/selenium/  
Beautiful Soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/  
Pandas: https://pandas.pydata.org/docs/getting_started/install.html  
tqdm: https://github.com/tqdm/tqdm

可透過以下指令取得：  

    pip install -r requirements.txt    

### 使用方式
#### 1. 打開並執行 Google map review crawler.ipynb 的前兩個 cell  

  
#### 2. 呼叫 get_all_restaurant_comment() 函式  
將餐廳清單傳入 get_all_restaurant_comment() 即可。舉例來說，如果要爬取 restaurant_list1 中所有餐廳的評論，呼叫的方式如下：

    get_all_restaurant_comment('restaurant_list1')    
    
餐廳清單皆存在這個路徑下：

    Google-map-review-crawler/restaurant_spilt_list/ 
    
get_all_restaurant_comment() 會從這個資料夾讀取餐廳清單。  
  
#### 3. 查看結果
所有餐廳的評論都會存入 /result 資料夾中，不同清單的餐廳則會存在以餐廳清單名稱命名的資料夾底下，如 restaurant_list1 中所有餐廳的評論的儲存路徑會是：

    Google-map-review-crawler/result/restaurant_list1/
    
### 注意事項
#### 1. 評論是以 Goolge map 所提供「最相關」的形式排序。
#### 2. 無論評論數有多少，最多能爬下的評論是 1130 則，超過這個數額，無論再如何捲動頁面， Google map 也不會再提供更多評論。
#### 3. 評論內文（comment_text）為空的評論會被捨棄，而不會被儲存，有效評論是指評論內文不為空的評論。
#### 4. 如果執行期間中斷也沒有關係，程式會自動偵測已經爬過的餐廳，而不會重複爬取。
#### 5. 爬完一個 restaurant list 約需要 2 個小時的時間，且有些耗電，請確保電腦電源充足。
#### 6. Chromedriver 控制的瀏覽器會在被背景中執行，而不會額外跳出視窗，如果想讓瀏覽器的視窗被呈現，comment 以下的程式碼。
    options.add_argument('--headless')

