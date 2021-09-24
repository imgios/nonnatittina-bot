# Imports

ROOT_WEB_PAGE = 'https://nonnatittina.eu/'
PIZZA = ROOT_WEB_PAGE + 'pizze-cdn/'
DAILY = ROOT_WEB_PAGE + 'menu-del-giorno/'
INSALATE = ROOT_WEB_PAGE + 'insalate-cdn/'

def retrieve_menu(course):
    if course == 'pizza':
        # scrape pizza menu
        return 0
    elif course == 'daily':
        # scrape daily menu
        return 0
    elif course == 'salad':
        # scrape salads menu
        return 0