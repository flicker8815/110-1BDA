import re
import requests
from urllib import error
from bs4 import BeautifulSoup
import os
 
num = 0
numPicture = 0
file = ''
List = []
 
def Find(url, A):
    global List
    print('Counting img numbers......')
    t = 0
    i = 1
    s = 0
    while t < 1000:
        Url = url + str(t)
        try:
            Result = A.get(Url, timeout=7, allow_redirects=False)
        except BaseException:
            t = t + 60
            continue
        else:
            result = Result.text
            pic_url = re.findall('"objURL":"(.*?)",', result, re.S)  
            s += len(pic_url)
            if len(pic_url) == 0:
                break
            else:
                List.append(pic_url)
                t = t + 60
    return s
 
def recommend(url):
    Re = []
    try:
        html = requests.get(url, allow_redirects=False)
    except error.HTTPError as e:
        return
    else:
        html.encoding = 'utf-8'
        bsObj = BeautifulSoup(html.text, 'html.parser')
        div = bsObj.find('div', id='topRS')
        if div is not None:
            listA = div.findAll('a')
            for i in listA:
                if i is not None:
                    Re.append(i.get_text())
        return Re
 
def dowmloadPicture(html, keyword):
    global num
    # t =0
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)  
    print('Found:' + keyword + 'images，ready to download now...')
    for each in pic_url:
        print('Downloading ' + str(num + 1) + ' pic，picture\naddress: ' + str(each))
        try:
            if each is not None:
                pic = requests.get(each, timeout=7)
            else:
                continue
        except BaseException:
            print('Error，the pic can not download')
            continue
        else:
            string = './' + keyword + '/' + keyword + '_' + str(num) + '.jpg'
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            num += 1
        if num >= numPicture:
            return
 
if __name__ == '__main__': 
    
    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Upgrade-Insecure-Requests': '1'
        }
 
    A = requests.Session()
    A.headers = headers
     
    ###############################
       
    tm = int(input('Input number that image you want to download :'))
    numPicture = tm
    line_list = []
    with open('./name.txt', encoding='utf-8') as file:
        line_list = [k.strip() for k in file.readlines()] 
 
    for word in line_list:
        url = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&pn='
        tot = Find(url,A)
        Recommend = recommend(url) 
        print('%srelatived image total %d' % (word, tot))
        file = word
        y = os.path.exists(file)
        if y == 1:
            print('This file has already exist，pls input again.')
            file = word+'file2'
            os.mkdir(file)
        else:
            os.mkdir(file)
        t = 0
        tmp = url
        while t < numPicture:
            try:
                url = tmp + str(t)
                result = A.get(url, timeout=10, allow_redirects=False)
                print(url)
            except error.HTTPError as e:
                print('network error, do it for later.')
                t = t + 60
            else:
                dowmloadPicture(result.text, word)
                t = t + 60
        numPicture = numPicture + tm
        
    print('Stop searching.')
