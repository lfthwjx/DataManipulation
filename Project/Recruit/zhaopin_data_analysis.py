#!/usr/bin/python
from bs4 import BeautifulSoup
import requests, re, time, datetime
import MySQLdb

# now = datetime.datetime.now()

# url = urls[0]
# fetch and parse the website
def get_save_url(url, headers):
    global html
    html = requests.get(url, headers=headers)
    if html.status_code == 200:
        print("Website " + url + " opened")
    global soup
    soup = BeautifulSoup(html.text, 'lxml')
    html = html.text

    get_post_fact_city_num(soup, html)
    print("Fetching " + pagenum)

# soupx = soup
# htmlx = html

def get_post_fact_city_num(soupx, htmlx):
    l_position_name = []
    l_company_name = []
    l_city = []
    l_company_size = []
    # l_job_nature = []
    l_industry = []

    regex = "__ga__fullResult(.*)postname_clicksfullresult(.*)postnames_001"
    posts = soup.findAll("a", {"class": re.compile(regex)})
    for post in posts[::2]:
        post = post.get_text()
        # print(post)
        l_position_name.append(post)
    facts = soup.findAll("p", {"class": "searchResultCompanyname"})

    for fact in facts[::2]:
        fact = fact.get_text()
        l_company_name.append(fact)

    cities = soup.findAll("em", {"class": "searchResultJobCityval"})
    for city in cities[::2]:
        city = city.get_text()
        l_city.append(city)

    infos = soup.findAll("p", {"class": "searchResultCompanyInfodetailed"})
    for info in infos:
        size = info.findAll("span",{"class": "searchResultKeyval"})
        size = size[0].get_text()
        l_company_size.append(size)
    # print("nums: "+str(inums))

    labs = soup.findAll("p", {"class": "searchResultCompanyIndustry"})
    for lab in labs:
        lab = lab.get_text()
        l_industry.append(lab)

    # natures = soup.findAll("p", {"class": "searchResultJobdescription"})
    # for nature in natures:
    #     nature = nature.get_text()
    #     l_job_nature.append(nature[2])
    # l_job_nature = l_job_nature[0:29]
    # save_to_sql(l_position_name, l_company_name, l_company_size, l_city, l_job_nature, l_industry)
    save_to_sql(l_position_name, l_company_name, l_company_size, l_city, l_industry)


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"}

urls = ["http://xiaoyuan.zhaopin.com/full/0/0_0_0_0_0_-1_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90_{}_0".format(str(x)) for x in range(1, 51)]

# url = "http://xiaoyuan.zhaopin.com/full/0/0_0_0_0_0_-1_%E7%BB%9F%E8%AE%A1_2_0"
db = MySQLdb.connect(host="localhost",user="root", passwd="wanjun", db="test", use_unicode=True, charset="utf8")
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS zhilian_data_analysis")
db.commit()
cursor.execute('''CREATE TABLE IF NOT EXISTS zhilian_data_analysis(
                  position_name VARCHAR(100),
                  company_name VARCHAR(100),
                  company_size VARCHAR(100),
                  city VARCHAR(20),
                  industry VARCHAR(200)
                  )''')

def save_to_sql(l_position_name, l_company_name, l_company_size, l_city, l_industry):
    sql = """INSERT INTO zhilian_data_analysis\
       SET position_name=%s, company_name=%s, company_size=%s,city=%s, industry=%s"""
    for x in range(0, len(l_position_name)):
        # print(len(l_post_name))
        # print(x)
        # print(l_fact_name)
        cursor.execute(sql,(l_position_name[x], l_company_name[x], l_company_size[x], l_city[x], l_industry[x]))
        db.commit()
    print("Fetched successfully, stored in DB.")

for url in urls:
    try:
        time.sleep(0.5)
        pagenum = url.split("_")[-2]
        get_save_url(url=url, headers=headers)
    except:
        print("No. " + str(pagenum) + " failed")
        pass
db.close()
print("Finished!")