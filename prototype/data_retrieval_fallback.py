import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from datetime import date

# driver = uc.Chrome(driver_executable_path = 'chromedriver.exe')

# this should match chrome version (current latest chrome version as of writing this comment: 151)
# need to automate matching local chrome version as it only runs latest version unless specified 
driver = uc.Chrome(version_main = 150)  

'''--------------------------------------------------------------------------------------------------------------------------'''
''' download rice stock inventory '''
# driver.get(
#     'https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__2E__CS/0032E4ECNV0.px/?__cf_chl_f_tk' \
#     '=Q0NnUBaUlEc.w1YA6_K9eDave0yIugUd5I_YQMpCDSA-1782738461-1.0.1.1-qAT6PwIdkUBTLEY2jomAAFd2VkyHpj4yJx5wplA53eM'
#     )
driver.get(
    'https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__2E__CS/0032E4ECNV0.px/?rxid=2f2df3e4-1a1a-4bf7-9802-5995d6bd9dee'
)

rice = ['Rice: Total Stock', 'Rice: Household Stock', 
        'Rice: Commercial Stock', 'Rice: NFA Stock']
months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
curr_year = date.today().year

# select rice types
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Rice: Total Stock')]"))
)
for rice_type in rice:
    driver.find_element(By.XPATH, f"//*[contains(text(), '{rice_type}')]").click()

# select year (drag [current year] and drop [2000] because 2017 cannot be selected)
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '2000')]"))
)
source_element = driver.find_element(By.XPATH, f"//*[contains(text(), '{curr_year}')]")
target_element = driver.find_element(By.XPATH, "//*[contains(text(), '1999')]")

actions = ActionChains(driver)
actions.drag_and_drop(source_element, target_element).perform()

# click year 1999 to exclude from query 
driver.find_element(By.XPATH, "//*[contains(text(), '1999')]").click()

# select months 
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'January')]"))
)
for month in months:
    driver.find_element(By.XPATH, f"//*[contains(text(), '{month}')]").click()

# select csv file type and download
driver.find_element(By.XPATH, f"//*[contains(text(), 'Comma delimited with heading')]").click()
driver.find_element(By.ID, 'ctl00_ContentPlaceHolderMain_VariableSelector1_VariableSelector1_ButtonViewTable').click()
time.sleep(1)

'''--------------------------------------------------------------------------------------------------------------------------'''
''' Download wholesale rice prices '''
# Link 1 (wholesale rice price new series [from x to current year])
driver.get(
    'https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__2M__NWSNEW/0052M4AWB01.px/?rxid=c4f7f965-0ca3-4191-bc17-f093fc76f63c'
)

# select region: PHILIPPINES
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'PHILIPPINES')]"))
)
driver.find_element(By.XPATH, f"//*[contains(text(), 'PHILIPPINES')]").click()

# select commodities
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Well Milled Rice (WMR)')]"))
)
driver.find_element(By.XPATH, f"//*[contains(text(), 'Well Milled Rice (WMR)')]").click()
driver.find_element(By.XPATH, f"//*[contains(text(), 'Regular Milled Rice (RMR)')]").click()

# select year
text_box_year = 'ctl00_ContentPlaceHolderMain_VariableSelector1_VariableSelector1_VariableSelectorValueSelectRepeater' \
            '_ctl03_VariableValueSelect_VariableValueSelect_SearchValuesTextbox'
year = 2000
while(curr_year >= year):
    box = driver.find_element(By.ID, text_box_year)
    box.send_keys(f'{year}' + Keys.ENTER)
    box.clear()
    year += 1

# select month
for month in months:
    driver.find_element(By.XPATH, f"//*[contains(text(), '{month}')]").click()

# select csv file type and download
driver.find_element(By.XPATH, f"//*[contains(text(), 'Comma delimited with heading')]").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderMain_VariableSelector1_VariableSelector1_ButtonViewTable").click()
time.sleep(1)

''' Data extension '''
# Link 2 (wholesale rice price old series [from 2000 to x])
driver.get(
    'https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__2M__WS/0012M4AWP01.px/?rxid=2187481f-e6b9-4cf3-bd03-05d803a64dd7'
)

# select region: PHILIPPINES
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'PHILIPPINES')]"))
)
driver.find_element(By.XPATH, f"//*[contains(text(), 'PHILIPPINES')]").click()

