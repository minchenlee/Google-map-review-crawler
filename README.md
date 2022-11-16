# Google-map-review-crawler
### 介紹
這個程式能根據 place_id 爬取指定店家的評論，包含評論者的名稱、評論者個人頁面的 url，

### Dependency 
Selenium: https://pypi.org/project/selenium/  
Beautiful Soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/  
Pandas: https://pandas.pydata.org/docs/getting_started/install.html  
tqdm: https://github.com/tqdm/tqdm

可透過以下指令取得：  

    pip install -r requirements.txt    

### 使用方式
#### 1. 執行 Google map review crawler.ipynb

#### 2. 呼叫 get_all_restaurant_comment() 函式  
傳入
舉例來說，如果我要爬取 restaurant_list1 中所有餐廳的評論，呼叫的方式如下：

    get_all_restaurant_comment('restaurant_list1')    

### 
