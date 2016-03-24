#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import csv
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

rules = {
    'inews_qq': ('p', 'text'),
    'toutiao': ('div', 'article-content'),
    'weixin': ('div', 'rich_media_content')
}

def match_rule(url):
    source = ''

    if url.find('view.inews.qq.com') >= 0:
        source = 'inews_qq'
    #else:
    #    print url.find('view.inews.qq.com')


    #if url.find('163.com') >= 0:
    #    source = '163'
    if url.find('toutiao.com') >= 0:
        source = 'toutiao'
    if url.find('weixin.qq.com') >= 0:
        source = 'weixin'

    if source != '':
        return source, rules[source][0], rules[source][1]

    raise Exception("No match!")



    
def parse_url(url, fout):
    print 'Now parse the url: ' + url

    try:
        source, tag_name, class_name = match_rule(url)
    except Exception as e:
        print e
        return


    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc)

    csv_source = source

    csv_title = soup.title.string

    csv_title2 = soup.find('p', class_ = 'title')
    if csv_title2 != None:
        csv_title2 = csv_title2.get_text()
    else:
        csv_title2 = ''

    csv_content = ""
    content = soup.find_all(tag_name, class_ = class_name)
    if len(content) == 1:
        content = content[0].find_all('p')

    #print content.get_text()
    for line in content:
        # try to remove the <p> tags
        csv_content += line.get_text() + '\n'

    fout.write("\"")
    for x in [csv_source, url, csv_title, csv_title2, csv_content]:
        fout.write(x + "\",\"")
    fout.write("\"\r")

    print '==================='
    return


if __name__ == '__main__':

    urls = ['http://view.inews.qq.com/a/NEW2016011805870804?from=groupmessage&isappinstalled=1&openid=o04IBAKbN4pAC4lA9XOzYfTkVzW0&key=710a5d99946419d9b21f713eeb80581d20ff9aef23f93e26acb53dcdeb1552d57edbff55f81182e2aabff938b22d1592&version=11020201&devicetype=iMac+MacBookPro11%2C1+OSX+OSX+10.11.2+build(15C50)&cv=0x11020201&dt=14&lang=zh_CN&pass_ticket=aQj0A5q%2Bj8kayo1G2kDvCf8A1Nb3nhH2EBjnSNeB4bvv%2BNIzQ%2Bf9PDHRNtD7n5gS',\
'http://3g.163.com/ntes/special/0034073A/wechat_article.html?docid=BDK4F3C705118B5G&from=groupmessage&isappinstalled=1',\
'http://m.toutiao.com/i6238828797404119553/?tt_from=weixin&utm_campaign=client_share&app=news_article&utm_source=weixin&iid=3396543334&utm_medium=toutiao_android&wxshare_count=3&from=groupmessage&isappinstalled=0',\
'http://mp.weixin.qq.com/s?__biz=MTQzMjE1NjQwMQ==&mid=404750083&idx=1&sn=b358067656c9866c51e3e077146a36c8&scene=1&srcid=0115s9cIzsF3nsHCN2AsUYzt&from=groupmessage&isappinstalled=0#wechat_redirect',\
'http://view.inews.qq.com/a/FIN2016011603512504?from=groupmessage&isappinstalled=1']


    fout = open('output.csv', 'w')
    fout.write(codecs.BOM_UTF8)

    for k in range(len(urls)):
        parse_url(urls[k], fout)
        
    fout.close()

    #f = open('ExcelUtf8.csv', 'w')
    #t = u'中国人'
    #f.write(codecs.BOM_UTF8)
    #f.write('\xEF\xBB\xBF');
    #f.write("傻逼,哈哈哈")

    #fout = open('csv_test.csv', 'w')

    
    #fout.write('王国赛' + ',' + '哈哈哈')
    #fout.close()

    '''
    writer = csv.writer(csvfile)

    writer.writerow(['姓名', '年龄', '电话'])

    data = [
        ('小河', '25', '1234567'),
        ('小芳', '18', '789456')
    ]
    writer.writerows(data)

    csvfile.close()
    '''

