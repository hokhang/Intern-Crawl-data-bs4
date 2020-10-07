import requests
import pandas
import json
import re
import psycopg2
import datetime

from bs4 import BeautifulSoup

url = 'https://careerbuilder.vn/viec-lam/cntt-phan-cung-mang-cntt-phan-mem-c63,1-trang-1-vi.html'

start=datetime.datetime.now()
print(start)

respone = requests.get(url)
# respone = requests.post(request_url, data= form_data)
print(respone)
soup = BeautifulSoup(respone.content, 'html.parser')
# print(soup)
container = soup.find('div', class_ = 'col-lg-8 col-custom-xxl-9')
# print(container)
list_page = container.find('div', class_ = 'pagination')
# print(list_page)
pages = list_page.find('li', class_ = 'next-page')
get_links = [url]

# i = 0
# Find link each page
while(1):
    if(pages == None):
        break
    link = str(pages.find('a').attrs['href'])
    #Add link next page
    get_links +=[link]
    # GET request http next this page again
    respone = requests.get(link)
    soup = BeautifulSoup(respone.content, 'html.parser')
    
    container = soup.find('div', class_ = 'col-lg-8 col-custom-xxl-9')

    list_page = container.find('div', class_ = 'pagination')
    pages = list_page.find('li', class_ = 'next-page')
    # i+=1

# print(get_links)
link_jobs = []
# Process each page insert link each job
for index in range(len(get_links)):
    _url = get_links[index]
    _respone = requests.get(_url)
    _soup = BeautifulSoup(_respone.content, 'html.parser')
    _container = _soup.find('div', class_ ='col-lg-8 col-custom-xxl-9')

    main_job = _container.find('div', class_ = 'main-slide')
    list_job = main_job.findAll('div', class_ = 'job-item')
    #FInd link job in this page
    for job in list_job:
        image = job.find('div', class_ = 'title')
        link_job = image.find('a', class_ = 'job_link').attrs['href']
        link_jobs +=[link_job]

# print(link_jobs)
#Process each job
data = []
for url_job in link_jobs:
    get_respone = requests.get(url_job)
    # print(get_respone)
    # print(url_job)
    get_soup = BeautifulSoup(get_respone.content, 'html.parser')
    try:
        banner = get_soup.find('section', class_ = 'apply-now-banner')
        name_company = banner.find('a', class_ = 'job-company-name')
        get_name_company = name_company.text.strip()
        print(get_name_company)
    except:
        continue

    name_job = banner.find('p', class_='title')
    get_name_job = name_job.text.strip()
    print(get_name_job)

    tab_content = get_soup.find('section', class_ = 'job-detail-content')
    detail_rows = tab_content.findAll('div', class_ = 'detail-row')
    for detail_row in detail_rows:
        try:
            detail = detail_row.find('h3', class_ ='detail-title').text.replace(' ', '')
        except:
            continue
        # print(detail)
        if(detail == 'MôtảCôngviệc'):
            description_jobs = detail_row
            text_description = description_jobs.text.strip()
            get_description = re.sub(' +', ' ', text_description)
        if(detail == 'YêuCầuCôngViệc'):
            request_jobs = detail_row
            text_request = request_jobs.text.strip()
            get_request_job = re.sub(' +', ' ', text_request)
    try:
        job_tags = get_soup.find('div', class_ = 'job-tags')
        text_job_tags = job_tags.text
        get_job_tags = re.sub('   +', '', text_job_tags)
    except:
        get_job_tags = 'Null'

    # print(get_job_tags)
    # print(get_request_job)
    # print(get_description)

    data.append({
        'Name_company': get_name_company,
        'Name_job': get_name_job,
        'Description_job': get_description,
        'Request_job': get_request_job,
        'Job_tags_skill': get_job_tags,
    })

conn = psycopg2.connect('dbname=Detail_Data user=postgres password=khanghb')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS data_career')
cur.execute('CREATE TABLE data_career(id serial PRIMARY KEY, Name_company TEXT, Name_job TEXT, Description_job TEXT, Request_job TEXT, Job_tags_skill TEXT );')

for i in range(len(data)):
    cur.execute('INSERT INTO data_career (Name_company, Name_job, Description_job, Request_job, Job_tags_skill) VALUES(%s, %s, %s, %s, %s)', (data[i]['Name_company'], data[i]['Name_job'], data[i]['Description_job'], data[i]['Request_job'], data[i]['Job_tags_skill']))
    print(i)

conn.commit()
cur.close()
conn.close()

end=datetime.datetime.now()
print(end)
time1=end-start
print(time1)    
    
    # print(get_name_company)
    # print(get_name_job)  