import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from PIL import Image

chrome_options = Options()
delay = 10 # seconds

def get_warranty_HTML(serial):
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--log-level=3")
  driver = webdriver.Chrome('C:/TEMP/chromedriver.exe', options=chrome_options)
  driver.get('https://support.hpe.com/hpsc/wc/public/find')
  if os.name == "posix": 
    os.system ("clear")
  elif os.name == ("ce" or "nt" or "dos"): 
    os.system ("cls")

# Time to waiting is page is ready 'delay'  
  try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'captchaChars')))
    print ("Page is ready!")
    captcha_def(driver, serial)
  except TimeoutException:
    print ("Loading took too much time!")
    quit()

def captcha_def(driver, serial):
  try:
    z = 0
    if z > 1:
      print('Captcha fail, try again...')
    while driver.find_element_by_id('captchaChars'):
      element = driver.find_element_by_xpath('//*[@id="captchaImg"]')
      location = element.location
      size = element.size
      driver.save_screenshot('pageimage.png')
      # crop image
      x = location['x']
      y = location['y']
      width = location['x']+size['width']
      height = location['y']+size['height']
      im = Image.open('pageImage.png')
      im = im.crop((int(x), int(y), int(width), int(height)))
      im.save('captcha.png')
      #os.startfile('captcha.png')
      img= Image.open('captcha.png')
      img.show()
      if os.name == "posix": 
        os.system ("clear")
      elif os.name == ("ce" or "nt" or "dos"): 
        os.system ("cls")
      capt_re = input('Please insert captcha: ')
      driver.find_element_by_id('captchaChars').send_keys(capt_re)
      driver.find_element_by_id('captchaSubmitBtn').click()
      os.system('TASKKILL /F /IM Microsoft.Photos.exe 2>NUL') #for windows 10
      if os.name == "posix": 
        os.system ("clear")
      elif os.name == ("ce" or "nt" or "dos"): 
        os.system ("cls")
  except:
    print('No more captcha needed')
    get_data_serial(driver, serial)

def get_data_serial(driver, serial):
  try:   
    driver.find_element_by_id('serialNumber0').send_keys(serial)
    driver.find_element_by_name('submitButton').click()
  except:
    print('Submit Button or field to fill with Serial not found, exit...')
  try:
    driver.find_element_by_xpath('//*[@id="nonIntroBlock"]/div')
    product_n = input('*Product number: ')
    driver.finde_element_by_id('productNumber0').send_keys(product_n)
    driver.find_element_by_name('submitButton').click()
    paso = 1
  except:
    paso = 1
	
  if paso == 1:
    for element in driver.find_elements_by_xpath('//*[@id="product_description_%s"]/h3/b' %(serial)):
      print (element.text)
  
    for element in driver.find_elements_by_xpath('//*[@id="generate_table_%s"]/table/tbody' %(serial)):
      print (element.text)
    wait = input('Press ENTER to continue.')
  
def main(argv):
  if len(argv) < 2:
      print("ERROR: A valid HPE Serial Number must be specified as an argument to this script")
      argv = [0, input('Please insert your serial: ')]

  print('\nChecking for %s ... \n' % (argv[1]))
  get_warranty_HTML(argv[1])
  
if __name__ == "__main__":
    main(sys.argv)