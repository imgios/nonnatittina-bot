from bs4 import BeautifulSoup
import requests
import re

_ROOT_WEB_PAGE = 'https://nonnatittina.eu/'
_PIZZA = _ROOT_WEB_PAGE + 'pizze-cdn/'
_DAILY = _ROOT_WEB_PAGE + 'menu-del-giorno/'
_SALAD = _ROOT_WEB_PAGE + 'insalate-cdn/'

def retrieve_menu(course):
    if course == 'pizza':
        # scrape pizza menu
        return scraper(_PIZZA)
    elif course == 'daily':
        # scrape daily menu
        return 0
    elif course == 'salad':
        return scraper(_SALAD)

def scraper(url):
    """
    This function scrapes pizzas and salads data from the official website.
    """
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    
    # List with all courses requested
    courses = []
    
    # Get all courses names
    for course_name in soup.find_all('h3', 'p1'):
        courses.append({'name': course_name.text, 'desc': '', 'price': ''})
    
    # Get all courses descriptions
    i = 0
    for course_desc in soup.find_all('p', 'p2'):
        courses[i]['desc'] = course_desc.text
        i += 1
    
    # Get all courses prices
    # !! Now it retrieves all prices but keeps putting someone out of range causing a crash
    k = 0
    for course_price in soup.find_all(string=re.compile('euro')):
        print("{} - {} - {}".format(k, len(courses), course_price))
        courses[k]['price'] = course_price.text
        k += 1 

    # Return courses requested
    return courses

if __name__ == '__main__':
    retrieve_menu('pizza')