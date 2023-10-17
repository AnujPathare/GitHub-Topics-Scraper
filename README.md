# Scraping Popular GitHub Topics

## Introducing Web Scraping: Unlocking the Data-Driven World

In the vast landscape of the internet, an incredible wealth of information lies within websites, waiting to be discovered. Imagine being able to extract this data automatically, transforming it into valuable insights, and fueling innovation. Web scraping, a powerful technique, opens the door to this data-driven universe.

- **What is Web Scraping?**

At its core, web scraping is the automated method of extracting large amounts of data from websites quickly. It's akin to a digital detective, capable of navigating the intricate web structures, gathering relevant information, and organizing it for analysis. Think of it as a bridge between the human-readable web and the data-driven computational world.

![](https://miro.medium.com/v2/resize:fit:1400/1*jDaMcAZfTHcbBHUWpS3itw.png)

- **How Does Web Scraping Work?**

Web scraping involves utilizing specialized software tools (commonly developed using programming languages like Python, JavaScript, or Ruby) to send requests to a website and then parse the HTML or other markup languages of the web pages. By understanding the structure of the web pages and employing techniques like CSS selectors or XPath, web scrapers can precisely target and extract the required data.

- **Ethics and Responsibility in Web Scraping**

While web scraping offers incredible potential, it is essential to use this technique responsibly and ethically. Respecting websites' terms of service, adhering to legal guidelines, and ensuring the privacy of individuals are paramount. Responsible web scraping practices preserve the integrity of the internet and foster a collaborative digital environment.

## Project Workflow
1. From GitHub's Popular Topics page, extracting all the topics.

- 3D
- Ajax
- Algorithm
- ...

2. Creating a CSV file that contains the Topic Title, Topic Description, and Topic URL.

|Topic|Description|Link|
|:------|:------|:------|
|3D     |"3D refers to the use of three-dimensional graphics, modeling, and animation in various industries."     |https://github.com//topics/3d     |
|Ajax     |Ajax is a technique for creating interactive web applications.     |https://github.com//topics/ajax     |
|Algorithm     |Algorithms are self-contained sequences that carry out a variety of tasks.     |https://github.com//topics/algorithm     |
|...     |...     |...     |

3. For each topic, creating a CSV file containing information about top the 100 repositories belonging to that respective topic.

**<center>3D.csv</center>**

|Username|Repository|Stars|Repo URL|
|:------|:------|:------|:------|
|mrdoob     |three.js     |94.9k     |https://github.com/mrdoob/three.js     |
|pmndrs     |react-three-fiber     |24k     |https://github.com/pmndrs/react-three-fiber     |
|libgdx     |libgdx     |22.1k     |https://github.com/libgdx/libgdx     |
|...     |...     |...     |...     |



#### Tools Utilized in the Project:
1. **Requests:** Python library for easy HTTP requests, ideal for web data retrieval.
2. **Selenium:** Automation framework for web interaction.
3. **BeautifulSoup:**  Python tool for parsing parsing HTML/XML, simplifying data extraction from web pages.
4. **Pandas:** Python library for converting lists to a Pandas Dataframe.

---
## <center>Let's Begin!!</center>
---

- Installing the necessary libraries.


```python
!pip install requests --upgrade --quiet
!pip install selenium --upgrade --quiet
!pip install beautifulsoup4 --upgrade --quiet
!pip install pandas --upgrade --quiet
```

- Importing the necessary modules.


```python
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import os
import time
import requests
import pandas as pd
```

**Requests** is used to send HTTP request to a website and store the response object within a variable.

- We check the status code to ensure that the request to the website was successful (status code 200). It helps detect errors (such as 404 for page not found) and ensures data is scraped from valid, accessible pages, enhancing the reliability and accuracy of the scraping process.




```python
url = "https://github.com/topics"
response = requests.get(url)
response.status_code
```




    200



### Getting Information Of All Popular Topics On GitHub

- Extracting HTML tags containing the topic title.



```python
def get_topic_title(soup):
    
    topic_titles_tags = soup.find_all("p", class_ = "f3 lh-condensed mb-0 mt-1 Link--primary")
    topic_titles = []
    for title in topic_titles_tags: # Get topic title of the corresponding repository
        topic_titles.append(title.text.strip())
    return topic_titles
```

- Extracting HTML tags containing topic description.



```python
def get_topic_descriptions(soup):

    topic_descriptions_tags = soup.find_all("p", class_ = "f5 color-fg-muted mb-0 mt-1")
    topic_descriptions = []
    for description in topic_descriptions_tags: # Get topic description of the corresponding repository
        topic_descriptions.append(description.text.strip())
    return topic_descriptions
```

- Extracting HTML tags containing topic URLs.



```python
def get_topic_urls(soup):
    
    topic_urls_tags_info = soup.find_all("a", class_= "no-underline flex-1 d-flex flex-column")
    topic_urls = []
    base_url = 'https://github.com/'
    for url in topic_urls_tags_info: # Get topic url of the corresponding repository
        topic_urls.append(base_url + url["href"])
    return topic_urls
```

**Selenium** allows you to automate the process of collecting data and can save you significant time and effort. Using Selenium, you can interact with websites just like a human user and extract the data you need more efficiently.

**BeautifulSoup** is used for parsing the HTML document. Using BeautifulSoup, we extract all the tags containing information relevant to us.

**Pandas** is used for data wrangling and data manipulation purposes. We store the collected data in a CSV file using pandas.

- The **scrape_topics()** function uses Selenium to load the whole https://github.com/topics page, extract its HTML content and then uses Pandas to save information related to all the topics to a CSV file and returns a Pandas dataframe that contains the topic title, topic description and topic page URL.


```python
def scrape_topics():
    
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    page_url = 'https://github.com/topics'
    driver.get(page_url)


    # Wait for the initial content to load (adjust the timeout as needed)
    
    wait = WebDriverWait(driver, 20)  # Wait up to 20 seconds


    for i in range(5):
    
        try:
            driver.find_element(By.CLASS_NAME, "ajax-pagination-btn")
            
            # Locate the "Load more" button
            load_more_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ajax-pagination-btn')))
            load_more_button.click()

            print(f"Iteration {i + 1}: Loaded more content.")

            # Add a small delay before the next iteration to ensure stability
            time.sleep(2)  # Wait for 2 seconds before clicking the button again
        
        except NoSuchElementException:
            print("Exiting Successfully...")
            break
        
        html_content = driver.page_source

        
    soup = BeautifulSoup(html_content, 'html.parser')
 
    topics_dict = {'Topic': get_topic_title(soup), 'Description': get_topic_descriptions(soup), 'Link': get_topic_urls(soup)}
    
    folder_path = 'Topics_Information/'
    os.makedirs(folder_path, exist_ok=True)
    pd.DataFrame(topics_dict).to_csv(os.path.join(folder_path, f"topics_information.csv"), index=None)
    
    print(f"Successfully saved information about all the popular topics!\n")
    
    return pd.DataFrame(topics_dict)
```

### Getting Information Out Of A Specific Topic's URL

- Extracting HTML tags containing the username of the repository's owner.



```python
def get_usernames(soup):
    
    repo_tags = soup.find_all('h3', class_ = 'f3 color-fg-muted text-normal lh-condensed')
    usernames = []
    for u_name in repo_tags:
        usernames.append(u_name.find_all('a')[0].text.strip())
    return usernames
```

- Accessing the child element from the above extracted tags, as they contain information about the repository name.


```python
def get_repo_names(soup):
    
    repo_tags = soup.find_all('h3', class_ = 'f3 color-fg-muted text-normal lh-condensed')
    repo_names = []
    for repo in repo_tags:
        repo_names.append(repo.find_all('a')[1].text.strip())
    return repo_names
```

- Extracting HTML tags containing stars count.



```python
def get_repo_stars(soup):
    
    stars = soup.find_all('span', id = "repo-stars-counter-star")
    star_counts = []
    for star_score in stars:
        star_counts.append(star_score.text.strip())
    return star_counts
```

- Extracting HTML tags containing information about the repository's URL. We get the repository URL by accessing the child element of the tags extacted to collect the username of the repository's owner.



```python
def get_repo_urls(soup):
    
    repo_tags = soup.find_all('h3', class_ = 'f3 color-fg-muted text-normal lh-condensed')
    repo_urls = []
    base_url = 'https://github.com'
    for rep__url in repo_tags:
        repo_urls.append(base_url + rep__url.find_all('a')[1]['href'])
    return repo_urls
```

- The **scrape_topic_repo()** function uses Selenium to visit the URL of each topic present in the 'topics_information.csv' file, load the whole page, extract its HTML content and then uses Pandas to return a pandas dataframe containing information about the top 100 repositories belonging to that respective topic.


```python
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

            # Add a small delay before the next iteration to ensure stability
            time.sleep(2)  # Wait for 2 seconds before clicking the button again
        
        except NoSuchElementException:
            break
        
    html_content = driver.page_source
    
    
    soup = BeautifulSoup(html_content, 'html.parser')

    repos_dict = {'Username': get_usernames(soup), 'Repository': get_repo_names(soup), 'Stars': get_repo_stars(soup), 'Repo URL': get_repo_urls(soup)}
    pd.set_option('display.max_colwidth', None)
    
    return pd.DataFrame(repos_dict)
```

### Let's begin to scrape top repositories from each topic.


```python
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
```

    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Iteration 5: Loaded more content.
    Successfully saved information about all the popular topics!
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: 3D
    ^_____^ Successfully saved 3D.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Ajax
    ^_____^ Successfully saved Ajax.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Algorithm
    ^_____^ Successfully saved Algorithm.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Amp
    ^_____^ Successfully saved Amp.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Android
    ^_____^ Successfully saved Android.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Angular
    ^_____^ Successfully saved Angular.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Ansible
    ^_____^ Successfully saved Ansible.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: API
    ^_____^ Successfully saved API.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Arduino
    ^_____^ Successfully saved Arduino.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: ASP.NET
    ^_____^ Successfully saved ASP.NET.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Atom
    ^_____^ Successfully saved Atom.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Awesome Lists
    ^_____^ Successfully saved Awesome Lists.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Amazon Web Services
    ^_____^ Successfully saved Amazon Web Services.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Azure
    ^_____^ Successfully saved Azure.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Babel
    ^_____^ Successfully saved Babel.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Bash
    ^_____^ Successfully saved Bash.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Bitcoin
    ^_____^ Successfully saved Bitcoin.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Bootstrap
    ^_____^ Successfully saved Bootstrap.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Bot
    ^_____^ Successfully saved Bot.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: C
    ^_____^ Successfully saved C.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Chrome
    ^_____^ Successfully saved Chrome.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Chrome extension
    ^_____^ Successfully saved Chrome extension.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Command line interface
    ^_____^ Successfully saved Command line interface.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Clojure
    ^_____^ Successfully saved Clojure.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Code quality
    ^_____^ Successfully saved Code quality.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Code review
    ^_____^ Successfully saved Code review.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Compiler
    ^_____^ Successfully saved Compiler.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Continuous integration
    ^_____^ Successfully saved Continuous integration.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: COVID-19
    ^_____^ Successfully saved COVID-19.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: C++
    ^_____^ Successfully saved C++.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Cryptocurrency
    ^_____^ Successfully saved Cryptocurrency.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Crystal
    ^_____^ Successfully saved Crystal.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: C#
    ^_____^ Successfully saved C#.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: CSS
    ^_____^ Successfully saved CSS.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Data structures
    ^_____^ Successfully saved Data structures.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Data visualization
    ^_____^ Successfully saved Data visualization.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Database
    ^_____^ Successfully saved Database.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Deep learning
    ^_____^ Successfully saved Deep learning.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Dependency management
    ^_____^ Successfully saved Dependency management.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Deployment
    ^_____^ Successfully saved Deployment.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Django
    ^_____^ Successfully saved Django.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Docker
    ^_____^ Successfully saved Docker.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Documentation
    ^_____^ Successfully saved Documentation.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: .NET
    ^_____^ Successfully saved .NET.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Electron
    ^_____^ Successfully saved Electron.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Elixir
    ^_____^ Successfully saved Elixir.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Emacs
    ^_____^ Successfully saved Emacs.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Ember
    ^_____^ Successfully saved Ember.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Emoji
    ^_____^ Successfully saved Emoji.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Emulator
    ^_____^ Successfully saved Emulator.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: ESLint
    ^_____^ Successfully saved ESLint.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Ethereum
    ^_____^ Successfully saved Ethereum.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Express
    ^_____^ Successfully saved Express.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Firebase
    ^_____^ Successfully saved Firebase.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Firefox
    ^_____^ Successfully saved Firefox.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Flask
    ^_____^ Successfully saved Flask.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Font
    ^_____^ Successfully saved Font.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Framework
    ^_____^ Successfully saved Framework.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Front end
    ^_____^ Successfully saved Front end.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Game engine
    ^_____^ Successfully saved Game engine.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Git
    ^_____^ Successfully saved Git.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: GitHub API
    ^_____^ Successfully saved GitHub API.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Go
    ^_____^ Successfully saved Go.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Google
    ^_____^ Successfully saved Google.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Gradle
    ^_____^ Successfully saved Gradle.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: GraphQL
    ^_____^ Successfully saved GraphQL.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Gulp
    ^_____^ Successfully saved Gulp.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Hacktoberfest
    ^_____^ Successfully saved Hacktoberfest.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Haskell
    ^_____^ Successfully saved Haskell.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Homebrew
    ^_____^ Successfully saved Homebrew.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Homebridge
    ^_____^ Successfully saved Homebridge.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: HTML
    ^_____^ Successfully saved HTML.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: HTTP
    ^_____^ Successfully saved HTTP.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Icon font
    ^_____^ Successfully saved Icon font.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: iOS
    ^_____^ Successfully saved iOS.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: IPFS
    ^_____^ Successfully saved IPFS.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Java
    ^_____^ Successfully saved Java.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: JavaScript
    ^_____^ Successfully saved JavaScript.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Jekyll
    ^_____^ Successfully saved Jekyll.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: jQuery
    ^_____^ Successfully saved jQuery.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: JSON
    ^_____^ Successfully saved JSON.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: The Julia Language
    ^_____^ Successfully saved The Julia Language.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Jupyter Notebook
    ^_____^ Successfully saved Jupyter Notebook.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Koa
    ^_____^ Successfully saved Koa.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Kotlin
    ^_____^ Successfully saved Kotlin.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Kubernetes
    ^_____^ Successfully saved Kubernetes.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Laravel
    ^_____^ Successfully saved Laravel.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: LaTeX
    ^_____^ Successfully saved LaTeX.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Library
    ^_____^ Successfully saved Library.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Linux
    ^_____^ Successfully saved Linux.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Localization (l10n)
    ^_____^ Successfully saved Localization (l10n).csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Lua
    ^_____^ Successfully saved Lua.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Machine learning
    ^_____^ Successfully saved Machine learning.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: macOS
    ^_____^ Successfully saved macOS.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Markdown
    ^_____^ Successfully saved Markdown.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Mastodon
    ^_____^ Successfully saved Mastodon.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Material Design
    ^_____^ Successfully saved Material Design.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: MATLAB
    ^_____^ Successfully saved MATLAB.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Maven
    ^_____^ Successfully saved Maven.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Minecraft
    ^_____^ Successfully saved Minecraft.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Mobile
    ^_____^ Successfully saved Mobile.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Monero
    ^_____^ Successfully saved Monero.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: MongoDB
    ^_____^ Successfully saved MongoDB.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Mongoose
    ^_____^ Successfully saved Mongoose.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Monitoring
    ^_____^ Successfully saved Monitoring.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: MvvmCross
    ^_____^ Successfully saved MvvmCross.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: MySQL
    ^_____^ Successfully saved MySQL.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: NativeScript
    ^_____^ Successfully saved NativeScript.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Nim
    ^_____^ Successfully saved Nim.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Natural language processing
    ^_____^ Successfully saved Natural language processing.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Node.js
    ^_____^ Successfully saved Node.js.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: NoSQL
    ^_____^ Successfully saved NoSQL.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: npm
    ^_____^ Successfully saved npm.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Objective-C
    ^_____^ Successfully saved Objective-C.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: OpenGL
    ^_____^ Successfully saved OpenGL.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Operating system
    ^_____^ Successfully saved Operating system.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: P2P
    ^_____^ Successfully saved P2P.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Package manager
    ^_____^ Successfully saved Package manager.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Parsing
    ^_____^ Successfully saved Parsing.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Perl
    ^_____^ Successfully saved Perl.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Phaser
    ^_____^ Successfully saved Phaser.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: PHP
    ^_____^ Successfully saved PHP.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: PICO-8
    ^_____^ Successfully saved PICO-8.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Pixel Art
    ^_____^ Successfully saved Pixel Art.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: PostgreSQL
    ^_____^ Successfully saved PostgreSQL.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Project management
    ^_____^ Successfully saved Project management.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Publishing
    ^_____^ Successfully saved Publishing.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: PWA
    ^_____^ Successfully saved PWA.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Python
    ^_____^ Successfully saved Python.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Qt
    ^_____^ Successfully saved Qt.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: R
    ^_____^ Successfully saved R.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Rails
    ^_____^ Successfully saved Rails.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Raspberry Pi
    ^_____^ Successfully saved Raspberry Pi.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Ratchet
    ^_____^ Successfully saved Ratchet.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: React
    ^_____^ Successfully saved React.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: React Native
    ^_____^ Successfully saved React Native.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: ReactiveUI
    ^_____^ Successfully saved ReactiveUI.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Redux
    ^_____^ Successfully saved Redux.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: REST API
    ^_____^ Successfully saved REST API.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Ruby
    ^_____^ Successfully saved Ruby.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Rust
    ^_____^ Successfully saved Rust.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Sass
    ^_____^ Successfully saved Sass.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Scala
    ^_____^ Successfully saved Scala.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: scikit-learn
    ^_____^ Successfully saved scikit-learn.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Software-defined networking
    ^_____^ Successfully saved Software-defined networking.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Security
    ^_____^ Successfully saved Security.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Server
    ^_____^ Successfully saved Server.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Serverless
    ^_____^ Successfully saved Serverless.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Shell
    ^_____^ Successfully saved Shell.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Sketch
    ^_____^ Successfully saved Sketch.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Scraping the topic: SpaceVim
    ^_____^ Successfully saved SpaceVim.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Spring Boot
    ^_____^ Successfully saved Spring Boot.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: SQL
    ^_____^ Successfully saved SQL.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Storybook
    ^_____^ Successfully saved Storybook.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Support
    ^_____^ Successfully saved Support.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Swift
    ^_____^ Successfully saved Swift.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Symfony
    ^_____^ Successfully saved Symfony.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Telegram
    ^_____^ Successfully saved Telegram.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Tensorflow
    ^_____^ Successfully saved Tensorflow.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Terminal
    ^_____^ Successfully saved Terminal.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Terraform
    ^_____^ Successfully saved Terraform.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Testing
    ^_____^ Successfully saved Testing.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Twitter
    ^_____^ Successfully saved Twitter.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: TypeScript
    ^_____^ Successfully saved TypeScript.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Ubuntu
    ^_____^ Successfully saved Ubuntu.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Unity
    ^_____^ Successfully saved Unity.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Unreal Engine
    ^_____^ Successfully saved Unreal Engine.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Vagrant
    ^_____^ Successfully saved Vagrant.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Vim
    ^_____^ Successfully saved Vim.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Virtual reality
    ^_____^ Successfully saved Virtual reality.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Vue.js
    ^_____^ Successfully saved Vue.js.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Wagtail
    ^_____^ Successfully saved Wagtail.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Web Components
    ^_____^ Successfully saved Web Components.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Web app
    ^_____^ Successfully saved Web app.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Webpack
    ^_____^ Successfully saved Webpack.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Windows
    ^_____^ Successfully saved Windows.csv
    
    Scraping the topic: WordPlate
    ^_____^ Successfully saved WordPlate.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: WordPress
    ^_____^ Successfully saved WordPress.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: Xamarin
    ^_____^ Successfully saved Xamarin.csv
    
    Iteration 1: Loaded more content.
    Iteration 2: Loaded more content.
    Iteration 3: Loaded more content.
    Iteration 4: Loaded more content.
    Scraping the topic: XML
    ^_____^ Successfully saved XML.csv
    
    


```python

```
