import requests
import re
import json
import time


def get_one_page(url):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    try:
        r=requests.get(url,headers=headers)
        r.encoding=r.apparent_encoding
        if r.status_code==200:
            return r.text
        return None
    except:
        print('shibai')

def parser_one_page(html):
    partern=re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    item=re.findall(partern,html)
    for i in item:
        print(i)
        yield {
            '排名': i[0],
            '电影名称': i[1],
            '演员': i[2].strip()[3:],
            '上映时间': i[3].strip()[5:],
            '评分': i[4] + i[5]
        }

def write_to_file(content):
    with open('result.txt','a',encoding='UTF-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')

def main(offset):
    url='http://maoyan.com/board/4?offset='+str(offset)
    html=get_one_page(url)
    parser=parser_one_page(html)
    for p in parser:
        write_to_file(p)

if __name__ == '__main__':
   for i in range(10):
       main(offset=i*10)
