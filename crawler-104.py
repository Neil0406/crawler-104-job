from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from tqdm import tqdm

#關鍵見字python

target = "python"

#-------------------------計算頁數--------------------------------------------------------
opt = Options()
opt.add_argument('--headless')
chrome_driver_path = "/Users/Desktop/chromedriver"             #chromedriver path
driver = webdriver.Chrome(executable_path = chrome_driver_path ,chrome_options=opt )
                               
driver.get(f'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={target}&jobcatExpansionType=0&area=6001001000&order=15&asc=0&page=2&mode=s&jobsource=2018indexpoc')
time.sleep(1)
html = driver.page_source
soup = bs(html,'lxml')
data = soup.select('#js-job-header > div.b-float-right > label:nth-child(1) > select > option')
p = data[-1].get('value')

driver.close()

#--------------------------爬取href---------------------------------------------------------

href = []
for pg in tqdm(range(1,int(p) + 1)):
    res = requests.get(f'https://www.104.com.tw/jobs/search/?ro=0&keyword={target}&jobcatExpansionType=0&order=15&asc=0&page={pg}&mode=s&jobsource=2018indexpoc')
    soup = bs(res.text,'lxml')
    x = soup.select('#js-job-content > article > div.b-block__left > h2 > a')
    for i in x:
        if  'javascript:void(0);' not in i.get('href'):
            href.append('https:' + i.get('href'))
        else:
            continue

print(len(href))

#-----------------------------------爬取內文--------------------------------------------------

opt = Options()
opt.add_argument('--headless')

chrome_driver_path = "/Users/Desktop/chromedriver"
driver = webdriver.Chrome(executable_path = chrome_driver_path ,chrome_options=opt )


job = []
company = []
content =[]
pay = []
pay_a = []      #經常性薪資資
loc = []
exp  = []    #工作經驗
lang = []    #語言能力
tool = []   #擅長工具
skill = []  #技能
other = []  #其他

for i in tqdm(href):
    try :
        driver.get(i)
    except:
        continue
    time.sleep(2)
    html = driver.page_source
    soup = bs(html,'lxml')

    #職缺    job
    data = soup.select('#app > div.job-header > div:nth-child(2) > div > div > div.job-header__title > h1')
    try:
        job.append(data[0].get('title'))
    except:
        job.append('NaN')
    #公司   company
    data = soup.select('#app > div.job-header > div:nth-child(2) > div > div > div.job-header__title > div > a:nth-child(1)')
    try:
        company.append(data[0].get('title')) 
    except:
        company.append('NaN')

    #內容     content
    data = soup.select('#app > div.container.jb-container.pt-4.position-relative > div > div.col.main > div.dialog.container-fluid.bg-white.py-6.mb-4.rounded.job-description > div.job-description-table.row > div.job-description.col-12 > p')
    try:
        if '\n' and '\r' in data[0].text:
            content.append(data[0].text.replace('\n','').replace('\r',''))
        elif '\n' in  data[0].text or '\r' not in data[0].text:
            content.append(data[0].text.replace('\n',''))
        else:
            content.append('NaN')
    except:
        content.append('NaN')
    #薪資   pay
    data = soup.select('#app > div.container.jb-container.pt-4.position-relative > div > div.col.main > div.dialog.container-fluid.bg-white.py-6.mb-4.rounded.job-description > div.job-description-table.row > div:nth-child(3) > div.col.p-0.job-description-table__data > div > p.t3.mb-0.mr-2.monthly-salary.text-primary.font-weight-bold.float-left')
    try:
        pay.append(data[0].text)
    except:
        pay.append('NaN')
    #經常性薪資 pay_a
    data = soup.select('#app > div.container.jb-container.pt-4.position-relative > div > div.col.main > div.dialog.container-fluid.bg-white.py-6.mb-4.rounded.job-description > div.job-description-table.row > div:nth-child(3) > div.col.p-0.job-description-table__data > div > p.t3.mb-0.monthly-salary-remark.text-gray-deep-dark')
    try:
        pay_a.append(data[0].text.replace('（','').replace('）','').replace(' ',''))
    except:
        pay_a.append('NaN')
    #上班地點 loc
    data = soup.select('#app > div.container.jb-container.pt-4.position-relative > div > div.col.main > div.dialog.container-fluid.bg-white.py-6.mb-4.rounded.job-description > div.job-description-table.row > div:nth-child(5) > div.col.p-0.job-description-table__data > p')
    try:
        loc.append(data[0].text.replace(' ',''))
    except:
        loc.append('NaN')
    #工作經驗  exp
    data = soup.select('#app > div.container.jb-container.pt-4.position-relative > div > div.col.main > div.dialog.container-fluid.bg-white.py-6.mb-4.rounded.job-requirement > div.job-requirement-table.row > div:nth-child(2) > div.col.p-0.job-requirement-table__data > p')
    try:
        exp.append(data[0].text)
    except:
        exp.append('NaN')
    #語言能力 lang
    data = soup.select('#app > div.container.jb-container.pt-4.position-relative > div > div.col.main > div.dialog.container-fluid.bg-white.py-6.mb-4.rounded.job-requirement > div.job-requirement-table.row > div:nth-child(5) > div.col.p-0.job-requirement-table__data > p')
    try:
        lang.append(data[0].text)
    except:
        lang.append('NaN')
    #擅長工具  tool
    data = soup.select('#app > div.container.jb-container.pt-4.position-relative > div > div.col.main > div.dialog.container-fluid.bg-white.py-6.mb-4.rounded.job-requirement > div.job-requirement-table.row > div:nth-child(6) > div.col.p-0.job-requirement-table__data > p > span > a > u')
    t = []
    w = ' / '
    if data != []:
        for i in data:
            try:
                t.append(i.text)
            except:
                t.append('NaN')
        tool.append(w.join(t))
    else:
        tool.append('NaN')

    #工作技能 skill
    data = soup.select('#app > div.container.jb-container.pt-4.position-relative > div > div.col.main > div.dialog.container-fluid.bg-white.py-6.mb-4.rounded.job-requirement > div.job-requirement-table.row > div:nth-child(7) > div.col.p-0.job-requirement-table__data > p > span > a > u')
    s = []
    if data != []:
        for i in data:
            try:
                s.append(i.text)
            except:
                s.append('NaN')
        skill.append(w.join(s))
    else:
        skill.append('NaN')


    #其他條件 other
    data = soup.select('#app > div.container.jb-container.pt-4.position-relative > div > div.col.main > div.dialog.container-fluid.bg-white.py-6.mb-4.rounded.job-requirement > div.job-requirement.col.opened > div > div.col.p-0.job-requirement-table__data > p')
    try:
        other.append(data[0].text)
    except:
        other.append('NaN')

driver.close()


#---------------------------------csv-----------------------------------------------------


import pandas as pd
import csv
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

dic = {
    '工作':job,
    '公司':company,
    '內容':content,
    '薪資':pay,
    '經常性薪資':pay_a,      #經常性薪資資
    '地點':loc,
    '經驗':exp,    #工作經驗
    '語言':lang,    #語言能力
    '工具':tool,   #擅長工具
    '技能':skill,  #技能
    '其他':other  #其他
}


df = pd.DataFrame(dic)
data = df.to_dict('recode')

#地區過濾（台北市）

tp = []
for i in data:
    if '台北市' in i['地點']:
         tp.append(i)
df = pd.DataFrame(tp)
     
df.to_csv('104.csv',index=True, index_label= 'id')