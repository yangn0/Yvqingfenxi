"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import sys
sys.path.append("C:\\Users\\79230\\Desktop\\FlaskWebProject1\\main\\")
import demoTest
from flask import Flask,url_for,redirect,render_template,request
import spider_163,spider_jd,spider_qq,time
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app
p=list()

@app.route('/',methods={'POST','GET'})
def index():
    if request.method == 'GET':
        return render_template('WebPage2.html')
    else:
        try:
            t_flag=time.time()
            web=request.form.get('web')
            url=request.form.get('url')
            if(web=="163"):
                print("163")
                l=spider_163.s163(url,40)
            if(web=="jd"):
                print("jd")
                l=spider_jd.sjd(url,5)
            if(web=="qq"):
                print("qq")
                l=spider_qq.sqq(url)
            #print(demoTest.main(url)[0])

            u=list()
            d=dict()
            d["积极"]=0
            d["消极"]=0
            for i in l:
                if(str(demoTest.main(i)[0])=='1'):
                    s='积极'
                    d[s]+=1
                else:
                    s='消极'
                    d[s]+=1
                u.append(i+' '+s)
        
            result='评论总体趋向积极' if d["积极"]>d['消极'] else '评论总体趋向消极'
            p.append(url+' '+result)
            print(time.time()-t_flag)
            return render_template('WebPage2.html',
                                   messages=u,
                                   result=result,
                                   recoreds=p,
                                   value=url,
                                   num1=d["积极"],
                                   num2=d["消极"]
                                   )
        except:
            return "error"

if __name__ == '__main__':
    #app.run('0.0.0.0', '80')
    app.run('0.0.0.0', '80')
