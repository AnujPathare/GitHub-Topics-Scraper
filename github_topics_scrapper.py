# TOP REPOSITORIES FOR GITHUB TOPICS
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import os
# import requests



#-------- Getting Information Of All Popular Topics On Github --------#



def get_topic_title(soup):
    topic_titles_tags = soup.find_all("p", class_ = "f3 lh-condensed mb-0 mt-1 Link--primary")
    topic_titles = []
    for title in topic_titles_tags: # Get topic title of the corresponding repository
        topic_titles.append(title.text.strip())
    return topic_titles

# df_topic_titles = pd.DataFrame(topic_titles, columns =['Topic'])


def get_topic_descriptions(soup):

    topic_descriptions_tags = soup.find_all("p", class_ = "f5 color-fg-muted mb-0 mt-1")
    topic_descriptions = []
    for description in topic_descriptions_tags: # Get topic description of the corresponding repository
        topic_descriptions.append(description.text.strip())
    return topic_descriptions


def get_topic_urls(soup):
    topic_urls_tags_info = soup.find_all("a", class_= "no-underline flex-1 d-flex flex-column")
    topic_urls = []
    base_url = 'https://github.com/'
    for url in topic_urls_tags_info: # Get topic url of the corresponding repository
        topic_urls.append(base_url + url["href"])
    return topic_urls


# The scrape_topics() function returns a pandas dataframe 
# that contains topic title, topic description and topic page url 
def scrape_topics():
    

    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    page_url = 'https://github.com/topics'
    driver.get(page_url)


    # Wait for the initial content to load (adjust the timeout as needed)
    wait = WebDriverWait(driver, 20)  # Wait up to 10 seconds


    for i in range(5):
    
        try:
            driver.find_element(By.CLASS_NAME, "ajax-pagination-btn")
            # Locate the "Load more" button
            load_more_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ajax-pagination-btn')))
            load_more_button.click()

            print(f"Iteration {i + 1}: Loaded more content.")

            # You might want to add a small delay before the next iteration to ensure stability
            time.sleep(2)  # Wait for 2 seconds before clicking the button again
        except NoSuchElementException:
            print("Exiting Successfully...")
            break
        
        html_content = driver.page_source
    
    # url = "https://github.com/topics"
    # response = requests.get(url)
    # if response.status_code != 200:
        # raise Exception(f"Failed to load page {url}")

    # content = response.text
    
    soup = BeautifulSoup(html_content, 'html.parser')
 
    # topic_titles = get_topic_title(soup)
    # topic_descriptions = get_topic_descriptions(soup)
    # topic_urls = get_topic_urls(soup)

    topics_dict = {'Topic': get_topic_title(soup), 'Description': get_topic_descriptions(soup), 'Link': get_topic_urls(soup)}
    
    folder_path = 'Topics_Information/'
    os.makedirs(folder_path, exist_ok=True)
    pd.DataFrame(topics_dict).to_csv(os.path.join(folder_path, f"topics_information.csv"), index=None)

    return pd.DataFrame(topics_dict)




#-------- Getting Information Out Of A Specific Topic's URL --------#



def get_usernames(soup):
    repo_tags = soup.find_all('h3', class_ = 'f3 color-fg-muted text-normal lh-condensed')
    usernames = []
    for u_name in repo_tags:
        usernames.append(u_name.find_all('a')[0].text.strip())
    return usernames

def get_repo_names(soup):
    repo_tags = soup.find_all('h3', class_ = 'f3 color-fg-muted text-normal lh-condensed')
    repo_names = []
    for repo in repo_tags:
        repo_names.append(repo.find_all('a')[1].text.strip())
    return repo_names

def get_repo_stars(soup):
    stars = soup.find_all('span', id = "repo-stars-counter-star")
    star_counts = []
    for star_score in stars:
        star_counts.append(star_score.text.strip())
    return star_counts

def get_repo_urls(soup):
    repo_tags = soup.find_all('h3', class_ = 'f3 color-fg-muted text-normal lh-condensed')
    repo_urls = []
    base_url = 'https://github.com'
    for rep__url in repo_tags:
        repo_urls.append(base_url + rep__url.find_all('a')[1]['href'])
    return repo_urls


def scrape_topic_repo(url):
    
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    topic_page_url = url
    driver.get(topic_page_url)


    # Wait for the initial content to load (adjust the timeout as needed)
    wait = WebDriverWait(driver, 20)  # Wait up to 10 seconds


    for i in range(4):
    
        try:
            driver.find_element(By.CLASS_NAME, "ajax-pagination-btn")
            # Locate the "Load more" button
            load_more_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ajax-pagination-btn')))
            load_more_button.click()

            print(f"Iteration {i + 1}: Loaded more content.")

            # You might want to add a small delay before the next iteration to ensure stability
            time.sleep(2)  # Wait for 2 seconds before clicking the button again
        except NoSuchElementException:
            break
        
    html_content = driver.page_source
    
    
    soup = BeautifulSoup(html_content, 'html.parser')

    # usernames = get_usernames(soup)
    # repo_names = get_repo_names(soup)
    # star_counts = get_repo_stars(soup)
    # repo_urls = get_repo_urls(soup)

    repos_dict = {'Username': get_usernames(soup), 'Repository': get_repo_names(soup), 'Stars': get_repo_stars(soup), 'Repo URL': get_repo_urls(soup)}
    pd.set_option('display.max_colwidth', None)
    
    return pd.DataFrame(repos_dict)



#-------- Scraping Top Repositories from Each Topic --------#



topics_info_df = scrape_topics()

for index, row in topics_info_df.iterrows():
    
    url = row['Link']
    title = row['Topic']
    folder_path = 'topics/'
    os.makedirs(folder_path, exist_ok=True)
    
    topic_repos_info = scrape_topic_repo(url)
    
    print(f"Scraping the topic: {title}")
    topic_repos_info.to_csv(os.path.join(folder_path, f"{title}.csv"), index=None)
    print(f"^_____^ Successfully saved {title}.csv\n")




# #-------- Getting Information Of All Trending Repositories On Github --------#



# url = "https://github.com/trending?since=daily"
# response = requests.get(url)
# if response.status_code != 200:
#     raise Exception(f"Failed to load page {url}")

# soup = BeautifulSoup(response.text, 'html.parser')\

# username_tags = soup.find_all('article', class_ = 'Box-row')
# usernames = []
# for name in username_tags:
#     usernames.append(name.text.strip())

# # print(usernames)




# # ***--- Project Outline ---***
# #   To scrape: https://github.com/topics
# #   We will get a list of the topics. For each topic in the list, we will get the topic title, topic description and topic page url.
# #   For each topic, we will grab the top 20 repositories from the corresponding topic page.
# #   For each repository, we will grab the repo name, username, stars and repo link.
# #   For each topic, we will create a CSV file in the following format:

# #   Repo Name, Username, Stars, Repo Link
# #   three.js, mrdoob, 94800, https://github.com/mrdoob/three.js 
# #   react-three-fiber, pmndrs, https://github.com/pmndrs/react-three-fiber




# #-------- Project Workflow --------#
# # 1. From topics page, create a list containing all the topics.
# # 2. For each topic, create a list containing all the top repositories belonging to that respective topic.
# # 3. For each topic, create a respective CSV file that contains these top repositories.