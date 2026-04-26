from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json


options = Options()
options.add_argument("--headless")           
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get("https://ethiojobs.net/jobs")
time.sleep(5)

jobs = driver.find_elements(By.TAG_NAME, "a")

job_data = []


for job in jobs:
    try:
        title = job.find_element(By.TAG_NAME, "p").text
        link = job.get_attribute("href")

        if title and "/job/" in link:
            job_data.append({
                "title": title,
                "link": link
            })

    except:
        pass

print("Collected jobs:", len(job_data))



for job in job_data:  
    driver.get(job["link"])
    time.sleep(3)

    try:
        description = driver.find_element(By.TAG_NAME, "main").text
        job["description"] = description
    except:
        job["description"] = "N/A"



with open("jobs.json", "w", encoding="utf-8") as f:
    json.dump(job_data, f, indent=4)

driver.quit()

print("Done. Check jobs.json file.")
