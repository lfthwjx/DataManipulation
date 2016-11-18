__author__ = 'Jun Wang'
#!/usr/bin/python
from bs4 import BeautifulSoup
import requests, time
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

    get_post_fact(soup, html)
    # print("Fetching " + pagenum)

# soupx = soup
# htmlx = html

def get_post_fact(soupx, htmlx):
    l_position_name = []
    l_company_name = []
    l_city = []
    l_company_size = []
    l_salary = []
    l_education = []

    #regex = "__ga__fullResult(.*)postname_clicksfullresult(.*)postnames_001"
    posts = soup.findAll("a", {"style": "font-weight: bold"})
    for post in posts:
        post = post.get_text()
        l_position_name.append(post)

    facts = soup.findAll("td", {"class": "gsmc"})
    for fact in facts:
        fact = fact.get_text()
        l_company_name.append(fact)

    cities = soup.findAll("td", {"class": "gzdd"})
    for city in cities:
        city = city.get_text()
        l_city.append(city)

    infos = soup.findAll("li", {"class": "newlist_deatil_two"})
    # info = infos[0]
    # info = info.findAll("span")[3].get_text()
    # str(info.encode('utf-8')).replace("\xe5\xad\xa6\xe5\x8e\x86\xef\xbc\x9a","").decode('utf-8')
    # str(info.encode('utf-8')).replace("\xe5\x85\xac\xe5\x8f\xb8\xe8\xa7\x84\xe6\xa8\xa1\xef\xbc\x9a","").replace("\xe4\xba\xba","").decode("utf-8")
    for info in infos:
        info = info.findAll("span")
        size = info[2].get_text()
        size = str(size.encode('utf-8')).replace("\xe5\x85\xac\xe5\x8f\xb8\xe8\xa7\x84\xe6\xa8\xa1\xef\xbc\x9a","").replace("\xe4\xba\xba","").decode("utf-8")
        # size = info.findAll("span",{"class": "searchResultKeyval"})
        # size = size[0].get_text()
        l_company_size.append(size)
        educ = info[3].get_text()
        educ = str(educ.encode('utf-8')).replace("\xe5\xad\xa6\xe5\x8e\x86\xef\xbc\x9a","").replace("\xe7\xbb\x8f\xe9\xaa\x8c\xef\xbc\x9a","").decode('utf-8')
        l_education.append(educ)
    # print("nums: "+str(inums))

    salarys = soup.findAll("td", {"class": "zwyx"})
    for salary in salarys:
        salary = salary.get_text()
        l_salary.append(salary)

    # natures = soup.findAll("p", {"class": "searchResultJobdescription"})
    # for nature in natures:
    #     nature = nature.get_text()
    #     l_job_nature.append(nature[2])
    # l_job_nature = l_job_nature[0:29]
    # save_to_sql(l_position_name, l_company_name, l_company_size, l_city, l_job_nature, l_industry)
    save_to_sql(l_position_name, l_company_name, l_company_size, l_city, l_salary, l_education)


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"}

urls = ["http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA&kw=%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98&p={}&isadv=0".format(str(x)) for x in range(1, 29)]

# url = "http://xiaoyuan.zhaopin.com/full/0/0_0_0_0_0_-1_%E7%BB%9F%E8%AE%A1_2_0"
db = MySQLdb.connect(host="localhost",user="root", passwd="wanjun", db="test", use_unicode=True, charset="utf8")
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS zhaopin_data_mining")
db.commit()
cursor.execute('''CREATE TABLE IF NOT EXISTS zhaopin_data_mining(
                  position_name VARCHAR(100),
                  company_name VARCHAR(100),
                  company_size VARCHAR(100),
                  city VARCHAR(20),
                  salary VARCHAR(50),
                  education VARCHAR(50)
                  )''')

def save_to_sql(l_position_name, l_company_name, l_company_size, l_city, l_salary, l_education):
    sql = """INSERT INTO zhaopin_data_mining\
       SET position_name=%s,company_name=%s,company_size=%s,city=%s,salary=%s,education=%s"""
    for x in range(0, len(l_position_name)):
        # print(len(l_post_name))
        # print(x)
        # print(l_fact_name)
        cursor.execute(sql,(l_position_name[x], l_company_name[x], l_company_size[x], l_city[x], l_salary[x], l_education[x]))
        db.commit()
    print("Fetched successfully, stored in DB.")

for url in urls:
    try:
        time.sleep(0.5)
        # pagenum = url.split("_")[-2]
        get_save_url(url=url, headers=headers)
    except:
        # print("No. " + str(pagenum) + " failed")
        pass
db.close()
print("Finished!")