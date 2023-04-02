from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import time
import re
import requests
import os
import datetime
from datetime import datetime

# 安装最新版的chromedriver
chromedriver_autoinstaller.install()

options = Options()
options.add_argument('--headless')
options.add_argument('--enable-javascript')
options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--hide-scrollbars')
options.add_argument("--headless")

html_list = []

with open('users.txt', 'r') as f:
    for user in f:
        user = user.strip()
        url = f'https://www.tiktok.com/@{user}'
        response = requests.get(url)
        if response.status_code == 200000000000:
            html_list.append(response.text)
        else:
            try:
                os.system('killall -9 chrome')
                driver = webdriver.Chrome(options=options)
                driver.set_page_load_timeout(15)
                driver.get(url)
                time.sleep(5)
                html_list.append(driver.page_source)
                driver.quit()
            except Exception as e:
                print(f"An exception occurred while scraping user {user}: {e}")

html = '\n'.join(html_list)

#print(html)
#exit()








regex_link = r'id\"\:\"[0-9]{19,23}\"\,\"desc\"\:\".+?\"\,\"createTime'
regex_tit = r'id\"\:\"[0-9]{19,23}\"\,\"desc\"\:\".+?\"\,\"createTime'
regex_con = r'originCover\"\:\"(.+?)\"'
regex_pubdate = r'\"createTime\"\:\"[0-9]{7,20}\"\,\"scheduleTime'

header = '''<?xml version="1.0" encoding="utf-8"?>
<?xml-stylesheet type="text/xsl" href="rss1.xsl"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:media="http://search.yahoo.com/mrss/">
<channel>
 <title>tiktok</title>
 <link>http://www.tiktok.com/</link>
 <atom:link href="http://www.tiktok.com/" rel="self" type="application/rss+xml" />

 '''

footer = '</channel></rss>'



if re.findall(regex_link, html) and re.findall(regex_tit, html):
    links = re.findall(regex_link, html)
    titles = re.findall(regex_tit, html)
    articles = re.findall(regex_con, html)
    pubdates = re.findall(regex_pubdate, html)

    # 将文章按发布时间从新到旧排序
    sorted_articles = sorted(zip(pubdates, links, titles, articles), reverse=True)

    rss = ""

    # 只保留最新的5个文章
    for pubdate, link, title, article in sorted_articles[:50]:
        pubdate = re.sub(r'.*([0-9]{10}).*', r'\1', pubdate)
        dt = datetime.fromtimestamp(int(pubdate))
        formatted_date = dt.strftime('%a, %d %b %Y %H:%M:%S %z')
        link = re.sub(r'id\"\:\"([0-9]{19,23})\"\,\"desc\"\:\"(.+?)\"\,\"createTime', r'https://www.tiktok.com/@enola.bedard/video/\1', link)
        title = re.sub(r'id\"\:\"([0-9]{19,23})\"\,\"desc\"\:\"(.+?)\"\,\"createTime', r'\2', title.encode('utf-8').decode('unicode_escape'))
        article = re.sub(r'originCover\"\:\"(.+?)\"', '\1', article.encode('utf-8').decode('unicode_escape'))
        author = re.sub(r'.*\/\@(.+?)\/video.*', r'\1', link)
        rss += f'''
                <item>
                <title><![CDATA[{title}]]]></title>
                <link><![CDATA[{link}]]></link>
                <description><![CDATA[{article}]]></description>
                <pubDate><![CDATA[{formatted_date}]]></pubDate>
                <author><![CDATA[{author}]]></author>
                </item>

                '''

    rss_feed = header + rss + footer

    #print(rss_feed)

else:
    rss = f'{header}\n\t<item>\n\t\t<title>出错，请检查 {date}-{hour}</title>\n\t\t<link>{url}#{date}-{hour}</link>\n\t</item>\n{footer}'
    print(rss)

with open('./tiktok.xml', 'w', encoding='utf-8') as f:
    f.write(rss_feed)
