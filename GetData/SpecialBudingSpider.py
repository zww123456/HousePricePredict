# 爬取南宁市已启用的地铁线路各站点信息
from selenium import webdriver

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

driver = webdriver.Chrome(chrome_options=options)


def isElementExist(xpath):
    flag = True
    try:
        driver.find_element_by_xpath(xpath)
        return flag
    except:
        flag = False
        return flag


try:
    driver.get('https://m.8684.cn/nanning_dt_map?from=singlemessage')

    for page in range(1, 4):
        for num in range(1, 50):
            dt = '/html/body/div[5]/ul/li[{}]/div/a[{}]'.format(page, num)
            if isElementExist(dt):
                with open('MyData/SpecialBudings.txt', 'a') as sb:
                    sb.write('南宁市,' + driver.find_element_by_xpath(dt).text + '地铁站\n')
            else:
                break
except:
    print('Error')

# 使用xGeocoding工具
