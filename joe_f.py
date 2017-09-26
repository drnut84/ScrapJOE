# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 22:11:19 2017

@author: sang
"""
def post_f(posting,p_num,Nop):
    inst_title=posting.find('h5', {'class':"group-header-title"}).text.strip()
    Devision  =posting.find('h6', {'class':"group-sub-header-title"})
    positions =posting.find_all('h6' , {'class':"listing-item-header-title"})
    pos_f     =posting.find_all('div', {'class':"listing-item-body"})
    if Nop != len(positions):
        print('Nop Error',inst_title)
        
    if Nop != len(pos_f):
        print('Nop Error',inst_title)
        
    for oop in list(range(0,Nop)):
        #Institution Name
        joe_sheet.update_cell   (p_num+oop+3,1,inst_title)
        joeExt_sheet.update_cell(p_num+oop+3,1,inst_title)
        
        #Devision/Department
        if not Devision:
            joe_sheet.update_cell(p_num+oop+3,6,' ')
        else:
            joe_sheet.update_cell(p_num+oop+3,6,Devision.text.strip())
    
        #JobTitle
        pp=positions[oop]
        job_title=pp.find_all('a')
        if len(job_title) != 1:
            print('Jobtitle Error',inst_title)
            break
        
        joe_url  ='https://www.aeaweb.org/'+job_title[0]['href']
        joe_sheet.update_cell   (p_num+oop+3,2,'=HYPERLINK("'+joe_url  +'","'+job_title[0].text.strip()+'")')
        joeExt_sheet.update_cell(p_num+oop+3,2,job_title[0].text.strip())

        deadline=pos_f[oop].find('p', {'class':"app-instruct-deadline"})
        if not deadline:
            joe_sheet.update_cell(p_num+oop+3,5,' ')
        else:
            joe_sheet.update_cell(p_num+oop+3,5,deadline.text.split(':')[1].strip())
        
        app=pos_f[oop].find_all('a', {'class':"app-instruct-button button"})
        if not app:
            joe_sheet.update_cell(p_num+3,3,'No Link')
        else:
            for in_app in app:
                if 'Apply' in in_app.text:
                    apply_url=in_app['href']
                    if apply_url =="javascript:applcntCand.cantApplyModal();":
                        joe_sheet.update_cell(p_num+oop+3,3,'Link Broken at JOE')
                    elif not apply_url:
                        joe_sheet.update_cell(p_num+oop+3,3,'Link Broken at JOE')
                    else:
                        joe_sheet.update_cell(p_num+oop+3,3,'=HYPERLINK("'+apply_url+'","Application Link")')
                elif 'Reference' in in_app.text:
                    rec_url=in_app['href']
                    if rec_url =="javascript:applcntCand.cantApplyModal();":
                        joe_sheet.update_cell(p_num+oop+3,4,'Link Broken at JOE')
                    elif not rec_url:
                        joe_sheet.update_cell(p_num+oop+3,4,'Link Broken at JOE')
                    else:
                        joe_sheet.update_cell(p_num+oop+3,4,'=HYPERLINK("'+rec_url+'","Reference Link")')
                else:
                    print('Extra Link')

        post = requests.get(joe_url)
        post = BeautifulSoup(post.content,"lxml")
        
        temp_post=post.find_all('div',{'class':"listing_section" })
        #JOE ID
        
        Base=temp_post[0].find_all('div')
        for bb in Base:
            if 'Number' in bb.text:
                JOE_num=bb.text.split(':')[1].strip()
                joe_sheet.update_cell(p_num+oop+3,7,JOE_num)
            elif 'Posted' in bb.text:
                joe_sheet.update_cell(p_num+oop+3,8,bb.text.split(':')[1].strip())
        
        #Description
        des=temp_post[1].find_all('span')
        JEL=''
        Key=''
        for ds in des:
            ds_text=ds.text
            
            if 'Section' in ds_text:
                joe_sheet.update_cell(p_num+oop+3,9 ,ds.next_sibling.strip())
            elif 'Location' in ds_text:
                joe_sheet.update_cell(p_num+oop+3,10,ds.next_sibling.strip())
            elif 'JEL' in ds_text:
                temp_JEL=ds.next_sibling
                for lot in list(range(10)):
                    if not temp_JEL:
                        if JEL=='':
                            print('No JEl',JOE_num)
                    else:
                        if temp_JEL.name=='span':
                            break
                        
                        elif temp_JEL.name=='br':
                            if temp_JEL.text=='':
                                temp_JEL=temp_JEL.next_sibling
                            else:
                                if JEL !='':
                                    JEL=JEL+', '+temp_JEL.text.strip()
                                else: 
                                    JEL=temp_JEL.text
                                temp_JEL=temp_JEL.next_sibling
                        elif not temp_JEL.name:
                            if temp_JEL=='':
                                temp_JEL=temp_JEL.next_sibling
                            else:
                                if JEL !='':
                                    JEL=JEL+', '+temp_JEL.strip()
                                else: 
                                    JEL=temp_JEL
                                temp_JEL=temp_JEL.next_sibling
                JEL=JEL.replace('\n', ', ')
                JEL=JEL.replace('\r', ', ')
                JEL=JEL.replace(', ,', ',')
                joe_sheet.update_cell(p_num+oop+3,11,JEL)
                
            elif 'Keywords' in ds_text:
                temp_Key=ds.next_sibling
                for lot in list(range(10)):
                    if not temp_Key:
                        break
                    elif temp_Key !='':
                        if not temp_Key.name:
                            if temp_Key=='':
                                temp_Key=temp_Key.next_sibling
                            else:
                                if Key !='':
                                    Key=Key+', '+temp_Key.strip()
                                else: 
                                    Key=temp_Key
                                temp_Key=temp_Key.next_sibling
           
                        elif temp_Key.name=='br':
                            if temp_Key.text=='':
                                temp_Key=temp_Key.next_sibling
                            else:
                                if Key !='':
                                    Key=Key+', '+temp_Key.text.strip()
                                else: 
                                    Key=temp_Key.text
                                temp_Key=temp_Key.next_sibling
                        elif temp_Key.name=='div':
                            if temp_Key.text=='':
                                temp_Key=temp_Key.next_sibling
                            else:
                                if Key !='':
                                    Key=Key+', '+temp_Key.text.strip()
                                else: 
                                    Key=temp_Key.text
                                temp_Key=temp_Key.next_sibling
                        elif temp_Key.name=='span':
                            break
                        
                Key=Key.replace('\n', ', ')
                Key=Key.replace('\r', ', ')
                Key=Key.replace(', ,', ',')
                joe_sheet.update_cell(p_num+oop+3,12,Key)
                
            elif 'Salary' in ds_text:
                joe_sheet.update_cell(p_num+oop+3,13,ds.next_sibling.strip())
            else:            
                if 'Title' not in ds_text:
                    print('Mis Des',JOE_num)
    
        joe_sheet.update_cell(p_num+oop+3,14,'=HYPERLINK("#gid=344395365&Range=C'+str(p_num+oop+3)+'","JOE_Extra!C'+str(p_num+oop+3)+'")')
        joeExt_sheet.update_cell(p_num+oop+3,3,post.find_all('p')[0].text)
        
        #Requirement
        joe_sheet.update_cell(p_num+oop+3,15,'=HYPERLINK("#gid=344395365&Range=D'+str(p_num+oop+3)+'","JOE_Extra!D'+str(p_num+oop+3)+'")')
        req=post.find('div',{'class':"listing_section last" })
        joeExt_sheet.update_cell(p_num+oop+3,4,req.text)
 


from selenium import webdriver 
from selenium.webdriver.support.ui import Select
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import requests
import time

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('D:\Python\jobposting.json', scope)
client = gspread.authorize(creds)
sheet = client.open("JobPosting")
joe_sheet   =sheet.worksheet("JOE")
joeExt_sheet=sheet.worksheet("JOE_Extra")
date_sheet  =sheet.worksheet("Posted Date")

joe_sheet.update_cell(1,2,'Updating')


driver = webdriver.Chrome('D:\chromedriver\chromedriver')
driver.implicitly_wait(3)

driver.get('https://www.aeaweb.org/joe/listings?issue=2017-02')

select = Select(driver.find_element_by_xpath('//*[@id="ListingsForm"]/div[4]/div[2]/div/label/select'))
select.select_by_visible_text("Older Postings")
select = Select(driver.find_element_by_xpath('//*[@id="ListingsForm"]/div[4]/div[3]/div/label/select'))
select.select_by_visible_text("All")
time.sleep(10)

ss=BeautifulSoup(driver.page_source, 'html.parser')

Fday    =ss.find('h5', {'class':"date-group-header-title spacer"}).text.split(':')[1].strip()
day_list=ss.find_all('h5', {'class':"date-group-header-title "})
day_list=[dl.text.split(':')[1].strip() for dl in day_list ]

day_post=ss.find_all('div', {'class':"listing-date-group-item"})

date_sheet.update_cell(2,1,'Posted_Date')
date_sheet.update_cell(2,2,'Num_Institute')
date_sheet.update_cell(2,3,'Num_Post')

Ndays =len(day_post)
Npost=357
for Nday in list(range(37,Ndays+1)):
    dp=day_post[Nday-1]
    AggNop=0
    
    if Nday==1:
        date_sheet.update_cell(Nday+2,1,Fday)
    else:
        date_sheet.update_cell(Nday+2,1,day_list[Nday-2])
        
    oneday_post =dp.find_all('div', {'class':"date-group-institution-group "})
    Noneday_post=len(oneday_post)+1
    
    if not oneday_post:
        date_sheet.update_cell(Nday+2,2,Noneday_post)
        print('One posting')
    else:
        for nn in list(range(0,Noneday_post-1)):
            op =oneday_post[nn]
            date_sheet.update_cell(Nday+2,2,Noneday_post)
            Nop=len(op.find_all('div', {'class':"show-hide-body-button"}))
            post_f(op,Npost,Nop)
            Npost =Npost+Nop
            AggNop=AggNop+Nop
    last_post =dp.find('div', {'class':"date-group-institution-group last-group"})
    Nop=len(last_post.find_all('div', {'class':"show-hide-body-button"}))
    post_f(last_post,Npost,Nop)
    Npost =Npost+Nop
    AggNop=AggNop+Nop
    date_sheet.update_cell(Nday+2,3,AggNop)

joe_sheet.update_cell(1,2,time.strftime("%Y/%m/%d"))
