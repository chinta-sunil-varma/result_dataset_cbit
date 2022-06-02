from fake_user_agent.main import user_agent
import  requests
from bs4 import BeautifulSoup
import pandas as pd
#user agen headers for entering the website
ua=user_agent('chrome')
sem=int(input('enter the semister'))
df=pd.DataFrame(columns=['NAME','SGPA','CGPA'])
def getResult(start,end,le=False):
        global  sem
        if(le==True):
            if(sem>=3):
                sem=sem-2
            else:
                return

        for roll in range(start,end):
            username=str(roll)+'P'
            password=str(roll)+'P'
            headers={'User-Agent':str(ua)}
            with requests.Session() as s:
                url="https://erp.cbit.org.in/beeserp/Login.aspx"
                g=s.get(url,headers=headers)
                src=g.content
                soup=BeautifulSoup(src,'lxml')
                lis=soup.find_all('input',{'type':'hidden'})
                a=[]
                for i in lis:
                    a.append(i.attrs['value'])

                payload={'__VIEWSTATE':a[3],'__VIEWSTATEGENERATOR':a[4],'__EVENTVALIDATION':a[5],'txtUserName':username,'btnNext':'Next'}
                post2 = s.post('https://erp.cbit.org.in/beeserp/login.aspx', data=payload,allow_redirects=True)

                res=post2.content
                soup1=BeautifulSoup(res,'lxml')
                lis1=soup1.find_all('input',{'type':'hidden'})
                b=[]
                for i in lis1:
                    b.append(i.attrs['value'])

                payload1 = { '__VIEWSTATE': b[0],
                           '__VIEWSTATEGENERATOR': b[1], '__EVENTVALIDATION': b[2],'txtPassword': password, 'btnSubmit':'Submit'
                           }
                # print(post2.request.url)
                post1 = s.post(post2.request.url, data=payload1)

                # print('suceesfully bypassed password page')
                # with open ('password.html','w')as f:
                #     f.write(post1.text)
                #https://erp.cbit.org.in/beeserp/StudentLogin/Student/OverallResultStudent.aspx
                #https://erp.cbit.org.in/beeserp/StudentLogin/Student/OverallMarksSemwise.aspx
                overall_result=s.get('https://erp.cbit.org.in/beeserp/StudentLogin/Student/OverallResultStudent.aspx')
                # with open ('testting.html','w')as f:
                #     f.write(overall_result.text)
                    # additional work
                rslt_page=overall_result.content
                parser=BeautifulSoup(rslt_page,'lxml')
                final_list=parser.find_all('tr',{'valign':'middle'})
                name=parser.find('span',{'id':'ctl00_cpHeader_ucStudCorner_lblStudentName'})
                try:
                  name=name.string.replace('WELCOME','').strip()
                except:
                    continue
                try:
                  container=final_list[sem].find_all('td')[2:4]
                except:
                    continue

                df.loc[len(df.index)] = [name,container[0].string,container[1].string]
                # print(df)
                print(name+' has been inserted into dataframe')

getResult(160120747001,160120747060)
# getResult(160120737182,160120737183)
# getResult(160120737307,160120737313,le=True)
df.to_csv('AIDS_result.csv')
