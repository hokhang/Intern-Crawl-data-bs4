import bs4
import requests
import pandas
### use module BeautifulSoup to data analysis HTML or XML
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

### fetch all data from website has url by method get (request.method)
respone = requests.get("https://tuoitre.vn/tin-moi-nhat.htm")

### use BeautifulSoup to separate the data into tree
soup = bs4.BeautifulSoup(respone.content, "html.parser")

### filter all tags h3 and clas "title-news"
titles = soup.findAll('h3', class_='title-news')


### get all Link in titles function 
links = [link.find('a').attrs["href"] for link in titles]
results = []
for link in titles:
    ### find only one tag a in h3 of titles, therefore i use find and attribute href
    results += [link.find('a').attrs['href']]
    # print(link.find('a').attrs['href'])


### build test
for link in results:
    news = requests.get("https://tuoitre.vn" + link)
    soup = BeautifulSoup(news.content, 'html.parser')

    title = soup.find('h1', class_='article-title')
    try:
        title = title.text
    except:
        title= 'No title'


    abstract = soup.find('h2', class_='sapo')
    print(type(abstract))
    try:
        abstract = abstract.text
    except:
        abstract = 'No abstract'


    body = soup.find('div', id = 'main-detail-body')
    content = ''
    try:
        content = body.findChildren('p', recursive = False)[0].text + body.findChildren('p', recursive = False)[1].text
    except:
        content ='No content'

    image = ''  
    try:
        image = body.find('img').attrs['src']
    except:
        image= 'No image'
    

    print("Tiêu đề: "+ title)
    print('Mô tả: '+ abstract)
    print('Nội dung: '+ content)
    print('Ảnh minh họa: '+ image)
    print(link)
    print('***********************************************************************************')

### create picture
"""img = Image.new('RGB',(650, 625), color = 'white')
font = ImageFont.load_default()
view = ImageDraw.Draw(img)
view.text((10,10), 'Hello', font=font, fill = 'black')
img.show()"""

### add character into picture
'''img = Image.new('RGB',(650,625), color='white')
font = ImageFont.truetype('font/arial.ttf', 12)

d= ImageDraw.Draw(img)

addImg = Image.open(r'anh.jpg')
img.paste(addImg,(10,10))
d.text((200,200),'AHHIHI VAN CHUA HIEEUR NHAS NEEN XEM LAIJ', font = font, fill ='white')
img.show()'''

def CrawlNewsData(baseUrl, url):
    respone = requests.get(url)
    soup = BeautifulSoup(respone.content,"lxml")
    titles = soup.findAll('h3', class_='title-news')
    links = [link.find('a').attrs['href'] for link in titles]
    data = []
    for link in links:
        news = requests.get(baseUrl + link)
        soup =  BeautifulSoup(news.content, 'lxml')
        title = soup.find('h1', class_='article-title').text
        abstract = soup.find('h2', class_='sapo').text
        body = soup.find('div', id = 'main-detail-body')
        image = body.find('img').attrs['src']
        data.append({
            'Title': title,
            'Abstract': abstract,
            'Image': image,
        })
    df = pandas.DataFrame(data)
    
    df.to_csv('collect-data.csv', header = True, index = False, encoding= 'utf-8-sig')

    dataExport = pandas.read_csv('collect-data.csv',parse_dates= False, infer_datetime_format= False)
    dataExport.shape
    (176,5)
    # print(dataExport.head())
 

# CrawlNewsData('https://tuoitre.vn','https://tuoitre.vn/tin-moi-nhat.htm')
