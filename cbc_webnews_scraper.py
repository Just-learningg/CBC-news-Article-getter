from selenium import webdriver 
import copy
import pandas as pd
from datetime import datetime
import os
import sys
import time

#get url
news_url = 'https://www.cbc.ca'

#get time
exe_time = datetime.now()
date = exe_time.strftime("%d%m%Y")
c_time = exe_time.strftime("%H%M%S")
print(date,c_time)

#get exe path
app_path = os.path.dirname(sys.executable)
#if running just the application please change app_path to this - 
#app_path = os.path.dirname(os.path.abspath(__file__))


#define the drivers and open the link and pass in option
driver = webdriver.Chrome()
driver.set_page_load_timeout(20)
driver.get(news_url)


#get all available articles

containers = driver.find_elements(by ='xpath', value = '//a[contains(@class,"cardWrapper")]')

#create a link and a title list 
links = []
titles = []

#iterate thru each container and store their link and title
for container in containers:
    link = container.get_attribute('href')
    links.append(link)
    # print(link)
    title = container.find_element(by = 'xpath', value = './/span[contains(@class,"title")]').text
    titles.append(title)
    # print(title)

#visit each link and get all the article contents(texts)
#iterate thru each the links in the link

print("Total Articles Found: ",len(titles))

#one list for each article and one list for all articles
article = []
all_articles = []
#iterate thru each link
for i in links:
    print("For ",i)
    
    #we handle exceptions if the page takes too long to respond - this was later solved by putting time.sleep(2) in line 75
    try:
        driver.get(i)
    except Exception as e:
        print(f"Unexcepted Error! Skipping: {i}", type(e))
        try:
            driver.execute_script("window.stop();")
        except Exception:
            pass
        #pass in an empty list for alignment
        all_articles.append([])
        continue

    
    time.sleep(2)
    all_lines = driver.find_elements(by = 'xpath', value = '//div[contains(@class,"story")]//p')
    num_lines = len(all_lines)
    print("Total lines found: ",num_lines)

    #get the text from each line and save them in a list
    line = 1
    for each_line in all_lines:
        article.append(each_line.text)
        print("copied line ",line)
        line+=1
    #save the whole article in a list deepcopy to make sure it doesn't get saved by reference
    all_articles.append(copy.deepcopy(article))
    #clear the article list so we can save the next article
    article.clear()
    print("\n")
    

#for testing
#print(len(all_articles))
#print(all_articles[0][1])
#print(all_articles[-1][1])

full_article = {'Titles':titles,'Links':links, 'Articles':all_articles}
df_headlines = pd.DataFrame(full_article)
csv_file_name = f'cbc_articles_date_{date}_time_{c_time}.csv'
file_dest =os.path.join(app_path,csv_file_name)

df_headlines.to_csv(file_dest)
print("Saved File to", file_dest)

driver.quit()
#//a[@class="cardWrapper-u5T0r"]//span[contains(@class,"title")]
