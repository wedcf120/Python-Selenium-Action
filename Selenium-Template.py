from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
import time
import re
from datetime import datetime
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 800))  
display.start()

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--enable-javascript') # 启用 JavaScript
options.add_argument('blink-settings=imagesEnabled=false')      # 不加载图片，提升运行速度
options.add_argument('--no-sandbox')                # 解决DevToolsActivePort文件不存在的报错
options.add_argument('--disable-gpu')               # 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('--hide-scrollbars')           # 隐藏滚动条，应对一些特殊页面
options.add_argument("--headless") #无界面




driver1 = webdriver.Chrome(options=options)
driver1.get('https://www.gettyimages.com/photos/people?assettype=image&page=1&phrase=Fashion&recency=last24hours&sort=newest')
time.sleep(6) 
html1 = driver1.page_source
# 关闭浏览器
driver1.quit()

driver2 = webdriver.Chrome(options=options)
driver2.get('https://www.gettyimages.com/photos/people?assettype=image&page=1&phrase=Actor&recency=last24hours&sort=newest')
time.sleep(6) 
html2 = driver2.page_source
# 关闭浏览器
driver2.quit()

driver3 = webdriver.Chrome(options=options)
driver3.get('https://www.gettyimages.com/photos/people?assettype=image&page=1&phrase=Concert&recency=last24hours&sort=newest')
time.sleep(6) 
html3 = driver3.page_source 
# 关闭浏览器
driver3.quit()


driver4 = webdriver.Chrome(options=options)
driver4.get('https://www.gettyimages.com/photos/people?assettype=image&page=1&phrase=Music&recency=last24hours&sort=newest')
time.sleep(6) 
html4 = driver4.page_source
# 关闭浏览器
driver4.quit()

driver5 = webdriver.Chrome(options=options)
driver5.get('https://www.gettyimages.com/photos/people?assettype=image&page=1&phrase=Celebrities&recency=last24hours&sort=newest')
time.sleep(6) 
html5 = driver5.page_source
# 关闭浏览器
driver5.quit()

driver6 = webdriver.Chrome(options=options)
driver6.get('https://www.gettyimages.com/photos/celebrities?assettype=image&page=&phrase=Celebrities&recency=last24hours&sort=newest')
time.sleep(6) 
html6 = driver6.page_source 
# 关闭浏览器
driver6.quit()


driver7 = webdriver.Chrome(options=options)
driver7.get('https://www.gettyimages.com/photos/people?assettype=image&page=2&phrase=Fashion&recency=last24hours&sort=newest')
time.sleep(6) 
html7 = driver7.page_source
# 关闭浏览器
driver7.quit()

driver8 = webdriver.Chrome(options=options)
driver8.get('https://www.gettyimages.com/photos/people?assettype=image&page=2&phrase=Actor&recency=last24hours&sort=newest')
time.sleep(6) 
html8 = driver8.page_source
# 关闭浏览器
driver8.quit()

driver9 = webdriver.Chrome(options=options)
driver9.get('https://www.gettyimages.com/photos/people?assettype=image&page=2&phrase=Concert&recency=last24hours&sort=newest')
time.sleep(6) 
html9 = driver9.page_source 
# 关闭浏览器
driver9.quit()


driver10 = webdriver.Chrome(options=options)
driver10.get('https://www.gettyimages.com/photos/people?assettype=image&page=2&phrase=Music&recency=last24hours&sort=newest')
time.sleep(6) 
html10 = driver10.page_source
# 关闭浏览器
driver10.quit()

driver11 = webdriver.Chrome(options=options)
driver11.get('https://www.gettyimages.com/photos/people?assettype=image&page=3&phrase=Celebrities&recency=last24hours&sort=newest')
time.sleep(6) 
html11 = driver11.page_source
# 关闭浏览器
driver11.quit()

driver12 = webdriver.Chrome(options=options)
driver12.get('https://www.gettyimages.com/photos/people?assettype=image&page=4&phrase=Celebrities&recency=last24hours&sort=newest')
time.sleep(6) 
html12 = driver12.page_source 
# 关闭浏览器
driver12.quit()

html = '\n\n'.join([html1, html2, html3, html4, html5, html6, html7, html8, html9, html10, html11, html12])





now = datetime.now()
date = now.strftime("%m-%d")
hour = now.strftime("%H")

regex_link = r'people\"\:\"[\s\S]{1,350}\"\,"artist[\s\S]{1,350}landingUrl\"\:\".+?\"'
regex_tit = r'people\"\:\"[\s\S]{1,350}\"\,"artist[\s\S]{1,350}landingUrl\"\:\".+?\"'
regex_con = r'caption\"\:\"[\s\S]{1,350}\"\,\".+?people\"\:\"[\s\S]{1,350}\"\,"artist'

header = '''<?xml version="1.0" encoding="utf-8"?>
<?xml-stylesheet type="text/xsl" href="rss1.xsl"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:media="http://search.yahoo.com/mrss/">
<channel>
 <title>Getty</title>
 <link>http://www.gettyimg.com/</link>
 <atom:link href="http://www.gettyimg.com/" rel="self" type="application/rss+xml" />

 '''

footer = '</channel></rss>'



#html = requests.get(url).text

if re.findall(regex_link, html) and re.findall(regex_tit, html):
    links = re.findall(regex_link, html)
    titles = re.findall(regex_tit, html)

    rss = ""

    for i in range(len(links)):
        link = re.sub(r'people\"\:\"[\s\S]{1,350}\"\,"artist[\s\S]{1,350}landingUrl\"\:\"(.+?)\"', r'https://www.gettyimages.com\1', links[i])
        title = re.sub(r'people\"\:\"([\s\S]{1,350})\"\,"artist[\s\S]{1,350}landingUrl\"\:\".+?\"', r'\1', titles[i])
        article = re.sub(r'.*detail\/news\-photo\/|news\-photo\/.*|\-', ' ', link)
        article = article.title()

        rss += f'''
                <item>
                <title><![CDATA[{title}【{article}]]]></title>
                <link><![CDATA[{link}]]></link>
                <description><![CDATA[{article}]]></description>
                </item>

                '''

    rss_feed = header + rss + footer

    print(rss_feed)
else:
    rss = f'{header}\n\t<item>\n\t\t<title>出错，请检查 {date}-{hour}</title>\n\t\t<link>{url}#{date}-{hour}</link>\n\t</item>\n{footer}'
    print(rss)

with open('./getty.html', 'w', encoding='utf-8') as f:
    f.write(rss_feed)
