# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re

pattern_day10_14 = re.compile('일급 1[0-4]')
pattern_month10_14 = re.compile('월급 1[0-4]')
pattern_ildao = re.compile('일다오')
pattern_day10_16 = re.compile('일급 1[0-6]')
pattern_month10_16 = re.compile('월급 1[0-6]')
pattern_system = re.compile('비계/동바리')
pattern_nego = re.compile('협의')
pattern_null = re.compile('null')

class IldaoTestWithSeleniumPipeline:
    def process_item(self, item, spider):
        if len(pattern_day10_14.findall(item['pay'])) > 0:  # '일급 10 ~ 14' 들어가면 다 뺌
            raise DropItem('Drop 일급 10 ~ 14 !')
        elif len(pattern_month10_14.findall(item['pay'])) > 0:  # '월급 10 ~ 14' 들어가면 다 뺌
            raise DropItem('Drop 월급 10 ~ 14 !')
        elif item['title'].find('일다오') != -1:    # str.find('문자열') 찾았으면 0 ~ 찾은 첫번째 인댁스 / 못찾았으면 -1 반환
            raise DropItem('Drop title : 일다오')
        elif len(pattern_ildao.findall(item['detail'])) > 0: # 일부러 str.find와 다르게 해봄
            raise DropItem('Drop detail : 일다오')
        elif len(item['detail']) < 35: # detail 35자 미만은 빼
            raise DropItem('Drop detail : detail 35자 미만')
        elif len(item['title']) < 6: # title 6자 미만은 빼
            raise DropItem('Drop detail : title 6자 미만')
        elif (len(pattern_day10_16.findall(item['pay'])) > 0 or len(pattern_month10_16.findall(item['pay'])) > 0) and len(pattern_system.findall(item['type'])) > 0:
            raise DropItem('Drop detail : 비계/동바리 이면서 단가 16이하')
        elif len(pattern_nego.findall(item['pay'])) > 0 and len(pattern_system.findall(item['type'])) > 0:
            raise DropItem('Drop detail : 비계/동바리 이면서 협의')
        elif len(pattern_null.findall(item['site'])) > 0:   # site 에 null 이 들어가면 빼
            raise DropItem('Drop detail : site 가 null')
        else:
            return item

# 중복제거
class DuplicatesPipeline:
    def __init__(self):
        self.titles_seen = set()
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter["title"] in self.titles_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.titles_seen.add(adapter["title"])
            return item

# 본문에 '♧일다오 지원하기를 이용해주세요♧' 뺌!!!
# '일급 10 ~ 14' 으로 시작하는 것도 뺌 !!!
# detail 30자 미만은 뺌!!!
# 인원 숫자만 가져와 더해준다. 0 인경우 0명 표기 함!!!
# pay  , 단위 고침!!!
# 조공/보조  고침!!!
# '비계/동바리' 16만원 이하 뺌!!!