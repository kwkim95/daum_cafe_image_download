from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import datetime
import time

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome("chromedriver.exe", options=options)
#driver.maximize_window()

login_url = "https://accounts.kakao.com/login?continue=https%3A%2F%2Flogins.daum.net%2Faccounts%2Fksso.do%3Frescue%3Dtrue%26url%3Dhttps%253A%252F%252Fwww.daum.net%252F"
driver.get(login_url)
time.sleep(2)

cur = datetime.datetime.now()
cur_date = cur.strftime("현재 시간 %y년 %m월 %d일 %h시 %m분 입니다.\n")
img_date = cur.strftime("%y%m%d%h%m")
print(cur_date)

def login(): # 다음카페 로그인
    id = input("아이디를 입력하세요 : ")
    driver.find_element_by_css_selector("div#loginEmailField > div.item_tf.item_inp").click()
    driver.find_element_by_css_selector("div#loginEmailField > div.item_tf.item_inp > input").send_keys(id)
    time.sleep(1)

    pwd = input("비밀번호를 입력하세요 : ")
    driver.find_element_by_css_selector("fieldset.fld_login > div.item_tf.item_inp").click()
    driver.find_element_by_css_selector("fieldset.fld_login > div.item_tf.item_inp > input").send_keys(pwd)
    time.sleep(1)
    driver.find_element_by_css_selector("div.wrap_btn > button.btn_g.btn_confirm.submit").click()

def loading(): # url의 사진들을 로딩
    print("로그인 되었습니다")
    cafe_url = input("사진을 다운받을 카페 주소를 입력하세요 : ")
    name = input("사진 파일에 들어갈 이름을 영어로 입력하세요 : ")
    driver.get(cafe_url)

    return name

def main(): # 메인함수
    name = loading()

    print("카페 로딩중입니다. 잠시만 기다려주세요.")
    # https://stackoverflow.com/questions/60182107/nosuchframeexceptionframe-reference-in-selenium
    wait = WebDriverWait(driver, 3)
    wait.until(ec.frame_to_be_available_and_switch_to_it("down"))
    #driver.switch_to.frame("name")

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    img = soup.find_all(class_="txc-image")

    num = 1
    count = len(img)/2

    for i in img:
        if num > count:
            break
        print("#{0}번째 파일 다운로드 완료".format(num))
        imgurl = i["data-img-src"]
        with urlopen(imgurl) as f:
            with open("./사진/" + img_date + "_" + name + str(num) + ".jpg", "wb") as h:
                img = f.read()
                h.write(img)
        num += 1

    print("다운로드 완료")

    driver.close()

if __name__ == "__main__":
    login()
    main()
