from bs4 import BeautifulSoup
import requests
import re

_ROOT_WEB_PAGE = 'https://nonnatittina.eu/'
_PIZZA = _ROOT_WEB_PAGE + 'pizze-cdn/'
_DAILY = _ROOT_WEB_PAGE + 'menu-del-giorno/'
_SALAD = _ROOT_WEB_PAGE + 'insalate-cdn/'

def retrieve_menu(course):
    if course == 'pizza':
        return scraper(_PIZZA)
    elif course == 'daily':
        return scraper(_DAILY)
    elif course == 'salad':
        return scraper(_SALAD)

def scraper(url):
    """
    This function scrapes courses data from the official website.
    """
    
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    # List with all courses requested
    courses = []

    if url == _DAILY:
        # Get courses tables
        tables = soup.find_all('table')

        # Get first course names and prices
        for row in tables[0].tbody.find_all('tr'):
            table_cell = row.find_all('td')    
            courses.append({'name': table_cell[0].text.replace(u'\n', u''), 'price': table_cell[1].text})
        
        # Get main course names and prices
        for row in tables[1].tbody.find_all('tr'):
            table_cell = row.find_all('td')
            courses.append({'name': table_cell[0].text.replace(u'\n', u''), 'price': table_cell[1].text})
    else:        
        # Get all courses names
        for course_name in soup.find_all('h3', 'p1'):
            courses.append({'name': course_name.text, 'desc': '', 'price': ''})
        
        # Get all courses descriptions
        for course_desc, course in zip(soup.find_all('h3', 'p1'), courses):
            course['desc'] = course_desc.find_next_sibling('p').text.replace(u'\xa0', u' ')
        
        # Get all courses prices
        for course_price, course in zip(soup.find_all(string=re.compile('euro')), courses):
            course['price'] = course_price

    # Return courses requested
    return courses