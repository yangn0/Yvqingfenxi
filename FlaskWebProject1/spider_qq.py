import requests,json,traceback


headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"}

url_mod="http://coral.qq.com/article/%s/comment/v2?orinum=30&oriorder=o&pageflag=1&cursor=0&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=1"
def sqq(url):
    #10 per page
    u=list()
    id=url.split('/')[-1]
    try:
        r=requests.get(url_mod%(id),headers=headers)
        d=json.loads(r.text)
        for i in d['data']['oriCommList']:
            u.append(i['content'])
    except:
        pass
    return u


if __name__ =="__main__":
    u=sqq('http://coral.qq.com/4016450430')
    print(u)
    print(len(u))
