# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 16:08:16 2022

@author: Mahya
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
from datetime import date


driver = webdriver.Chrome('chromedriver.exe')
url = 'https://indeed.com/'
# url = 'https://www.indeed.com/jobs?q=data%20science%20intern&l=remote&from=searchOnHP&vjk=1aaf9713fcbd398a'
driver.get(url)
source = driver.page_source

# %% input job title and location

job_title = 'Data Science intern'
location = 'remote'

what_search_box = driver.find_element_by_id('text-input-what')
what_search_box.send_keys(job_title)
what_search_box.send_keys(Keys.ENTER)

where_search_box = driver.find_element_by_id("text-input-where")
where_search_box.send_keys(location)
where_search_box.send_keys(Keys.ENTER)

driver.implicitly_wait(30)
Data Science intern
# %% find the number of result pages

page = driver.find_element_by_class_name('pagination')
page_num = re.findall('\d',str(page.text))
page_num = [int(i) for i in page_num]
print(f'total number of pages to scrape:{len(page_num)}')

# %% scrape the web pages

titles = []
companies = []
conditions = [] 
salary = []

for n in page_num[:-1]:
    results = driver.find_elements_by_class_name('resultContent')
    cols = ['title','company','location','condition','salary']
    
    for i, r in enumerate(results):
        
        try:
            titles.append(r.find_element_by_class_name('jcs-JobTitle').text)
        except:
            titles.append('None')
        
        try:
            companies.append(r.find_element_by_class_name('companyName').text)            
        except:
            companies.append('None')
    
        try:
            conditions.append(r.find_element_by_class_name('attribute_snippet').text)
        except:
            conditions.append('None')
       
        try:
            salary.append(r.find_element_by_class_name('estimated-salary').text) 
        except:
            salary.append('None')
        
    # going to the next page
    try:
        next_page = driver.find_element_by_xpath('//a[@aria-label="Next"]//span[@class="np"]')
        print(f'using next button,in page {n}')
        
        try:
            next_page.click()
        except:
            # for closig the pop up note on the page
            close_button = driver.find_element_by_class_name('popover-x-button-close icl-CloseButton')
            close_button.click()
            next_page.click()
            
    except:
        print(f'there is problem loading next page, current page number: {n}')
        # raise
    

    
    print(f"going to the next Page: page{n+1}")

print('end of web scraping')       
# %% quit

driver.quite()

# %% creating dataframe and saving to csv

cols = ['title','company', 'condition', 'salary']
df = pd.DataFrame(list(zip(titles,companies,conditions,salary)),columns=cols)


# %% save the data frame to a csv file

today = date.today()
# mm/dd/y
d1 = today.strftime("%m/%d/%y")
# YYYY-mm-dd
d2 = today.strftime('%Y-%m-%d')

name_csv = f'indeed-ds-remote- {d2}.csv'
df.to_csv(name_csv, index=False)