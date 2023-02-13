from selenium import webdriver
from selenium.webdriver.common.by import By
import json

class Data:
    def __init__(self, title, description, paras) -> None:
        self.title = title
        self.description = description
        self.paras = paras

# Initialize the JSON data object
data = {"content": []}

url = "https://dantri.com.vn/the-gioi/ong-kim-jong-un-yeu-cau-tang-toc-phat-trien-tiem-luc-quan-su-20230210132924777.htm"

# Use Selenium to extract the data from the web page
driver = webdriver.Chrome("../chromedriver.exe")

def crawlDantri(url):
    
    if "dantri.com.vn" not in url:
        return "khong dung duoc"
    else:
        cut = url.split("/")
        file_name = cut[-1].replace(".htm", '').replace("-", "_")
        file_name = str(file_name) + ".json"
        
        driver.get(url)
        
        # Get title
        title = driver.find_element(By.XPATH, "/html/body/main/div[1]/div[2]/div[1]/article[1]/h1")
        title = title.text

        # Get description
        description = driver.find_element(By.XPATH, "/html/body/main/div[1]/div[2]/div[1]/article[1]/h2")
        description = description.text

        # Get content
        paras = []
        count = len(driver.find_elements(By.XPATH,"/html/body/main/div[1]/div[2]/div[1]/article[1]/div[3]/p"))
        for i in range(1,count):
            base_xpath = "/html/body/main/div[1]/div[2]/div[1]/article[1]/div[3]/p[" + str(i) + "]"
            para = driver.find_element(By.XPATH, base_xpath).text.replace('"', "'")
            paras.append(para)
            
        driver.close()

        # Store the data in a Data object
        content = Data(title, description, paras)

        # Append the new data to the content list
        data["content"].append({"title": content.title, "description": content.description, "paras": content.paras})

        # Write the JSON data object to a file
        with open(file_name, "w", encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return "Data written successfully to data.json"

crawlDantri(url)