import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def take_screenshot(absolute_url):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from bs4 import BeautifulSoup
    # 待機用ライブラリ
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    wd = webdriver.Chrome(
        options=options
    )

    wd.get(absolute_url)
    # ページ上のすべての要素が読み込まれるまで待機（15秒でタイムアウト判定）
    WebDriverWait(wd, 15).until(EC.presence_of_all_elements_located)
    # beautifulsoupへの流し込み
    soup = BeautifulSoup(wd.page_source, "html.parser")
    # ページの大きさを調整
    page_width = wd.execute_script('return document.body.scrollWidth')
    page_height = wd.execute_script('return document.body.scrollHeight')
    wd.set_window_size(page_width, page_height)
    # スクリーンショットの保存
    title = soup.find('title')
    print(title)
    wd.save_screenshot(title.get_text()+'.png')
    #wd.save_screenshot('s.png')
    wd.close()

# 再帰的にリンクを取得する関数
def get_links_with_titles(url, visited_links):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.find_all("a")
    for link in links:
        href = link.get("href")
        #print(href)
        if href and not href.startswith("#") and not href.endswith((".pdf", ".zip", ".doc", ".docx", ".csv", ".pptx", "xls", ".xlsx", ".jpg", ".mp4")):
            absolute_url = urljoin(url, href)
            parsed_url = urlparse(absolute_url)
            if parsed_url.scheme in ["http", "https"] and parsed_url.netloc == "www.digitalservice.metro.tokyo.lg.jp" and absolute_url not in visited_links:
                visited_links.add(absolute_url)
                title = link.get_text()
                print(title+","+absolute_url)
                take_screenshot(absolute_url)

# ホームページのURLを指定
url = "https://www.digitalservice.metro.tokyo.lg.jp/"

visited_links = set()  # 収集済みのリンクを保持するセット
get_links_with_titles(url, visited_links)