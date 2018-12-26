import requests
from lxml import etree
import time
import random
import csv

urllist = []
headers={
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
	}
def Get_url(page):  # 获取连接
    url = "https://search.51job.com/list/000000,000000,0000,00,9,99,数据分析师,2,%d.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%%2C0&radius=-1&ord_field=1&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=" % page
    # 关键词“数据分析师”，地点：全国，按时间排序
    try:
        r = requests.get(url,headers=headers,timeout=10)
        urlcontent = etree.HTML(r.text, parser=etree.HTMLParser(encoding="gbk"))
        myurls = urlcontent.xpath("//p[@class='t1 ']/span/a/@href")
        for myurl in myurls:
            urllist.append(myurl)
    except:
        print("第%d页没有获取！" % page)

data = []

def parser_url(urllist):  # 解析详情页内容
    for myurl in urllist:
        try:
            resp = requests.get(myurl)
            maincontent = etree.HTML(resp.text, parser=etree.HTMLParser(encoding="gbk"))
            job = maincontent.xpath("string(//div[@class='cn']/h1)")
            salary = maincontent.xpath("string(//div[@class='cn']/strong)")
            company = maincontent.xpath("string(//a[@class='catn'])")
            companytype = maincontent.xpath("string(//p[@class='at'][1])")
            companysize = maincontent.xpath("string(//p[@class='at'][2])")
            companyfield = maincontent.xpath("string(//p[@class='at'][3])")
            requirements = maincontent.xpath("string(//p[@class='msg ltype'])")
            welfare = maincontent.xpath("string(//div[@class='t1'])")
            jobdescription = maincontent.xpath("string(//div[@class='bmsg job_msg inbox'])")
            workplace = maincontent.xpath("string(//div[@class='bmsg inbox']/p[@class='fp'])")
            data.append([myurl, job.replace("\t", "").encode("gbk", "ignore").decode("gbk"),
                         salary.replace("\t", "").encode("gbk", "ignore").decode("gbk"),
                         company.replace("\t", "").encode("gbk", "ignore").decode("gbk"),
                         companytype.replace("\t", "").encode("gbk", "ignore").decode("gbk"),
                         companysize.replace("\t", "").encode("gbk", "ignore").decode("gbk"),
                         companyfield.replace("\t", "").encode("gbk", "ignore").decode("gbk"),
                         requirements.replace("\t", "").encode("gbk", "ignore").decode("gbk"),
                         welfare.replace("\t", "").encode("gbk", "ignore").decode("gbk"),
                         jobdescription.replace("\t", "").encode("gbk", "ignore").decode("gbk"),
                         workplace.replace("\t", "").encode("gbk", "ignore").decode("gbk")])
        except:
            print("%s没有获取" % myurl)

if __name__ == "__main__":
    for page in range(1, 1000):  #前n页
        Get_url(page)
        time.sleep(random.uniform(0.7, 1.5)) #略微歇会
    parser_url(urllist)
    time.sleep(random.uniform(0.7, 2.5)) #在歇会
    with open("51job数据分析.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["url", "job", "salary", "company", "companytype", "companysize", "companyfield", "requirements", "welfare",
             "jobdescription", "workplace"])
        for k in data:
            writer.writerow(k)
