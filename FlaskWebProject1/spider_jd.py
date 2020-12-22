import requests,json,traceback


headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"}

url_mod="https://sclub.jd.com/comment/productPageComments.action?productId=%s&score=0&sortType=6&page=%s&pageSize=10&isShadowSku=0&fold=1"
def sjd(url,pages):
    #10 per page
    u=list()
    headers["Referer"]=url
    id=url.split('/')[-1].split('.')[0]
    for page in range(int(pages)):
        try:
            r=requests.get(url_mod%(id,page),headers=headers)
            d=json.loads(r.text)
            for i in d['comments']:
                u.append(i['content'])
        except:
            pass
    return u


if __name__ =="__main__":
    u=sjd('https://item.jd.com/6027055.html',10)
    print(u)
    print(len(u))