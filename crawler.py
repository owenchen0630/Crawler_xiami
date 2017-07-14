#coding=utf-8
import requests
from bs4 import BeautifulSoup
from asyncio.tasks import sleep
import time
import mysql.connector



MYSQLUSER = USERNAME
MYSQLPASSWD = PASSWD
XIAMIUSER = TELENUM
XIAMMIPASSWD = PASSWORD
L = []

conn = mysql.connector.connect(host='139.199.12.31',user=MYSQLUSER,password=MYSQLPASSWD,database='xiami')
cursor = conn.cursor()
cursor.execute('truncate table all_info_lists')

def login():
    username = TELENUM
    passwd = PASSWORD
    LOGIN_URL = 'https://login.xiami.com/member/login'
    data = {'email': username, 'password': passwd}
    response = requests.post(LOGIN_URL, data=data)


def mgr_url(candicate_url):
    candicate_url = candicate_url[6:-1]
    L.append(candicate_url)
    if L.count(candicate_url) > 1:
        L.pop()
    print(len(L))
    
def read_url():
    if len(L) == 0:
        return "end" 
    url = L[0]
    L.pop(0)
    return url           
         
def init():
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13 '
    headers = { 'User-Agent' : user_agent }
    i = 1
    while i <= 41:
        url = 'http://www.xiami.com/search/orinew/page/' + str(i) + '?spm=a1z1s.3061701.6856305.148.UhCvBs&key=&order=weight'
        time.sleep(2)
        r = requests.get(url, headers = headers)
        html_doc = r.text
        soup = BeautifulSoup(html_doc,
                             'html.parser',
                             from_encoding='utf-8')
        links = soup.find_all("div", class_ = "block_cover")
        for node in str(links).split():
            if node[:7] == 'href="h':
                print(node)
                mgr_url(node)
        i += 1
#               print(str(links).split())

def crawler():
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13 '
    headers = { 'User-Agent' : user_agent }
    url = read_url()
#    url = "http://www.xiami.com/collect/267962214"
    while url != "end":
        print(url)
        time.sleep(2)
        r = requests.get(url, headers = headers)
        html_doc = r.text
        soup = BeautifulSoup(html_doc,
                            'html.parser',
                            from_encoding='utf-8')
        img_name = soup.find_all("p", class_ = "cover")
        print(str(img_name).split())
        links = soup.find_all("div", class_ = "cdinfo")
        print(str(links).split())
        
        try:
            img_link = str(img_name).split()[7]
            name = str(img_name).split()[11]
            img_link = img_link[6:-1]
            name = name[5:-1]
            play = str(links).split()[-10]
            star = str(links).split()[-4]
            print(str(links).split()[-10])
            cursor.execute("insert into all_info_lists(link, img_link, name, play, star) values(' " + url + "'," \
                                        + "'"  + img_link + "','" + name + "', '" + play +"'," \
                                        + "'"  + star + "')" )
            conn.commit()
        except IndexError:
            pass
        url = read_url()
        print(len(L))
                           
def main():
    login()
    init()
    crawler()
    
if __name__ == '__main__':
    main()