import sys

import requests
from bs4 import BeautifulSoup
import re



def getFilename_fromCd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
       return None
    return fname[0]


headers={'user-agent':'<your header goes here' }

with requests.Session() as s:
    url="https://learning.cbit.org.in/"
    g=s.get(url,headers=headers)
    src=g.content

    soup=BeautifulSoup(src,'html.parser')
    lis=soup.find_all('input',{'type':'hidden'})

    var=lis[0].attrs['value']
    payload = {'username': '', 'password': '', 'logintoken': var} #give here your original lms credentials
    post = s.post('https://learning.cbit.org.in/login/index.php', data=payload)
    while(1):
        a= input('enter your course name to fetch the details')
        course_payload={'areaids':'core_course-course','q':a}
        course_post=s.get('https://learning.cbit.org.in/course/search.php',params=course_payload)
        with open('file.html', 'w') as obj:
          obj.write(course_post.text)
        parse=BeautifulSoup(course_post.content,'lxml')
        count=0
        output=[]
        lis=parse.find_all(class_='coursebox clearfix odd first' )
        for i in lis:
            a=i.find(class_='coursename')
            print(str(count)+' .'+a.find('a').text)
            output.append(a)
            count+=1
        lis = parse.find_all(class_='coursebox clearfix even')
        for i in lis:
            a = i.find(class_='coursename')
            print(str(count)+' .'+a.find('a').text)
            output.append(a)
            count+=1

        lis = parse.find_all(class_='coursebox clearfix odd')
        for i in lis:
            a = i.find(class_='coursename')
            print(str(count)+' .'+a.find('a').text)
            output.append(a)
            count+=1
        # print(output)
        if(count!=0):
            choice=int(input('from above list of courses select the desired course to view its notes '))
            url=output[choice].find('a')

            java=s.get(url.attrs['href'])
            with open('file.html', 'w') as obj:
             obj.write(java.text)
            parse=BeautifulSoup(java.content,'lxml')
            lis=parse.find_all(class_='activity resource modtype_resource')

            notes_count=0
            if(lis):
               for i in lis:
                  print(str(notes_count)+'. '+i.find('a').text )
                  notes_count+=1
                  print(i.find('a').attrs['href'])

            elif(lis==[]):
                print('******* EITHER THE NOTES ARE NOT PRESENT OR YOU ARE NOT ELIGIBLE TO ACCESS THIS COURSE **********')
                sys.exit()
                pass
            inpu=int(input('do you want to download above the files? press one for specific download 2 for complete download 0 for ternmination'))
            if(inpu==1):
                inpu=int(input('enter the serial no of the file you want to download'))
                url = lis[inpu].find('a').attrs['href']
                print(url)
                h = requests.head(url, allow_redirects=True)
                header = h.headers
                content_type = header.get('content-type')
                status=0
                if 'text' in content_type.lower():
                   status+=1

                elif ('html' in content_type.lower()):
                    pass
                if(status==0):
                    print('This is not a downloadable file')
                if(status==1):

                    r = s.get(url, allow_redirects=True)
                    # with open('file1.pptx','wb') as f:
                    #   f.write(r.content)
                    filename = getFilename_fromCd(r.headers.get('content-disposition')).strip().replace(' ','')

                    arr=filename[1:len(filename)-1]
                    type=arr.split('.')

                    name=input('enter your file name(make sure you dont have the file already it ovrerrides the prev file)')
                    file=name+'.'+type[1]


                    with open(file,'wb') as f:
                        f.write(r.content)


            if (inpu == 2):
                for inpu in range(len(lis)-1):
                    url = lis[inpu].find('a').attrs['href']

                    h = requests.head(url, allow_redirects=True)
                    header = h.headers
                    content_type = header.get('content-type')
                    status = 0
                    if 'text' in content_type.lower():
                        status += 1

                    elif ('html' in content_type.lower()):
                        pass
                    if (status == 0):
                        print(lis[inpu].find('a').text + ' not a downloadable file view the link instead')
                    if (status == 1):
                        r = s.get(url, allow_redirects=True)
                        # with open('file1.pptx','wb') as f:
                        #   f.write(r.content)
                        filename = getFilename_fromCd(r.headers.get('content-disposition')).strip().replace(' ', '')

                        arr = filename[1:len(filename) - 1]

                        with open(arr, 'wb') as f:
                            f.write(r.content)
                            print(lis[inpu].find('a').text + ' status - succesfully downloaded')
            if(inpu==0):
                break

        else:
            print('unable to fetch the result. Try to expand the name of the course like dlca-> digital logic')
