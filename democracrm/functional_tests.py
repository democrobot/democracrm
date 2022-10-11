from selenium import webdriver
print('Loading...')
firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = True
browser = webdriver.Firefox(options=firefox_options)  #
browser.get('https://localhost:8000')

print('Loaded.')

# assert 'The install worked successfully!' in browser.title

browser.quit()
