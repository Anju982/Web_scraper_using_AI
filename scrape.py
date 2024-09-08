import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import os
import time
from bs4 import BeautifulSoup

def scrape_website(url):
    print("Launch Chrome Browser...")
    
    chrome_driver_path = os.path.join(os.getcwd(),"Web_Driver" ,"chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument("--incognito")
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    
    try:
        driver.get(url)
        print("Page Loaded")
        html = driver.page_source
        time.sleep(10)
     
        return html
    finally:
        driver.quit()
        
def extract_body(html_contain):
       soup = BeautifulSoup(html_contain, "html.parser")
       boday_contents = soup.body
       if boday_contents:
           return str(boday_contents)
       else:
           return ""
       
def clean_body_contents(body_contents):
    soup = BeautifulSoup(body_contents, "html.parser")
    
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    
    cleaned_contents = soup.get_text(separator="\n")
    cleaned_contents = "\n".join(
        line.strip() for line in cleaned_contents.splitlines() if line.strip()
    )
    
    return cleaned_contents

def split_dom_content(dom_content, max_legnth = 6000):
    return [dom_content[i:i+max_legnth] for i in range(0, len(dom_content), max_legnth)]