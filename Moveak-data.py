import requests
import pandas
import psycopg2

from bs4 import BeautifulSoup

url = 'https://moveek.com'
# Get all data on Movee website


respone = requests.get(url)

soup = BeautifulSoup(respone.content, 'html.parser')
titles = soup.findAll('h3', class_='text-truncate h4 mb-1')

# for title in titles:
#     print(title)
#     print('*************************************************************')

# Get detailed movie site http link
links = [link.find('a').attrs['href'] for link in titles]
#print(links)

info_joiner = []
data = []
# For every movie
for link in links:
    _respone = requests.get(url + link)
    _soup = BeautifulSoup(_respone.content, 'html.parser')
    find_title = _soup.find('h1', class_ = 'mb-0 text-truncate')
    # print( find_title)

    #Find title of movie
    get_title = find_title.find('a').attrs['title']

    #Find moive genre
    genre = _soup.find('p', class_='mb-0 text-muted text-truncate')
    get_genre = ' '.join(genre.text.split())
    
    # See discription of movie
    description = _soup.find('p', class_='mb-3 text-justify')
    get_description = description.text

    join_movie = _soup.find('div', class_ = 'col-12 col-lg-5')
    list_joiner = join_movie.findAll('p', class_='mb-2')
    get_cast = ' '
    get_director = ' '
    get_producer = ' '
    for element in list_joiner:

        find = element.find('strong').text.replace(' ','')
        try:
            if(find == 'Diễnviên'):
                casts = element.findAll('a', class_='text-danger')
                get_cast = [cast.text for cast in casts]
        except:
            get_cast = ' '

        try:
            if(find == 'Đạodiễn'):
                directors = element.findAll('a', class_='text-danger')
                get_director = [director.text for director in directors]
        except:
            get_director = ' '
        
        try:
            if(find == 'Nhàsảnxuất'):
                producers = element.findAll('a', class_='text-danger')
                get_producer = [producer.text for producer in producers]
        except:
            get_producer = ' '
    
    # print('*',get_cast)  
    # print('**',get_director)
    # print('***',get_producer)

    

    # Get information about level satisfy
    info_movies = _soup.find('div', class_ = 'row mb-3')
    info_movie = info_movies.findAll('div', class_ = 'col text-center text-sm-left')
    get_satify = ' '
    get_publish = ' '
    get_time = ' '
    get_limit_age = ' '
    # print(info_movie)
    for info in info_movie:
        # Get string to test follow function
        find= info.find('span', class_ = 'd-none d-sm-inline-block').text
        # print(find)
        #Get Satify
        try:
            if(find == 'Hài lòng'):
                satify = info.find('a', class_ = 'text-white')
                get_satify = ' '.join(satify.text.split())
        except:
            get_satify = ' '

        #Get publish
        try:
            if(find == 'Khởi chiếu'):
                publish = info.findAll('span')
                #print(publish)
                get_publish = publish[1].text
        except: 
            get_publish = ' '
        
        # Get Time
        try:
            if(find == 'Thời lượng'):
                time = info.findAll('span')
                get_time = time[1].text
        except:
            get_time = ' '

        # Get Limit age
        try:
            if(find == 'Giới hạn tuổi'):
                limit_age = info.findAll('span')
                get_limit_age = limit_age[1].text
        except:
            get_limit_age = ' '

    # print('*',get_satify)
    # print('**',get_publish)
    # print('***',get_time)
    # print('****',get_limit_age)

    data.append({
        'Title': get_title,
        'Genre': get_genre,
        'Discription': get_description,
        'Cast': get_cast,
        'Director': get_director,
        'Producer': get_producer,
        'Satify':get_satify,
        'Publish': get_publish,
        'Time': get_time,
        'Limit Age': get_limit_age
    })

# table = pandas.DataFrame(data)
# table.to_csv('collect-data-moveak.csv', header = True, index = False, encoding= 'utf-8-sig')
    # Get published movie

conn = psycopg2.connect('dbname=Project user=postgres password=khanghb')
cur = conn.cursor()
cur.execute('CREATE TABLE data(id serial PRIMARY KEY, Title varchar(100), Genre varchar(100), Description varchar(1000));')
cur.execute('INSERT INTO data (Title, Genre, Description) VALUES(%s, %s, %s)', (get_title, get_genre, get_description) )
conn.commit()
cur.close()
conn.close()


  
    









    
