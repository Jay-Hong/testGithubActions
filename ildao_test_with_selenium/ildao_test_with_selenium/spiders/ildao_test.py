import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re; import time;
from ildao_test_with_selenium.items import IldaoTestWithSeleniumItem

class IldaoTestSpider(scrapy.Spider):
    name = "ildao_test"
    allowed_domains = ["ildao.com"]
    start_urls = ["https://ildao.com/recruit"]
 
    def __init__(self):
        headlessoptions = webdriver.ChromeOptions()
        headlessoptions.add_argument('headless')
        headlessoptions.add_argument('window-size=1920x1080')
        headlessoptions.add_argument("disable-gpu")
        headlessoptions.add_argument("User-Agent:  Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
        headlessoptions.add_argument("lang=ko_KR")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        #self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=headlessoptions)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(2)
        
        # ildao_items 가져오기
        ildao_items = self.driver.find_elements(By.CSS_SELECTOR, "div.scrollsection > div.box.pointer")

        for i in range(2):
            print(f"목록가져오기{i} : {ildao_items[-1].location_once_scrolled_into_view}")
            time.sleep(1.1)
            ildao_items = self.driver.find_elements(By.CSS_SELECTOR, "div.scrollsection > div.box.pointer")

        # scrollsection 가장 상단 가기
        print(f"상단가기  : {ildao_items[0].location_once_scrolled_into_view}")
        time.sleep(1.5)

        for index, ildao_item in enumerate(ildao_items):
            print(f"{index} : {ildao_item.location_once_scrolled_into_view}")
            time.sleep(.26)
            ildao_item.click()
            time.sleep(.26)
    
            title_sel = self.driver.find_element(By.CSS_SELECTOR, "#detail_info div.ft5.NotoSansM")
            title_pre = re.sub('[^a-zA-Z0-9가-힣一-龥_\s\(\)\[\]\-\~\/\,\.\ㆍ\&]', ' ', title_sel.text)
            title = re.sub('\s{2,9}', ' ', title_pre).strip(' _-~/,.ㆍ&').lstrip(')]').rstrip('([').upper()

            site_sel = self.driver.find_element(By.CSS_SELECTOR, "div.time.ft11.col_gra04.NotoSansL")
            site_pre = re.sub('[a-z]+_[a-z]+\s', '', site_sel.text) # "location_on " 없애기
            site = re.sub('세종 세종', '세종시', site_pre)

    
            type_sel = self.driver.find_element(By.CSS_SELECTOR, "#detail_info div.ft11 div.ft10")
            type_pre = re.sub('조공/잡부', '조공/보조', type_sel.text)
            type = re.sub('시스템/비계', '비계/동바리', type_pre)
    
            pay_sel = self.driver.find_element(By.CSS_SELECTOR, "#detail_info div.col_blu02.ft10 > div")
            pay_pre1 = re.sub('\n', ' ', re.sub('0 원', '0원', pay_sel.text))
            pay_pre2 = re.sub('0,000', '만', pay_pre1)
            if pay_pre2.find(',000') == -1:
                pay = re.sub(',', '', pay_pre2)
            else:
                pay = re.sub('', '', pay_pre2)
    
            etcs_sel = self.driver.find_elements(By.CSS_SELECTOR, "#detail_info div.ft11.col_blu02")

            etc1 = '';etc2 = '';etc3 = ''
            etc_set = set()
            for etc in etcs_sel:
                etc_set.add(etc.text.strip(','))

            if '숙식제공' in etc_set:
                etc1 = '숙식제공'

                if '4대보험' in etc_set:
                    etc2 = '4대보험'
                    if '출퇴근가능' in etc_set:
                        etc3 = '출퇴근가능'
                    elif '장기근무' in etc_set:
                        etc3 = '장기근무'
            
                elif '출퇴근가능' in etc_set:
                    etc2 = '출퇴근가능'
                    if '장기근무' in etc_set:
                        etc3 = '장기근무'
            
                elif '장기근무' in etc_set:
                    etc2 = '장기근무'

            elif '4대보험' in etc_set:
                etc1 = '4대보험'

                if '출퇴근가능' in etc_set:
                    etc2 = '출퇴근가능'
                    if '장기근무' in etc_set:
                         etc3 = '장기근무'
                elif '장기근무' in etc_set:
                    etc2 = '장기근무'

            elif '출퇴근가능' in etc_set:
                etc1 = '출퇴근가능'
                if '장기근무' in etc_set:
                    etc2 = '장기근무'

            elif '' in etc_set:
                etc1 = '장기근무'

            numpeople_int = 0
            numpeople_pre = 0
            num_pattern = re.compile('[0-9]')
            numpeople_sel_list = self.driver.find_elements(By.CSS_SELECTOR, "#detail_info div.ft11 div.ft10[style='display: flex;']")
            for numpeople_sel in numpeople_sel_list:
                if len(num_pattern.findall(numpeople_sel.text)) > 0:    # 숫자가 들어있는 문자열만 가져온다
                    numpeople_int = re.sub('[^0-9]', '', numpeople_sel.text)    # 숫자를 제외한 문자 삭제
                    print(f"numpeople_int : {numpeople_int}")
                    numpeople_pre += int(numpeople_int)                 # 초보+조공+준공+기공 = 총인원
            numpeople = f"{numpeople_pre}명"
    
            phone_sel = self.driver.find_element(By.CSS_SELECTOR, "#detail_info div.ft11 div.ft10.RobotoM")
            phone = re.sub('', '', phone_sel.text)
    
            #detail = driver.find_element(By.CSS_SELECTOR, "#detail_info p.ft10.lin_h2")
            detail_sel = self.driver.find_element(By.CSS_SELECTOR, "#detail_info p.ft10.lin_h2")
            detail_pre = re.sub('\*\]', '•', detail_sel.text) # 특정 소개소 detail 작성 양식 때문에 바꿔줌 '*]타일용접' (나중에 없애도 됨)
            detail = re.sub('', '', detail_pre)
    
            imageURL_sel = ''
            imageURL = ''
            try:
                imageURL_sel = self.driver.find_element(By.CSS_SELECTOR, "#detail_info > div > div > div > div > img")
            except Exception as e:
                imageURL = ''
            else:
                imageURL = imageURL_sel.get_attribute('src')

            job_item = IldaoTestWithSeleniumItem()
            #print(f"title : {title}")
            job_item['title'] = title
            #print(f"site  : {site}")
            job_item['site'] = site
            #print(f"type  : {type_}")
            job_item['type'] = type
            #print(f"pay   : {pay}")
            job_item['pay'] = pay
            #print(f"etc1  : {etc1}")
            job_item['etc1'] = etc1
            #print(f"etc2  : {etc2}")
            job_item['etc2'] = etc2
            #print(f"etc3  : {etc3}")
            job_item['etc3'] = etc3
            print(etc_set)
            #print(f"numpeople : {numpeople}")
            job_item['numpeople'] = numpeople
            #print(f"phone     : {phone}")
            job_item['phone'] = phone
            #print(f"detail    : {detail}")
            job_item['detail'] = detail
            #print(f"imageURL  : {imageURL}")
            job_item['imageURL'] = imageURL
            #print()
            job_item['time'] = ''
            job_item['sponsored'] = ''
            yield job_item
        
        time.sleep(2)
        pass
