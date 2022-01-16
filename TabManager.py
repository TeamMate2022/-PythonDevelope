import os
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import time

DRIVER_PATH = os.getcwd() + r'/chromedriver.exe'
driver = Chrome(DRIVER_PATH)


# tabs database!
tabs = []

# if you want to findout tab id of specific url, you can use this method
def find_tab_id(tab_link):
    for tab in tabs:
        if tab['tab_link'] == tab_link:
            return tab['tab_id']

# open new tab and open links - save tab information to a list
def open_tabs(links):
    for link in links:
        tab_information = {}
        # first of all open a new tab
        driver.execute_script("window.open('');")
        # switch to new tab
        driver.switch_to.window(driver.window_handles[(len(driver.window_handles)-1)])
        driver.get(link)
        tab_information['tab_id'] = len(driver.window_handles) - 1
        tab_information['tab_link'] = link
        print(tab_information)
        tabs.append(tab_information)
    return tabs

# refresh specific tab
def refresh_tab(tab_id):
    driver.switch_to.window(driver.window_handles[tab_id])
    driver.refresh()
    time.sleep(2)

# switch to specific tab
def switch_to_tab(tab_id):
    driver.switch_to.window(driver.window_handles[tab_id])
    time.sleep(1)
    return True

def close_tab(tab_id):
    driver.switch_to.window(driver.window_handles[tab_id])
    time.sleep(2)
    driver.close()
    if (len(driver.window_handles)) <= 1:
        driver.switch_to.window(driver.window_handles[tab_id]-1)

# def close_tab(tab_link):
#     for tab in tabs:
#         if tab['tab_link'] == tab_link:
#             print(tab_link)
#             driver.switch_to.window(driver.window_handles[tab['tab_id']])
#             time.sleep(2)
#             driver.close()
#             if (len(driver.window_handles)) <= 1:
#                 driver.switch_to.window(driver.window_handles[tab['tab_id']]-1)    

# we will manage our tabs here
def tab_manager(links):
    tabs = []
    # open links in new tabs:
    tabs = open_tabs(links)

    time.sleep(2)

    # refresh_tabs(tabs_list)
    for tab in tabs:
        if switch_to_tab(tab['tab_id']):
            print(f"Refreshing page number {tab['tab_id']}")
            refresh_tab(tab['tab_id'])

    # print(find_tab_id[tabs[0]['tab_link']]
    close_tab(tabs[1]['tab_id'])
    # close_tab(tabs[1]["tab_link"])


links = ['https://github.com', 'https://google.com', 'https://stackoverflow.com']
# links = ['https://github.com', ]
driver.get('https://duckduckgo.com')


tab_manager(links)


