from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_experimental_option(
    "excludeSwitches", ["enable-logging"]
)  # Optional for reducing logging
options.add_argument(
    "--no-sandbox"
)  # Needed for running Chrome in headless mode in containers

# Run in headless mode (optional, for faster execution without a visible browser window)
options.add_argument("--headless")

# Ensure ChromeDriver is updated and managed automatically
driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)


url = "https://www.example.com"  # Replace with the desired URL

try:
    driver.get(url)
    driver.implicitly_wait(10)  # Wait up to 10 seconds for page elements to load

    page_title = driver.title
    print("Page title:", page_title)

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()  # Ensure driver is closed even if exceptions occur
