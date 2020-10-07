import requests
import pandas
import json
import re
import psycopg2
import datetime

from bs4 import BeautifulSoup

# url of home page
url = 'https://www.vietnamworks.com'
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
})

start=datetime.datetime.now()
print(start)
##################
# Get request html of home page
respone_big = requests.get(url)
soup_big = BeautifulSoup(respone_big.content, 'html.parser')


# Find menue in home page
titles = soup_big.find('div', class_ = 'sc-fznzOf jxQFAb menu-homepage')
# Find all list menue in home page
find_title = titles.findAll('a', class_ = 'sc-fzoant hXtGXC')

# Get only viec lam page
for title in find_title:
    find_  = title.text.replace(' ', '')
    try:
        if(find_ == 'Việclàm'):
            get_url = title.attrs['href']
    except:
        continue


# Get request html viec lam page
respone_select = requests.get(get_url)
soup_select = BeautifulSoup(respone_select.content, 'html.parser')
titles_select = soup_select.find('div', class_ = 'main-content')
# Find list option job style
find_selects = titles_select.find('div', class_ = 'select-options')


# Get list option job style
find_select = find_selects.findAll('div', class_ ='item-text')
# print(find_select)
#array to append form data and name job
form_data = []
get_job = []
# Get JOB Internet/Online Media, JOB IT - Phần mềm and JOB IT-Phần cứng/Mạng
for element in find_select:
    get_text = element.text.replace(' ','')

    # Check Internet job
    if(get_text == 'Internet/OnlineMedia'):
        form_data += ['{"requests":[{"indexName":"vnw_job_v2_57","params":"query=&hitsPerPage=200&attributesToRetrieve=%5B%22*%22%2C%22-jobRequirement%22%2C%22-jobDescription%22%5D&attributesToHighlight=%5B%5D&query=&facetFilters=%5B%5B%22categoryIds%3A57%22%5D%2C%5B%22locationIds%3A29%22%5D%5D&filters=&numericFilters=%5B%5D&page=0&restrictSearchableAttributes=%5B%22jobTitle%22%2C%22skills%22%2C%22company%22%5D"}]}']
        get_job += ['JOB Internet/Online Media']

    # Check IT- Phan mem job
    if(get_text == 'IT-Phầnmềm'):
        form_data += ['{"requests":[{"indexName":"vnw_job_v2_35","params":"query=&hitsPerPage=200&attributesToRetrieve=%5B%22*%22%2C%22-jobRequirement%22%2C%22-jobDescription%22%5D&attributesToHighlight=%5B%5D&query=&facetFilters=%5B%5B%22categoryIds%3A35%22%5D%2C%5B%22locationIds%3A29%22%5D%5D&filters=&numericFilters=%5B%5D&page=0&restrictSearchableAttributes=%5B%22jobTitle%22%2C%22skills%22%2C%22company%22%5D"}]}']
        get_job += ['JOB IT - Phần mềm']

    # Check IT- phan cung Mang job
    if(get_text == 'IT-Phầncứng/Mạng'):
        form_data += ['{"requests":[{"indexName":"vnw_job_v2_55","params":"query=&hitsPerPage=200&attributesToRetrieve=%5B%22*%22%2C%22-jobRequirement%22%2C%22-jobDescription%22%5D&attributesToHighlight=%5B%5D&query=&facetFilters=%5B%5B%22categoryIds%3A55%22%5D%2C%5B%22locationIds%3A29%22%5D%5D&filters=&numericFilters=%5B%5D&page=0&restrictSearchableAttributes=%5B%22jobTitle%22%2C%22skills%22%2C%22company%22%5D"}]}']
        get_job += ['JOB IT-Phần cứng/Mạng']
requests_url = 'https://jf8q26wwud-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser&x-algolia-application-id=JF8Q26WWUD&x-algolia-api-key=2bc790c0d4f44db9ab6267a597d17f1a'

