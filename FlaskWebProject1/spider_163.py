import requests,json,traceback
from bs4 import BeautifulSoup


url="http://home.163.com/19/0418/07/ED1D294L001081EI.html"
url_hots="http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/%s/comments/hotList?ibc=newswap&offset=0&limit=%s&headLimit=3&tailLimit=1&callback=hotList&ibc=newswap"
url_rank="http://news.163.com/special/0001386F/rank_whole.html"
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"}

def s163(url,num):
    try:
        code=url.split("/")[-1].split(".")[0]
    except:
        return "error4"
    try:
        r=requests.get(url_hots%(code,num),headers)
    except:
        print("error1")
        return "error1"
    try:
        s=r.text.strip('hotList(\n').strip(");")
        d=json.loads(s)
    except:
        return r.text
    try:
        u=list()
        for i in d['comments'].values():
            try:
                u.append(i['content'].strip())
            except:
                print("error2")
                continue
    except:
        return "error3"
    return u
if __name__ =="__main__":
    print(s163(url,40))