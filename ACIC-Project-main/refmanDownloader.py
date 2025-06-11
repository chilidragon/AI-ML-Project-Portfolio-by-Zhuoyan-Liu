from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import sys
import time

# set default download location, suppress error messages, set incognito mode
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : r"C:\Users\wande\Downloads\Test\\"}
chromeOptions.add_experimental_option("prefs",prefs)
chromeOptions.add_argument('log-level=3')
chromeOptions.add_argument("--incognito")
chromedriver = Service("chromedriver.exe")

# function to convert a list into string
def convert(s):
    str1 = ""
    return(str1.join(s))
		
# Assign the arguments passed to a variable search_string
search_string = sys.argv[1:]

# The argument passed to the program is accepted
# as list, it is needed to convert that into string
search_string = convert(search_string)

# This is done to structure the string
# into search url.(This can be ignored)
search_string = search_string.replace(' ', '+')


# Assigning the browser variable with chromedriver of Chrome.
# Any other browser and its respective webdriver
# like geckodriver for Mozilla Firefox can be used
browser = webdriver.Chrome(service=chromedriver, options=chromeOptions)

# keywords list
keywordsList = ["\"emergency+response\""] #, "digital+democracy"


# save links to a dictionary with refman filename as keyword and link as value
links = {}


# loop through all keywords
for index, keyword in enumerate(keywordsList):
    matched_elements = browser.get("https://scholar.google.com/scholar?as_vis=1&q=" + keyword + "&hl=en&as_sdt=0,48&as_ylo=2022") # search google scholar for keyword
    if index == 0: # if first term, allow time to fill out captcha and maximize window
        browser.maximize_window()
        time.sleep(15)
    else:
        time.sleep(2)
    
    # loop through two pages of search results
    for i in range(1):
        citeButtons = browser.find_elements(By.CSS_SELECTOR, "a.gs_or_cit.gs_or_btn.gs_nph")
        for index2, x in enumerate(citeButtons): # loop through all cite buttons
            button = x
            button.click()
            time.sleep(1)
            button = browser.find_element(By.CSS_SELECTOR, "#gs_citi > a:nth-child(3)") # download refman
            button.click()
            time.sleep(1)
            button = browser.find_element(By.CSS_SELECTOR, "#gs_cit-x") # close modal
            button.click()
            time.sleep(1)
            selector = "#gs_res_ccl_mid > div:nth-child(" + str(index2 + 1) + ") > div.gs_ggs.gs_fl > div > div > a > span"
            # check if direct source link and exists and if it is a PDF
            if len(browser.find_elements(By.CSS_SELECTOR, selector)) != 0 and browser.find_element(By.CSS_SELECTOR, selector).get_attribute("innerHTML") == "[PDF]":
                selector2 = "#gs_res_ccl_mid > div:nth-child(" + str(index2 + 1) + ") > div.gs_ggs.gs_fl > div > div > a"
                link = browser.find_element(By.CSS_SELECTOR, selector2).get_attribute("href") # get link to source
                # print(link)
            # elif len(browser.find_elements(By.XPATH, "/html/body/div/div[10]/div[2]/div[3]/div[2]/div[" + str(index2 + 1) + "]/div[2]/h3/a")) != 0: # else get link to publication website
                # selector2 = "#gs_res_ccl_mid > div:nth-child(" + str(index2 + 1) + "> div.gs_ri > h3 > a"
                # selector2 = "/html/body/div/div[10]/div[2]/div[3]/div[2]/div[" + str(index2 + 1) + "]/div[2]/h3/a"
                # link = browser.find_element(By.XPATH, selector2).get_attribute("href")
                # print(link)
            # elif len(browser.find_elements(By.XPATH, "/html/body/div/div[10]/div[2]/div[3]/div[2]/div[" + str(index2 + 1) + "]/div/h3/a")) != 0:
                # selector2 = "/html/body/div/div[10]/div[2]/div[3]/div[2]/div[" + str(index2 + 1) + "]/div/h3/a"
                # link = browser.find_element(By.XPATH, selector2).get_attribute("href")
                # print(link)
            # elif len(browser.find_elements(By.XPATH, "/html/body/div/div[10]/div[2]/div[3]/div[" + str(index2 + 1) + "]/div[2]/div/h3/a")) != 0:
                # selector2 = "/html/body/div/div[10]/div[2]/div[3]/div[" + str(index2 + 1) + "]/div[2]/div/h3/a"
                # link = browser.find_element(By.XPATH, selector2).get_attribute("href")
                # print(link)
            # else:
                # link = "missing source URL"
                # print("no source URL found")
            else: 
                link = "missing pdf link"

            if index2 == 0:
                links['scholar'] = link
            else:
                links['scholar (' + str(index2) + ')'] = link
                
        # advance to next page of search results
        nextButton = browser.find_element(By.CSS_SELECTOR, "#gs_n > center > table > tbody > tr > td:nth-child(12) > a")
        nextButton.click()
        time.sleep(2)

print(links)

# for i in range(1):
#     matched_elements = browser.get("https://scholar.google.com/scholar?as_ylo=2022&q=" + search_string + "&hl=en&as_sdt=0,48")
#     browser.maximize_window()
#     time.sleep(10)

# py -3 -m venv .venv
# .venv\scripts\activate




# get searched term in google scholar and maximize window
# allow time to fill out captcha
# for index, keyword in enumerate(keywordsList):
#     matched_elements = browser.get("https://scholar.google.com/scholar?as_ylo=2022&q=" + keyword + "&hl=en&as_sdt=0,48")
#     browser.maximize_window()
#     if index == 0:
#       time.sleep(10)
    
#     # get all cite buttons, download all refmans, repeat for multiple pages
#     for i in range(2):
#       citeButtons = browser.find_elements_by_css_selector("a.gs_or_cit.gs_or_btn.gs_nph")
#       for x in citeButtons:
#           button = x
#           button.click()
#           time.sleep(1)
#           button = browser.find_element_by_css_selector("#gs_citi > a:nth-child(3)")
#           button.click()
#           time.sleep(1)
#           button = browser.find_element_by_css_selector("#gs_cit-x")
#           button.click()
#           time.sleep(1)

#       nextButton = browser.find_element_by_css_selector("#gs_n > center > table > tbody > tr > td:nth-child(12) > a")
#       nextButton.click()
#       time.sleep(3)

# print PDF links for any source that has one
# for index, keyword in enumerate(keywordsList):
#     matched_elements = browser.get("https://scholar.google.com/scholar?as_ylo=2022&q=" + keyword + "&hl=en&as_sdt=0,48")
#     browser.maximize_window()
#     if index == 0:
#         time.sleep(15)
#     for i in range(2):
#         sourceResults = browser.find_elements_by_css_selector(".gs_r.gs_or.gs_scl")
#         for i in range(1, len(sourceResults) + 1):
#             selector = "#gs_res_ccl_mid > div:nth-child(" + str(i) + ") > div.gs_ggs.gs_fl > div > div > a > span"
#             if len(browser.find_elements_by_css_selector(selector)) != 0:
#                 if browser.find_element_by_css_selector(selector).get_attribute("innerHTML") == "[PDF]":
#                     selector2 = "#gs_res_ccl_mid > div:nth-child(" + str(i) + ") > div.gs_ggs.gs_fl > div > div > a"
#                     link = browser.find_element_by_css_selector(selector2).get_attribute("href")
#                     print(link)
#         nextButton = browser.find_element_by_css_selector("#gs_n > center > table > tbody > tr > td:nth-child(12) > a")
#         nextButton.click()
#         time.sleep(3)