# Create data array to add attribute we get
data = []
# For each option job stype
for k in range(len(form_data)):
    i = 0
    respone = requests.post(requests_url, data= form_data[k])
    # print(respone)
    soup = BeautifulSoup(respone.content, 'html.parser').text
    
    # print(soup)
    json_ = (json.loads(soup))
    length_list = len(json_['results'][0]['hits'])
    print(length_list)
    # print(json_['results'][0]['hits'][0]['jobId'])
    idJob = []
    alias = []

    # Get JobId and alias in Json file to combine them create link child page
    for index in range(length_list):
        idJob += [json_['results'][0]['hits'][index]['jobId']]
        alias += [json_['results'][0]['hits'][index]['alias']]
    # print(idJob)
    # print(alias)

    # 'https://www.vietnamworks.com/ + str(alias) "-" + str(jobid) + "-jv" '

    links = []
    url_ = 'https://www.vietnamworks.com/'
    # Get Link child page to access it
    for index in range(length_list):
        links += [url_ + str(alias[index]) +'-' + str(idJob[index]) + '-jv']
    # print(links)
    
    # Access each child page
    for link in links:
        # print(link)
        _respone = requests.get(link)
        _soup = BeautifulSoup(_respone.content, 'html.parser')
        try:
            name_company = _soup.find('div', class_= 'col-sm-12 company-name')
            get_name_company = ' '.join(name_company.text.split())
            # print(get_name_company)
        except:
            continue

        find_title = _soup.find('h1', class_='job-title')
        get_title = find_title.text
        # print(find_title)
        
        description = _soup.find('div', class_ = 'description')
        text_description = description.text.strip()
        get_description = re.sub(' +', ' ', text_description)
        # print(get_description)

        job_requirement = _soup.find('div', class_ = 'requirements')
        text_job_requirement = job_requirement.text.strip() 
        get_job_requirement  = re.sub(' +', ' ', text_job_requirement)
        # print(get_job_requirement)
        # print('*************************************************')

        summarys = _soup.find('div', class_  ='box-summary link-list')
        list_summary = summarys.findAll('div', class_ = 'col-xs-10 summary-content')
        # print(list_summary)
        for summary in list_summary:
            find  = summary.find('span', class_ = 'content-label').text.replace(' ', '')
            try:
                if(find == 'KỹNăng'):
                    skill = summary.find('span', class_ = 'content')
                    get_skill = skill.text.strip()
            except:
                continue
        # print(get_skill)

        data.append({
            'Job_Type': get_job[k],
            'Company': get_name_company,
            'Label': get_title,
            'Job_Description': get_description,
            'Job_Requirement': get_job_requirement,
            'Job_Skill': get_skill,
        })

        
        i+=1
        print(i)
        
conn = psycopg2.connect('dbname=Detail_Data user=postgres password=khanghb')


cur = conn.cursor()


cur.execute('DROP TABLE IF EXISTS data_vietnamworks')
cur.execute('CREATE TABLE data_vietnamworks(id serial PRIMARY KEY, Job_Type TEXT, Company TEXT, Label TEXT, Job_Description TEXT, Job_Requirement TEXT, Job_Skill TEXT );')

for i in range(len(data)):
    cur.execute('INSERT INTO data (Job_Type, Company, Label, Job_Description, Job_Requirement, Job_Skill) VALUES(%s, %s, %s, %s, %s, %s)', (data[i]['Job_Type'], data[i]['Company'], data[i]['Label'], data[i]['Job_Description'], data[i]['Job_Requirement'], data[i]['Job_Skill']))
    print(i)
    
conn.commit()
cur.close()
conn.close()

end=datetime.datetime.now()
print(end)
time1=end-start
print(time1)


# titles = soup.find(attrs={'class': 'block-job-list'})
# print(titles)
# soup = BeautifulSoup(respone.content, 'html.parser')
# # print(soup)
# titles = soup.find('div', class_ = 'block-job-list')
# print(titles)
# get_links = titles.findAll('div', class_ = 'col-12 col-lg-8 col-xl-8 p-0 wrap-new')
# print(get_links)
# links = [link.find('a').attrs['href'] for link in get_links ]
# print(links)
    