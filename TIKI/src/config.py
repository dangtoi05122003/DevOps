from selenium.webdriver.chrome.options import Options
def setup():
    options=Options()
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")
    return options