# -* - coding: UTF-8 -* - 

import urllib2, pyquery, time, os, sys

# host = 'https://m.booktxt.net'
# host = 'https://m.booktxt.net'
# path = '3'
# book_id = '1861'
host = str.rstrip(sys.argv[1], '/')
path = sys.argv[2]
book_id = sys.argv[3]
menu_id = sys.argv[4]
name = sys.argv[5]


menuUrl = host + '/' + path + '/' + menu_id + '.html'

os.system('rm -rf output/' + path + '/'+book_id+'*')

if not os.path.isdir('output/' + path + '/' + book_id):
    os.makedirs('output/' + path + '/' + book_id)


def getter():
    doc = pyquery.PyQuery(menuUrl, parser="html", opener=opener)

    with open('output/'+path+'/' + book_id + '/index.html', 'a') as f:
        f.write('<html><body style="font-size:54px"><h1>'+name+'</h1>')

    for i in doc('select[name="pageselect"]>option').items():
        pageUrl = host + i.val()
        pageDoc = pyquery.PyQuery(pageUrl, parser="html", opener=opener)
        menu = pageDoc('div.info_chapters>ul')
        for a_tag in menu('a').items():
            href = str.lstrip(a_tag.attr('href'), '/')
            chapter_url = host + '/' +href
            page = pyquery.PyQuery(chapter_url, opener=opener)
            title = page('head>title').html().encode('utf-8')
            readpage = page('div.page_chapter1').html().encode('utf-8')
            content = page('div#novelcontent').html().encode('utf-8')

            html = '<html><body style="font-size:54px">'
            html += title + content + '</br></br><p>' + readpage + '</p>'
            html += '</body></html>'
            print chapter_url
            with open('output/' + href, 'w') as f:
                f.write(html)

        with open('output/'+path+'/' + book_id + '/index.html', 'a') as f:
            f.write(menu.html().encode('utf-8'))

    with open('output/'+path+'/' + book_id + '.html', 'a') as f:
        f.write('</body></html>')

def opener(url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)

    # rs = response.decode('GBK').encode('utf-8')
    rs = unicode(response.read(), 'gbk')
    return rs


def main():
    getter()


if __name__ == "__main__":
    main()
