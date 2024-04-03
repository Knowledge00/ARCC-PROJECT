from django.test import TestCase
from datetime import date, datetime
import datetime
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from time import gmtime, strftime
import time
# Create your tests here.
name = "hello"
consent  = "No"
hcname = "Zain"
DateofHC = "11/01/2024"
Location = "Penge"
Postcode = "SE207SP"
register_gp = "No"
gpname = "Parkpractice"
sex = "Male"
age = 65
ethnic = "South Asian"
highblood = "Yes"
bmi = 26.7
risk_score = 10
bloodP = "100/76"
HeartRate = 76
pulse = "Regular"
def secondpartwebscrape(name,consent,HC_name,DateofHC,location,postcode,register_gp,GPName,sex,age,ethnic,highblood,bmi,risk_score,bloodP,HeartRate,Pulse):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    browser.get('https://forms.office.com/Pages/ResponsePage.aspx?id=Zcs4idCYjkKIQ-B0nIw7p_ufpSCFf91HtFqjffmCTtxUNzRVWU9ORVpORU45TzBEWjlETkM3UUZIOCQlQCN0PWcu')
    #driver.maximize_window()
    wait = WebDriverWait(browser, 10)
    #consent_cb = sys.argv[2]
    #gp_register = sys.argv[9]



    ### NAME ###
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div/div[2]/div/span/input"))).click()
    time.sleep(1) 
    temp = browser.find_element(By.XPATH, "//div[@id='question-list']/div/div[2]/div/span/input")
    temp.send_keys(name)

    ### CONSENT ## 
    if consent == "Yes":
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[2]/div[2]/div/div/div/div/label"))).click()
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[2]/div[2]/div/div/div[2]/div/label"))).click()
    time.sleep(1) 

    ### NAME OF HEALTH CHAMPTION ###
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[4]/div[2]/div/span/input"))).click() #units
    ##########time.sleep(1)  
    temp = browser.find_element(By.XPATH, "//div[@id='question-list']/div[4]/div[2]/div/span/input")
    temp.send_keys(HC_name)

    ### DATE OF HEALTHCHECK ###
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[5]/div[2]/div/div/div/div/div/input"))).click() #units
    ##########time.sleep(1)  
    temp = browser.find_element(By.XPATH, "//div[@id='question-list']/div[5]/div[2]/div/div/div/div/div/input")
    temp.send_keys(DateofHC)

    ### LOCATION OF HEALTHCHECK ###
    ##########time.sleep(1) 
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[6]/div[2]/div/span/input"))).click()
    ##########time.sleep(1) 
    temp = browser.find_element(By.XPATH, "//div[@id='question-list']/div[6]/div[2]/div/span/input")
    temp.send_keys(location)

    ### PHONE NUMBER ###
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[7]/div[2]/div/span/input"))).click()
    ##########time.sleep(1) 
    temp = browser.find_element(By.XPATH, "//div[@id='question-list']/div[7]/div[2]/div/span/input")
    temp.send_keys(".")

    ### EMAIL ### 
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[8]/div[2]/div/span/input"))).click()
    ##########time.sleep(1) 
    temp = browser.find_element(By.XPATH, "//div[@id='question-list']/div[8]/div[2]/div/span/input")
    temp.send_keys(".")

    ### POSTCODE ### 
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[9]/div[2]/div/span/input"))).click()
    ##########time.sleep(1) 
    temp = browser.find_element(By.XPATH, "//div[@id='question-list']/div[9]/div[2]/div/span/input")
    temp.send_keys(postcode)

    ### REGISTERED CROYDON GP ### 
    if register_gp == "Yes":
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[10]/div[2]/div/div/div/div/label"))).click()
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[10]/div[2]/div/div/div[2]/div/label"))).click()

    ### POSTCODE ### 
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[11]/div[2]/div/span/input"))).click()
    ##########time.sleep(1) 
    temp = browser.find_element(By.XPATH, "//div[@id='question-list']/div[11]/div[2]/div/span/input")
    temp.send_keys(GPName)

    ### SEX ### 
    if sex == "Female":
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[12]/div[2]/div/div/div/div/label"))).click()
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[12]/div[2]/div/div/div[2]/div/label"))).click()

    ### AGE ### 
    if age <= 30:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[13]/div[2]/div/div/div/div/label"))).click()
    if age >= 31 and age <= 40:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[13]/div[2]/div/div/div[2]/div/label"))).click()
    if age >= 41 and age <= 50:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[13]/div[2]/div/div/div[3]/div/label"))).click()
    if age >= 51 and age <= 60:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[13]/div[2]/div/div/div[4]/div/label"))).click()
    if age >= 61 and age <= 70:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[13]/div[2]/div/div/div[5]/div/label"))).click()
    if age >= 71 and age <= 80:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[13]/div[2]/div/div/div[6]/div/label"))).click()
    if age >= 81 and age <= 90:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[13]/div[2]/div/div/div[7]/div/label"))).click()
    if age >= 91:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[13]/div[2]/div/div/div[8]/div/label"))).click()
    
    ### ETHNIC ###

    if ethnic == "South Asian":
        wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(.,'South Asian')]"))).click()
    if ethnic == "Black":
        wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(.,'Black')]"))).click()
    if ethnic == "Chinese":
        wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(.,'Chinese')]"))).click()
    if ethnic =="Mixed Ethnicity":
        wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(.,'Mixed Ethnicity')]"))).click()
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(.,'White')]"))).click()
    
    ### HIGH BLOOD PRESSURE ### 
    if highblood == "Yes":
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[16]/div[2]/div/div/div/div/label"))).click()
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[16]/div[2]/div/div/div[2]/div/label"))).click()

    ### BMI ### 
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[17]/div[2]/div/span/input"))).click()
    ##########time.sleep(1) 
    temp = browser.find_element(By.XPATH, "//div[@id='question-list']/div[17]/div[2]/div/span/input")
    temp.send_keys(bmi)
    
    ### RISK SCORE ###
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[18]/div[2]/div/span/input"))).click()
    ##########time.sleep(1) 
    temp = browser.find_element(By.XPATH, "//div[@id='question-list']/div[18]/div[2]/div/span/input")
    temp.send_keys(risk_score)

    ### BLOODPRESURE ###
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[19]/div[2]/div/span/input"))).click()
    ##########time.sleep(1) 
    temp = browser.find_element(By.XPATH, "//div[@id='question-list']/div[19]/div[2]/div/span/input")
    temp.send_keys(bloodP)

    ### RESTING HEART RATE ###
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[20]/div[2]/div/span/input"))).click()
    ##########time.sleep(1) 
    temp = browser.find_element(By.XPATH, "//div[@id='question-list']/div[20]/div[2]/div/span/input")
    temp.send_keys(HeartRate)

    ### FULL ADDRESS ###
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[27]/div[2]/div/span/input"))).click()
    ##########time.sleep(1) 
    temp = browser.find_element(By.XPATH, "//div[@id='question-list']/div[27]/div[2]/div/span/input")
    temp.send_keys(".")

    ### PULSE ###
    if Pulse == "Regular":
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[28]/div[2]/div/div/div/div/label"))).click()
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[28]/div[2]/div/div/div[2]/div/label"))).click()    
    
    
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[29]/div[2]/div/div/div[5]/div/label"))).click()
    
    #wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='form-main-content1']/div/div/div[2]/div[3]/div/button"))).click()
    time.sleep(10)



    #return #bmi_value


secondpartwebscrape(name,consent,hcname,DateofHC,Location,Postcode,register_gp,gpname,sex,age,ethnic,highblood,bmi,risk_score,bloodP,HeartRate,pulse)