
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# driver = webdriver.Chrome(ChromeDriverManager().install())
# driver = webdriver.Chrome()

# driver.get("http://selenium.dev")
# driver.implicitly_wait(0.5)
# title = driver.title
# print(title)
# text_box = driver.find_element(by=By.NAME, value="my-text")
# submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
# driver.quit()

# def test_eight_components():
#     driver = webdriver.Chrome(ChromeDriverManager().install())
#
#     driver.get("https://www.selenium.dev/selenium/web/web-form.html")
#
#     title = driver.title
#     assert title == "Web form"
#
#     driver.implicitly_wait(0.5)
#
#     text_box = driver.find_element(by=By.NAME, value="my-text")
#     submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
#
#     text_box.send_keys("Selenium")
#     # submit_button.click()
#
#     message = driver.find_element(by=By.ID, value="message")
#     value = message.text
#     assert value == "Received!"
#
#     driver.quit()
#
# test_eight_components()


# driver = webdriver.Chrome(ChromeDriverManager().install())
# driver.get("http://bkzhjx.wh.sdu.edu.cn/sso.jsp")
#
# print(driver.title)
# input = driver.find_elements(By.CLASS_NAME, 'login_box_input')
#
# # 输入账号和密码
# input[0].send_keys("202000130143")
# input[1].send_keys("zkr89803589")
# # 输入账号和密码
#
# submit = driver.find_element(By.CLASS_NAME, 'login_box_landing_btn')
# submit.send_keys("webdriver" + Keys.ENTER)
#
# print(driver.title)
# enterance = driver.find_element(By.CSS_SELECTOR, '#dataList > tbody > tr:nth-child(2) > td > a')
# enterance.click()
#
# print(driver.title)
# school_record = driver.find_element(By.CSS_SELECTOR, 'body > div.new-main > div.main > div.sidebar > div.scrollbar > div > ul > li:nth-child(2) > div > span.text')
# school_record.click()
#
# driver.implicitly_wait(0.5) # 需要等待加载
# my_record = driver.find_element(By.CSS_SELECTOR, 'body > div.new-main > div.main > div.sidebar > div.scrollbar > div > ul > li:nth-child(2) > ul > li:nth-child(2)')
# # body > div.new-main > div.main > div.sidebar > div.scrollbar > div > ul > li:nth-child(2) > ul > li:nth-child(1)
# # body > div.new-main > div.main > div.sidebar > div.scrollbar > div > ul > li:nth-child(2) > ul > li:nth-child(2)
# # body > div.new-main > div.main > div.sidebar > div.scrollbar > div > ul > li:nth-child(2) > ul > li:nth-child(1) > ul
#
# try:
#     # print(my_record)
#     print(my_record.text)
#     # print(my_record.size)
#     my_record.click()
# except Exception as e:
#     print(e)
#
# course_record = driver.find_element(By.CSS_SELECTOR, 'body > div.new-main > div.main > div.sidebar > div.scrollbar > div > ul > li:nth-child(2) > ul > li:nth-child(2) > ul')
# course_record.click()
#
# # 进入到成绩查询界面
# # 查询事项
# curriculum_time = driver.find_element(By.CSS_SELECTOR, '#search-form-content > div:nth-child(1) > div.search-line-input')
# # print(curriculum_time)
# print(driver.window_handles)
#
# # 进入到成绩查询界面



# 切换思路：直接发送POST数据包
# post请求
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re

def parse_score(tr_obj):
    # 获取课程名，成绩，等级，绩点，分数段排名，实际排名，课程性质，more
    units = tr_obj.select('td')
    # print(units)
    # print(len(units))
    class_name = str(units[4].get_text())
    num = str(units[8].get_text())
    pattern = re.compile(r'[0-9]{2}')
    num = pattern.findall(num)
    # 有些课程仅评级
    grade = num[0] if len(num) > 0 else ''
    gpa = str(units[10].get_text())
    attr = str(units[17].get_text())
    ret = [class_name, grade, gpa, attr]
    return ret

def get_ids(tr_obj):
    units = tr_obj.select('td input')[0]
    print(units['value'])
    return units['value']

# #dataList > tbody > tr:nth-child(2) > td:nth-child(1) > input[type=checkbox]

url = 'https://bkzhjx.wh.sdu.edu.cn/jsxsd/kscj/cjcx_list'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Cookie': 'bzb_jsxsd=C91D2F49C5D85448D48CC3A25C989081; bzb_njw=AAAD27AC1BFD71C73273D9B2877FB5B6; SERVERID=124'
}
# bzb_jsxsd=C91D2F49C5D85448D48CC3A25C989081; SERVERID=125; bzb_njw=4123B79CC29DE0A1C28D7DEDC8DCD6AF
# bzb_jsxsd=C91D2F49C5D85448D48CC3A25C989081; bzb_njw=ED878962F23171A90F772477B7188F2D; SERVERID=124
# bzb_jsxsd=C91D2F49C5D85448D48CC3A25C989081; SERVERID=124; bzb_njw=AAAD27AC1BFD71C73273D9B2877FB5B6
# Cookie失效，可以存在多个有效cookie

data = {
    'kksj': '2022-2023-1',     # 默认查询全部，2022-2023-1
    'kcxz': '',
    'kcmc': '',
    'xsfs': 'all'
}

data = urllib.parse.urlencode(data).encode('utf-8')
request = urllib.request.Request(url=url, data=data, headers=headers)
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')

# try:
#     with open('{}.html'.format('content'), 'w', encoding='utf-8') as f:
#         f.write(content)
# except Exception as e:
#     print(e)

# 通过BeautifulSoup解析得到成绩信息
soup = BeautifulSoup(content, 'html.parser')
scores = soup.select('table[id="dataList"] tr')

print(len(scores))
score_list = []
ids = ''
for i in range(1, len(scores)):
    score = parse_score(scores[i])
    id = get_ids(scores[i])  # 获取名为C_select标签的value
    ids += (str(id) + ',')
    score_list.append(score)

print(score_list)

# for i in score_list:
#     if (i[3] == '专业必修课'):
#         print(i)


# https://bkzhjx.wh.sdu.edu.cn/jsxsd/kscj/xskcpm_list.do
# get请求，如何构造ids？
url_detailed = 'https://bkzhjx.wh.sdu.edu.cn/jsxsd/kscj/xskcpm_list.do'
url_detailed += '?ids=' + ids
print(url_detailed)
request = urllib.request.Request(url=url_detailed, headers=headers)
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')
# https://bkzhjx.wh.sdu.edu.cn/jsxsd/kscj/xskcpm_list.do?ids=F572722D68FCC0EDE053214BA8C02B45,F5C37CBE75714C42E053214BA8C0EC70,F2E73028529812D8E053214BA8C03E54,F5BFD841B098124FE053214BA8C0383E,F5D11282A8CB2E84E053214BA8C08AB0,EFEF0473068C09D1E053214BA8C020DD,
# print(content)
# try:
#     with open('{}.html'.format('cont_detailed'), 'w', encoding='utf-8') as f:
#         f.write(content)
# except Exception as e:
#     print(e)

# 进一步解析工作
# 转化为JSON文件格式进行存储
# 通过github action进行部署

# 导出当前代码使用的依赖项
