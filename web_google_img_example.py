from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import os

# 사용자 입력: 검색할 키워드와 이미지 저장 경로
search_keyword = '오리'
save_folder = '/img/duck/'

# 브라우저 열기
driver = webdriver.Chrome()

# 구글 이미지 검색 페이지 열기
driver.get('https://www.google.com/imghp?hl=en')

# 검색창에 키워드 입력 및 검색 실행
search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys(search_keyword)
search_box.send_keys(Keys.RETURN)

# 페이지 로딩 대기
time.sleep(2)

# 스크롤 다운 (이미지 더 불러오기)
for _ in range(5):  # 필요한 만큼 스크롤
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(2)  # 페이지 로딩 대기

# HTML 파싱
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 이미지 링크 추출
image_elements = soup.find_all('img', class_='YQ4gaf', style=True)
image_links = [img.get('src') for img in image_elements if img.get('src')]

# 이미지 저장할 폴더 생성
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# 이미지 다운로드
for i, link in enumerate(image_links):
    try:
        response = requests.get(link)
        with open(os.path.join(save_folder, f'image_{i+1}.jpg'), 'wb') as file:
            file.write(response.content)
        print(f'Successfully downloaded image {i+1}')
    except Exception as e:
        print(f'Failed to download image {i+1}: {e}')

# 브라우저 닫기
driver.quit()