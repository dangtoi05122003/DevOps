from selenium.webdriver.chrome.options import Options
def setup():
    options=Options()
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")
    options.add_argument("headless")
    options.add_argument("no-sandbox")
    options.add_argument("disable-dev-shm-usage")
    return options