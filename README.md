# hpe-warranty-lookup-selenium
Python script for looking up active warranties on HPE servers with selenium and chromedriver. Based in Windows 10 commands for open and check captcha.

## Requirements
* Selenium
* Image
* os
* sys
* Python3

## Usage
./hpe-warranty-lookup-selenium.py <Serial_Number>

If you don't introduce a serial, the script ask to input.

./hpe-warranty-lookup-multiple-selenium.py

Check serials till 20 serial number in a txt file and extract the information and saved the reponse in checked.txt
