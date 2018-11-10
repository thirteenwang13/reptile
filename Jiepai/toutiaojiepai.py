import time
import requests
import os
from hashlib import md5

def get_html(url,offset):
    headers={
        'referer':'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        'x-requested-with':'XMLHttpRequest'
    }
    data={
        'offset':offset,
        'format':'json',
        'keyword':'街拍',
        'autoload':'true',
        'count':'20',
        'cur_tab':'3',
        'from':'gallery'
    }
    try:
        r=requests.get(url,headers=headers,params=data)
        if r.status_code==200:
            return r.json()
        else:
            HTTPError=requests.HTTPError
            print('An HTTP error occurred'+str(HTTPError))
    except requests.ConnectionError:
        print('A Connection error occurred')


def parser_html(html):
    jiepai = {}
    if html.get('data'):
        for item in html.get('data'):
            if item.get('cell_type') is not None:
                continue
            jiepai['title']=item.get('title')
            jiepai['create_time']=item.get('create_time')
            print(item.get('title'))
            for image in item.get('image_list'):
                jiepai['pictureurl'] = 'https:' +image.get('url')
                yield jiepai
    else:
        print('Other tag is not data')

def save_file(item):
    img_path = 'img' + os.path.sep + item.get('title') #os.path.sep = //
    if not os.path.exists(img_path):
        os.makedirs(img_path)
        print('文件夹创建成功')
    try:
        picture = requests.get(item.get('pictureurl'))
        if picture.status_code == 200:
            #file_path=img_path + os.path.sep +item.get('create_time')+'jpg'
            file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'.format(
                file_name=md5(picture.content).hexdigest(),
                file_suffix='jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(picture.content)
                print('图片已下载 %s' % file_path)
            else:
                print('已经下载完成', file_path)
    except requests.ConnectionError:
        print('A Connection error occurred，Failed to Save Image，item %s' % item)

if __name__ == '__main__':
    url='https://www.toutiao.com/search_content/?'
    for offset in range(0,220,20):
        html=get_html(url,offset)
        time.sleep(2)
        items=parser_html(html)
        for item in items:
            save_file(item)