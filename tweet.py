from selenium import webdriver
from selenium.webdriver.chrome.options import Options # オプションを使うために必要
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import urllib.parse
import random

from dotenv import load_dotenv
# .envファイルの内容を読み込みます
load_dotenv()

import os
 
CHROMEDRIVER = "driver/chromedriver"
TWITTER_BASE = "https://twitter.com/"

def get_driver():
    # 　ヘッドレスモードでブラウザを起動
    options = Options()
    # options.add_argument('--headless')
    # ブラウザーを起動
    driver = webdriver.Chrome(options=options, executable_path='driver/chromedriver')
 
    return driver
 
 
# twitterログイン
def do_login(driver):
    driver.get('https://twitter.com/i/flow/login')
    time.sleep(5)
    
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']

    driver.find_element_by_name('username').send_keys(username + Keys.ENTER)
    time.sleep(random.randint(2, 5))
    
    driver.find_element_by_name('password').send_keys(password + Keys.ENTER)
    time.sleep(random.randint(2, 5))

# tweet投稿
def post_tweet(driver, text, url):
 
    tweet_text = text
    tweet_text = urllib.parse.quote(tweet_text, safe='')
 
    tweet_url = url
    tweet_url = urllib.parse.quote(tweet_url, safe='')
 
    target_url = TWITTER_BASE + "intent/tweet?text=" + tweet_text + "&amp;url=" + tweet_url
 
    # 投稿画面へ遷移
    driver.get(target_url)
 
    # tweetボタンが読み込まれるまで待機（最大10秒）
    elem_tweet_btn = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='tweetButton']"))
    )

    try:
        actions = ActionChains(driver)
        actions.move_to_element(elem_tweet_btn)
        actions.click(elem_tweet_btn)
        actions.perform()

    except:
        print("投稿エラー")
    
if __name__ == "__main__":
    # Driver
    driver = get_driver()
 
    # ログイン
    login_flg = do_login(driver)

    # ツイート
    sample = "カイエン乗りてえ"
    tweet_flag = post_tweet(driver, sample, sample)

 
    # driver.quit()
