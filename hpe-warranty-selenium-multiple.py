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

def get_warranty_HTML(file):
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--log-level=3")
  driver = webdriver.Chrome('C:/TEMP/chromedriver.exe', options=chrome_options)
  driver.get('https://support.hpe.com/hpsc/wc/public/find')
  # Time to waiting is page is ready 'delay'  
  try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'captchaChars')))
    print ("Page is ready!")
  except TimeoutException:
    print ("Loading took too much time!")
    quit()
	
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
      img=Image.open('captcha.png')
      img.show()
      capt_re = input('Please insert captcha: ')
      driver.find_element_by_id('captchaChars').send_keys(capt_re)
      driver.find_element_by_id('captchaSubmitBtn').click()
      img.close()
      os.system('TASKKILL /F /IM Microsoft.Photos.exe 2>NUL') #for windows 10
  except:
    print('No more captcha needed')

  count_lines = len(open(file).readlines())
  
  if count_lines < 10:
    check_n(count_lines, file, driver)
    
  elif count_lines <= 20:
    driver.find_element_by_xpath('//*[@id="wcFormDataItem"]/span/a').click()
    check_n(count_lines, file, driver)
  else:
    print('No more of 20 serials')
    quit()
    
def check_n(count_lines, file, driver):
  n = 0
  try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'serialNumber%s' %(n))))
    print ("Checking Serials, please wait...!")
  except TimeoutException:
    print ("Loading took too much time!")
  while n < count_lines:
    for line in open(file):
      driver.find_element_by_id('serialNumber%s' %(n)).send_keys(line.strip())
      n= n + 1
  
  try:  
    driver.find_element_by_name('submitButton').click()
  except:
    print('Submit Button not found, exit...')
    quit()
  
  try:
    driver.find_element_by_xpath('//*[@id="nonIntroBlock"]/div')
    product_n = input('*Product number: ')
    driver.finde_element_by_id('productNumber0').send_keys(product_n)
    driver.find_element_by_name('submitButton').click()
    paso = 1
  except:
    paso = 1

  if paso == 1:
    f = open("checked.txt","a")
    for line in open(file):
      print('Warranty checked for '+ line.strip())
      f.write('\nWarranty checked for '+ line.strip() +('\n'))
      print('-----------------------------------------------')
      f.write('----------------------------------------------- \n')
      for element in driver.find_elements_by_xpath('//*[@id="product_description_%s"]/h3/b' %(line.strip())):
        print (element.text)
        f.write(element.text +('\n'))
      for element in driver.find_elements_by_xpath('//*[@id="generate_table_%s"]/table/tbody' %(line.strip())):
        print (element.text)
        f.write(element.text)
        print('\n')
        f.write('\n')
    f.close()
    wait = input('All SN checked press ENTER to finish.')

def main(argv):
  if len(argv) == os.path.isfile('*.txt'):
    print('\nChecking for %s ... \n' % (argv[1]))
    get_warranty_HTML(argv[1])
  else:
    while True:
      argv = input('Please insert your txt file (q): ')
      
      if os.path.isfile(argv):
        print('\nChecking for %s ... \n' % (argv))
        get_warranty_HTML(argv)
      if argv == 'q':
        quit()
      else:
        print('Fichero no valido')

if __name__ == "__main__":
    main(sys.argv)