# select commodities
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Well Milled Rice (WMR)')]"))
)
driver.find_element(By.XPATH, f"//*[contains(text(), 'Well Milled Rice (WMR)')]").click()
driver.find_element(By.XPATH, f"//*[contains(text(), 'Regular Milled Rice (RMR)')]").click()

year = 2000
while(curr_year >= year):
    box = driver.find_element(By.ID, text_box_year)
    box.send_keys(f'{year}' + Keys.ENTER)
    box.clear()
    year += 1

# select month
for month in months:
    driver.find_element(By.XPATH, f"//*[contains(text(), '{month}')]").click()

# select csv file type and download
driver.find_element(By.XPATH, f"//*[contains(text(), 'Comma delimited with heading')]").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderMain_VariableSelector1_VariableSelector1_ButtonViewTable").click()
time.sleep(1)

'''--------------------------------------------------------------------------------------------------------------------------'''
''' Download retail rice prices '''
# Link 1 (retail rice price new series [from x to current year])
driver.get(
    'https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__2M__2018NEW/0042M4ARN01.px/?rxid=70eda2de-8cce-4538-b441-b81b8456b360'
)

# select region (geolocation): PHILIPPINES  *** MIGHT CAUSE ERROR ***
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Philippines')]"))
)
text_box_geoloc = 'ctl00_ContentPlaceHolderMain_VariableSelector1_VariableSelector1_VariableSelectorValueSelectRepeater_' \
                'ctl01_VariableValueSelect_VariableValueSelect_SearchValuesTextbox'
geolocation = driver.find_element(By.ID, text_box_geoloc)
geolocation.send_keys('Philippines' + Keys.ENTER)
geolocation.clear()

# select commodities
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'RICE, WELL-MILLED, 1 KG')]"))
)
text_box_commodities = 'ctl00_ContentPlaceHolderMain_VariableSelector1_VariableSelector1_VariableSelectorValueSelectRepeater_' \
                    'ctl02_VariableValueSelect_VariableValueSelect_SearchValuesTextbox'
commodity = driver.find_element(By.ID, text_box_commodities)
commodity.send_keys('RICE, WELL-MILLED, 1 KG' + Keys.ENTER)
commodity.clear()

commodity.send_keys('RICE, REGULAR-MILLED, 1 KG' + Keys.ENTER)
commodity.clear()

# driver.find_element(By.XPATH, f"//*[contains(text(), 'RICE, WELL-MILLED, 1 KG')]").click()
# driver.find_element(By.XPATH, f"//*[contains(text(), 'RICE, REGULAR-MILLED, 1 KG')]").click()

# select year
year = 2000
while(curr_year >= year):
    box = driver.find_element(By.ID, text_box_year)
    box.send_keys(f'{year}' + Keys.ENTER)
    box.clear()
    year += 1

# select month (period)
for month in months:
    driver.find_element(By.XPATH, f"//*[contains(text(), '{month}')]").click()

# select csv file type and download
driver.find_element(By.XPATH, f"//*[contains(text(), 'Comma delimited with heading')]").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderMain_VariableSelector1_VariableSelector1_ButtonViewTable").click()
time.sleep(1)

''' Data extension '''
# Link 2 (retail rice price old series [from 2000 to x])
driver.get(
    'https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__2M__RP/0042M4ARP01.px/?rxid=11176638-8515-41a0-b48c-e304faa32380'
)

# select region (geolocation): PHILIPPINES  *** MIGHT CAUSE ERROR ***
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'PHILIPPINES')]"))
)
driver.find_element(By.XPATH, f"//*[contains(text(), 'PHILIPPINES')]").click()

# select commodities
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Well Milled Rice (WMR)')]"))
)
driver.find_element(By.XPATH, f"//*[contains(text(), 'Well Milled Rice (WMR)')]").click()
driver.find_element(By.XPATH, f"//*[contains(text(), 'Regular Milled Rice (RMR)')]").click()

# select year
year = 2000
while(curr_year >= year):
    box = driver.find_element(By.ID, text_box_year)
    box.send_keys(f'{year}' + Keys.ENTER)
    box.clear()
    year += 1

# select month (period)
for month in months:
    driver.find_element(By.XPATH, f"//*[contains(text(), '{month}')]").click()

# select csv file type and download
driver.find_element(By.XPATH, f"//*[contains(text(), 'Comma delimited with heading')]").click()
driver.find_element(By.ID, "ctl00_ContentPlaceHolderMain_VariableSelector1_VariableSelector1_ButtonViewTable").click()

time.sleep(2)
driver.quit()
