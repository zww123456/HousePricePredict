# -*- encoding=utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time

options = webdriver.ChromeOptions()

options.add_argument(
    'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"')

# 禁用谷歌浏览器图片、JavaScript,提升爬取速度

prefs = {
    'profile.default_content_setting_values': {
        'images': 2,
        'javascript': 2
    }
}
options.add_experimental_option('prefs', prefs)

quyu = ['jiangnan', 'xingning', 'yongning', 'liangqing', 'wumingquwumingxian']
driver = webdriver.Chrome(chrome_options=options)
# 爬取每一个标题的链接，进入以后获取相应的内容后再返回上一级，重复以上动作

for i in range(len(quyu)):
    for page in range(3, 51):
        try:
            driver.get('https://nanning.anjuke.com/sale/' + quyu[i] + '/p' + str(
                page) + '/?kwid=10507608784&utm_term=%E5%8D%97%E5%AE%81%E6%88%BF%E4%BA%A7#filtersort')  #
            for num in range(1, 61):
                search = driver.find_element_by_xpath('//*[@id="houselist-mod-new"]/li[' + str(
                    num) + ']/div[2]/div[1]/a')

                driver.get(search.get_attribute('href'))  # 获取子页面链接

                # 获取房源详情页面
                html = driver.page_source
                info = ''
                # 北纬
                lat = re.compile('lat : "(.*?)"', re.S)
                north = lat.findall(html)[0]
                # 东经
                lng = re.compile('lng : "(.*?)"', re.S)
                east = lng.findall(html)[0]

                # 小区名，户型，单价，面积，年份，房屋朝向，楼层，装修程度，有无电梯，地理坐标
                try:
                    village = driver.find_elements(By.XPATH,
                                                   '//*[@id="content"]/div[4]/div[1]/div[3]/div/div[1]/ul/li[1]/div[2]/a')
                    village_str = ''
                    for vi in village:
                        village_str += vi.text
                    info += village_str + ','

                except:
                    village_str = 'NULL'

                try:
                    layout = driver.find_element(By.XPATH,
                                                 '//*[@id="content"]/div[4]/div[1]/div[3]/div/div[1]/ul/li[2]/div[2]')
                    layout = layout.text
                    info += layout + ','

                except:
                    layout = 'NULL'

                try:
                    price = driver.find_element(By.XPATH,
                                                '//*[@id="content"]/div[4]/div[1]/div[3]/div/div[1]/ul/li[3]/div[2]')
                    price = price.text
                    info += price + ','
                except:
                    price = 'NULL'

                try:
                    area = driver.find_element(By.XPATH,
                                               '//*[@id="content"]/div[4]/div[1]/div[3]/div/div[1]/ul/li[5]/div[2]')
                    area = area.text
                    info += area + ','
                except:
                    area = 'NULL'

                try:
                    year = driver.find_element(By.XPATH,
                                               '//*[@id="content"]/div[4]/div[1]/div[3]/div/div[1]/ul/li[7]/div[2]')
                    year = year.text
                    info += year + ','
                except:
                    year = 'NULL'

                try:
                    orientation = driver.find_element(By.XPATH,
                                                      '//*[@id="content"]/div[4]/div[1]/div[3]/div/div[1]/ul/li[8]/div[2]')
                    orientation = orientation.text
                    info += orientation + ','
                except:
                    orientation = 'NULL'

                try:
                    floor = driver.find_element(By.XPATH,
                                                '//*[@id="content"]/div[4]/div[1]/div[3]/div/div[1]/ul/li[11]/div[2]')
                    floor = floor.text
                    info += floor + ','
                except:
                    floor = 'NULL'

                try:
                    trim = driver.find_element(By.XPATH,
                                               '//*[@id="content"]/div[4]/div[1]/div[3]/div/div[1]/ul/li[12]/div[2]')
                    trim = trim.text
                    info += trim + ','
                except:
                    trim = 'NULL'

                try:
                    elevator = driver.find_element(By.XPATH,
                                                   '//*[@id="content"]/div[4]/div[1]/div[3]/div/div[1]/ul/li[14]/div[2]')
                    elevator = elevator.text
                    info += elevator + ','
                except:
                    elevator = 'NULL'

                info += north + ',' + east + '\n'
                print(info)
                with open('MyData/House.csv', 'a', encoding='utf-8') as f:
                    f.write(info)
                time.sleep(5)
                driver.back()  # 后退，返回上一级目录页
        except Exception:
            print(quyu[i] + '第' + str(page) + '页,第' + str(num) + '条信息' + '出现问题')
            time.sleep(1000)
            continue
driver.quit()
