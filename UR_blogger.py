# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from time import strftime
import csv

bloggerList = []

class r(object):
    def __init__(self,r0=0, r1=0, r2=0, r3=0, r4=0):
        self.r0, self.r1, self.r2, self.r3, self.r4 = r0, r1, r2, r3, r4
        
def getHref(user_info):
    return user_info.select('a')[0].get('href').split('/')[2]

def getSoup(site):
    res = requests.get(site, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup

def getNowTime():
    time = strftime('%Y-%m-%d %H:%M:%S')
    return time

def getNickname(soup):
    for nickname in soup.select('.nickname'):
        return nickname.text

def getProfileRight(soup):
    profile =  soup.select('.mbd-aut-right')
    try:
        return r(profile[0].text, profile[1].text, profile[2].text, profile[3].text, 'none')
    except:
        return r('none', 'none', 'none', 'none')
    
def getProfileRightH(soup):
    profile = soup.select('.mbd-aut-right-h')
    try:
        return r(profile[0].text, profile[1].text, profile[2].text, profile[3].text, profile[4].text)
    except:
        return r('error', 'error', 'error',' error', 'error')
def getPost(soup):
    opinion = soup.select('.beauty-diary-opinion-stat')
    try:
        a = opinion[0].select('a')
        del a[0:2]
        s = ''
        for i in a:
            s = s + i.text + '\n'
            return r(a[1].text, s)
    except:
        return r('error', 'error')
    
def getBuy(soup):
    try:
        div = soup.find_all("div", class_="menu-item v-align-middle ")
        return r(div[0].text.split('(')[1].split(')')[0], div[1].text.split('(')[1].split(')')[0])
    except:
        return r('error', 'error')

def checkBlogger(blogger):
    global bloggerList
    for i in bloggerList:
        
        if blogger == i:
            return True
            break
        elif blogger == u'438359':
            return True
            break
        
    return False

def checkUpdate(bloggerName, L):
    if bloggerName in L:
        return True
    else:
        return False
    
if __name__ == '__main__':
    
    global bloggerList
    try:
        updatefile = open('data.csv', 'rb')
        upfileCsv = csv.reader(updatefile, dialect='excel', quoting=csv.QUOTE_MINIMAL)
        for i in upfileCsv:
            bloggerList = bloggerList + i
        updatefile.close()
    except:
        p=1   

    urlBlogger = 'https://www.urcosme.com/new-reviews'
    
    blogger = open('blogger.csv', 'a')
    bloggerCsv = csv.writer(blogger, dialect='excel', quoting=csv.QUOTE_MINIMAL) 
    title = ['建立時間 ', '更新時間', '來源網站', '部落客名稱', '網站Profile連結', '性別', '膚質', 
             '居住地', '年齡', '星座', '關於我', '個人特質', '常逛的地方', '我的Blog', '喜歡的美容流行雜誌', 
             '全部心得數', '心得分類', '買過數', '升火數']
    bloggerCsv.writerow(title)
    for page in range(1, 1000):
        url = urlBlogger + '?page=' + str(page)
        print ('------------'), (page), ('-------------')
        res = requests.get(url, verify=False)
        if len(res.text) < 40000:
            break
        soup = BeautifulSoup(res.text, "html.parser")
        for user_info in soup.select('.user-info'):
            href = getHref(user_info)
            if checkBlogger(href):
                
                continue
            reviewsHref = 'https://www.urcosme.com/beauty_diary/' + href + '/reviews'
            profileHref = 'https://www.urcosme.com/beauty_diary/' + href + '/profile'
            reviewsSoup = getSoup(reviewsHref)
            profileSoup = getSoup(profileHref)
            
            createTime = getNowTime()
            updateTime = 'none'
            sourceSite = reviewsHref
            bloggerName = getNickname(reviewsSoup)
            
            
            bloggerList.append(href)
            print (href)
            siteProfileLink = profileHref
            
            profileRight = getProfileRight(profileSoup)
            profileRightH = getProfileRightH(profileSoup)
            post = getPost(reviewsSoup)
            num = getBuy(reviewsSoup)
            
            sex = profileRight.r0
            skin = profileRight.r1
            location = 'tempNone'
            age = profileRight.r2
            constellation = profileRight.r3
            
            aboutMe = profileRightH.r0
            personalStyle = profileRightH.r1
            placeToGo = profileRightH.r2
            myBlog = profileRightH.r3
            magazine = profileRightH.r4
            
            allPostNum = post.r0
            postCategory = post.r1
            
            buyNum = num.r0
            fireNum = num.r1
            
            csvList = [createTime.encode('utf8'), updateTime.encode('utf8'), sourceSite.encode('utf8'), bloggerName.encode('utf8'), siteProfileLink.encode('utf8'), sex.encode('utf8'), skin.encode('utf8'),
                            location.encode('utf8'), age.encode('utf8'), constellation.encode('utf8'), aboutMe.encode('utf8'), personalStyle.encode('utf8'), placeToGo.encode('utf8'), myBlog.encode('utf8'),
                             magazine.encode('utf8'), allPostNum.encode('utf8'), postCategory.encode('utf8'), buyNum.encode('utf8'), fireNum.encode('utf8')]
            
            bloggerCsv.writerow(csvList)
            
    f = open('data.csv', 'wb')
    c = csv.writer(f, dialect='excel', quoting=csv.QUOTE_MINIMAL)
    c.writerow(bloggerList)
    f.close()
    blogger.close()
    print ('---------finish---------')
    x = raw_input()
    pass