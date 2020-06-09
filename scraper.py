import json
import time
import os

with open('user_input.json', 'r') as openfile:
    json_object = json.load(openfile)

browser_option = json_object.get('f_browser')
browser_mode = json_object.get('f_mode')

from selenium import webdriver

if browser_option == 'chrome':
    from selenium.webdriver.chrome.options import Options
elif browser_option == 'firefox':
    from selenium.webdriver.firefox.options import Options

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import urllib.request
from pathlib import Path

timeout = 25
i = 1
downloading = True

img_urls = {
    'count': None
}


def img_finder(page):
    try:
        img_xpath = r'//*[@id="imgCurrent"]'
        img = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.XPATH, img_xpath)))
        link = img.get_attribute('src')
        img_urls.update({f'{page}': link})
        page_number = Select(WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.ID, "selectPage"))))
        page_number.select_by_visible_text(str(page+1))
    except:
        global downloading
        downloading = False


quality_set = json_object.get('f_quality')
comic_url = json_object.get('f_comic_url')

options = Options()

if browser_mode == 'headless':
    options.headless = True

drivers_path = Path('drivers').resolve()
extensions_path = Path('extensions').resolve()

if browser_option == 'chrome':
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    if browser_mode == 'head':
        options.add_extension(str(extensions_path) + r"\extension_4_13_0_0.crx")

    browser = webdriver.Chrome(options = options, executable_path = str(drivers_path) + r"\chromedriver.exe")
    
    if browser_mode == 'head':
        browser.switch_to.window(browser.window_handles[1])
    # options.add_argument('log-level=3')
elif browser_option == 'firefox':
    browser = webdriver.Firefox(options = options, executable_path = str(drivers_path) + r"\geckodriver.exe", service_log_path = os.path.devnull)
    browser.install_addon(str(extensions_path) + r"\uBlock0@raymondhill.net.xpi")
    browser.install_addon(str(extensions_path) + r"\@easyimageblocker.xpi")


if comic_url == 'None':
    comic_name = json_object.get('f_comic_name')
    year = int(json_object.get('f_year'))
    if year != 1:
        issue_number = json_object.get('f_issue_number')
    
    url = "https://readcomiconline.to/"

    browser.get(url)

    search_bar = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.ID, "keyword")))
    search_bar.send_keys(comic_name + Keys.ENTER)

    if year == 1:
        comic = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.XPATH, r"(//*[@class='listing']//a)[1] | (//*[@class='list']//a)[1]")))
        comic.click()
    else:
        comic = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, f"{year}")))
        comic.click()        

    if year != 1:        
        top_issue = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.XPATH, r"(//*[@class='listing']//a)[1] | (//*[@class='list']//a)[1]")))
        top_issue_name = top_issue.text
        top_issue_number = int(top_issue_name.partition("#")[-1])
        required_issue = top_issue_number - (int(issue_number) - 1)
        issue = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.XPATH, f"(//*[@class='listing']//a)[{required_issue}] | (//*[@class='list']//a)[{required_issue}]")))
        issue.click()
else:
    browser.get(comic_url)

if quality_set == 'high':
    quality = Select(WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.ID, "selectQuality"))))
    quality.select_by_value("hq")


print("Scraping readcomiconline...")
while downloading:
    img_finder(i)
    i += 1


img_urls.update({'count': f'{i}'})
json_url_object = json.dumps(img_urls, indent=1)
with open('img_urls_file.json', 'w') as urlfile:
    urlfile.write(json_url_object)

print("Scraped readcomiconline successfully")
browser.quit()