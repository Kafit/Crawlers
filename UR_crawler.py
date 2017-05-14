# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
import datetime

from time import strftime

class r(object):
    def __init__(self,r0=0, r1=0, r2=0, r3=0):
        self.r0, self.r1, self.r2, self.r3 = r0, r1, r2, r3
        
        
def getNowTime():
    time = datetime.datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    return time
def checkMiBrand(brand_item):
    if brand_item.find_all('script'):
        return True
    else:
        return False
    
def getSourceSite(brand_item):
    result = brand_item.find_all('a')
    return str(result).split('"')[1]

def getNo1Product(sourceSite):
    res = requests.get('https://www.urcosme.com' + sourceSite)
    soup = BeautifulSoup(res.text, "html.parser")
    info_block = soup.select('.info-block')
    try:
        a = info_block[0].select('a')
        uc_stat = info_block[0].select('.uo-stat')
        uc_point = info_block[0].select('.uc-point')
        return  r(a[1].text.strip(), uc_stat[0].text.split('N')[0], uc_point[0].text)
    except IndexError:
        return r('none', 'none', 'none')

def getmiSite(brand_item):
    return brand_item.select('.gfy-s-limited')[0].get('href')

def getProductNum(miSite):
    res = requests.get('https://www.urcosme.com' + miSite)
    soup = BeautifulSoup(res.text, "html.parser")
    brand_element = soup.select('.brand_element')
    li = brand_element[0].select('li')
    return r(li[2].text, li[3].text, li[4].text, li[5].text)

def getFB(miSite):
    res = requests.get('https://www.urcosme.com' + miSite)
    soup = BeautifulSoup(res.text, "html.parser")
    iframe = soup.select('a')
    for i in iframe:
        if i.text == u'品牌粉絲專頁' :
            return i.get('href')

def getFbName(fbSite):
    try:
        res = requests.get(fbSite)
        soup = BeautifulSoup(res.text, "html.parser")
        FBid = soup.find(id = 'pageTitle')
        return FBid.text
    except:
        return 'none'
def getFbFan(FBPageLink):
    try:
        res = requests.get(FBPageLink)
        soup = BeautifulSoup(res.text, "html.parser")
        sqk = soup.select('._5sqk')
        return sqk[0].text.split(' ')[0]
    except:
        return 'none'
    
def compare(brand):
    global brandList
    for i in brandList:
        if brand == i:
            return True
    return False

if __name__ == '__main__':
    
    brandList = []
    try:
        updatefile = open('data.csv', 'rb')
        upCsv = csv.reader(updatefile, dialect='excel', quoting=csv.QUOTE_MINIMAL)
        for i in upCsv:
            brandList = brandList + i
        updatefile.close()
    except:
        p = 1
    url = 'https://www.urcosme.com/find-brand'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    
    
    dictData = dict()
    
    title = ['CreateTime', 'UpdateTime', 'SourceSite', 'Brand', 'MiBrand', 'ProductNum', 'AllPostNum',
                'FireNum', 'BuyNum', 'No1ProductName', 'No1ProductUrCosmeRank', 'No1ProductPostNum',
                'FBPageName', 'FBPageLink', 'FBPageFanNum']

    f = open('1.csv', 'wb')
    c = csv.writer(f, dialect='excel', quoting=csv.QUOTE_MINIMAL) 
    c.writerow(title)
    count = 0
    for brand_item in soup.select('.brand-item'):

        t = brand_item.text.split(">")
        brandName = t[0].strip()
        
        createTime = strftime('%Y-%m-%d %H:%M:%S')
        updateTime = 'none'
        sourceSite = getSourceSite(brand_item)
        MiBrand = checkMiBrand(brand_item)
        Product = getNo1Product(sourceSite)
        no1Product = Product.r0
        no1ProductUrCosmeRank = Product.r1
        no1ProductPostNum = Product.r2

        if MiBrand:
            miSite = getmiSite(brand_item)
            miProduct = getProductNum(miSite)
            productNum, allPostNum, fireNum, buyNum = miProduct.r0, miProduct.r1, miProduct.r2, miProduct.r3
            FBPageLink = getFB(miSite)
            FBPageNum = getFbName(FBPageLink)
            FBPageFanNum = getFbFan(FBPageLink)
        else:
            #brandObj = Brand(createTime, updateTime, sourceSite, brandName, MiBrand, no1Product, no1ProductUrCosmeRank, no1ProductPostNum)
            productNum, allPostNum, fireNum, buyNum = 'none', 'none', 'none', 'none'
            FBPageNum, FBPageLink, FBPageFanNum = 'none', 'none', 'none'
        brandList.append(brandName)
        #dictData[brandName] = brandObj
        csvList = [createTime.encode('utf8'), updateTime.encode('utf8'), 'https://www.urcosme.com'+sourceSite.encode('utf8'), brandName.encode('utf8'), str(MiBrand).encode('utf8'),
                        productNum.encode('utf8'), allPostNum.encode('utf8'), fireNum.encode('utf8'), buyNum.encode('utf8'),
                        no1Product.encode('utf8'), no1ProductUrCosmeRank.encode('utf8'), no1ProductPostNum.encode('utf8'),
                        FBPageNum.encode('utf8'), FBPageLink.encode('utf8'), FBPageFanNum.encode('utf8')]

        print (count),(csvList)
        count = count + 1
        c.writerow(csvList)
        
        
    f = open('data.csv', 'a')
    c = csv.writer(f, dialect='excel', quoting=csv.QUOTE_MINIMAL)
    c.writerow(brandList)
    print ('final')
    pass


