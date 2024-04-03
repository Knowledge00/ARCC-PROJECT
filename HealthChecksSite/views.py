from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import numpy as np
import sys
import time
import os
import psycopg2
from datetime import date, datetime
from time import gmtime, strftime
from django.db import transaction, DatabaseError


# Create your views here.
host = "arcc-server.postgres.database.azure.com"
dbname = "arccdb"
user = "ZainR"
password = "ARCC123*!"
sslmode = "require"

# Construct connection string

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
print("Connection established")


def home(request):
    if request.method == "POST":
        Name = request.POST.get('Name')
        Postcode = request.POST.get('Postcode')
        Waist = request.POST.get('Waist')
        Weight = request.POST.get('Weight')
        Height = request.POST.get('Height')
        Sex = request.POST.get('gender')
        Ethnicity = request.POST.get('ethnicbg')
        Dia_hist = request.POST.get('historyDB')
        BP_hist= request.POST.get('bloodpressure')
        display_type = request.POST.get("colorCheckbox", None)
        birthDate = request.POST.get('DOB')
        GpSurgery = request.POST.get('Gpsurgery')
        consent = request.POST.get('consent')
        register_gp = request.POST.get('registerGP')
        birthDate = datetime.strptime(str(birthDate), "%Y-%m-%d")
        birth = datetime.strftime(birthDate, "%d/%m/%Y")
        bloodP = request.POST.get('BloodP')
        HeartRate = request.POST.get('HeartRate')
        Pulse = request.POST.get('Pulse')
        lipids_CHOL = request.POST.get('lipids CHOL')
        lipids_HDL = request.POST.get('lipids HDL')
        Lipids_CHOLHDL = request.POST.get('Lipids CHOL/HDL')
        HbA1c = request.POST.get('HbA1c')
        QRisk_Score= request.POST.get('Q-Risk Score')
        HC_name = "Zain"
        location = "hello"
        DateofHC = datetime.now().strftime("%Y-%m-%d")
        bmi_value = 16
        #bmi_value = WebScrape(Sex,Ethnicity,Dia_hist,Waist,Height,Weight,BP_hist,calculateAge(birth))
        risk = risk_score(Waist,calculateAge(birth),bmi_value,Sex,Ethnicity,Dia_hist,BP_hist)
        print(risk)
        #cursor.execute("INSERT INTO details (name, postcode, nameofgp, dob, ethnic, sex, time) VALUES (%s,%s,%s,%s,%s,%s,%s);",(Name,Postcode,GpSurgery,birth,Ethnicity,Sex,strftime("%H:%M", gmtime())))
        #conn.commit()
        if display_type in ["C"]:
            secondpartwebscrape(Name,consent,HC_name,DateofHC,location,Postcode,register_gp,GpSurgery,Sex,calculateAge(birth),Ethnicity,BP_hist,bmi_value,risk,bloodP,HeartRate,Pulse,"Yes",QRisk_Score,HbA1c,Lipids_CHOLHDL,lipids_HDL,lipids_CHOL)
        else:
            secondpartwebscrape(Name,consent,HC_name,DateofHC,location,Postcode,register_gp,GpSurgery,Sex,calculateAge(birth),Ethnicity,BP_hist,bmi_value,risk,bloodP,HeartRate,Pulse,"No",QRisk_Score,HbA1c,Lipids_CHOLHDL,lipids_HDL,lipids_CHOL)
    return render(request, "HealthChecksSite/HealthCheck.html")
def test(request):
    return render(request, "HealthChecksSite/test.html")
def calculateAge(birthDate):
    today = date.today()
    birth = datetime.strptime(birthDate, "%d/%m/%Y")
    age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    return age
def WebScrape(sex1,ethnicity1,dia_hist,waist,height,weight,bp_hist,age):
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    browser.get('https://riskscore.diabetes.org.uk/')
    #driver.maximize_window()
    wait = WebDriverWait(browser, 10)
    #consent_cb = sys.argv[2]
    #gp_register = sys.argv[9]


    ### COOKIES ###
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='onetrust-accept-btn-handler']"))).click()
    time.sleep(1) 
    ### START ###
    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='start-survey']"))).click()
    time.sleep(1) 

    ### SEX ###

    wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='%s']"%(sex1)))).click()
    time.sleep(1) 

    ### AGE ###
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="quiz_age"]'))).click()
    time.sleep(1) 
    age_box = browser.find_element(By.ID, "quiz_age")
    age_box.send_keys(age)

    browser.find_element(By.XPATH, "//button[@class='button next'][normalize-space()='Next']").click()
    time.sleep(1) 

    ### ETHNICITY ###
    wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='%s']"%(ethnicity1)))).click()
    time.sleep(1) 


    ### FIRST-ORDER DIABETIC ###
    wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='question current']//label[@class='button'][normalize-space()='%s']"%(dia_hist)))).click()
    time.sleep(1) 


    ### WAIST ###
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='quiz_waistMeasurementUnits_1']"))).click() #units
    time.sleep(1) 
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='quiz_waistCircumference']"))).click()
    time.sleep(1) 
    waist_value = browser.find_element(By.ID, "quiz_waistCircumference")
    waist_value.send_keys(waist)

    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='container with-diagram']//button[@class='button next'][normalize-space()='Next']"))).click()
    time.sleep(1) 


    ### BMI ###
    wait.until(EC.element_to_be_clickable((By.ID, "quiz_heightMeasurementUnits_1"))).click()
    time.sleep(1) 
    wait.until(EC.element_to_be_clickable((By.ID, "quiz_heightMeasurementPrimary"))).click()
    time.sleep(1) 
    p_height_value = browser.find_element(By.ID, "quiz_heightMeasurementPrimary")
    p_height_value.send_keys(height)


    wait.until(EC.element_to_be_clickable((By.ID, "quiz_weightMeasurementUnits_1"))).click()
    time.sleep(1) 
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='quiz_weightMeasurementPrimary']"))).click()
    time.sleep(1) 
    p_weight_value = browser.find_element(By.ID, "quiz_weightMeasurementPrimary")
    p_weight_value.send_keys(weight)

    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='bmi']")))
    bmi_value = browser.find_element(By.XPATH, "//input[@name='bmi']").get_attribute('value')
    print(bmi_value)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='result']//div//button[@class='button next'][normalize-space()='Next']"))).click()
    time.sleep(1) 

    ### HIGH BP ###
    wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='question current']//label[@class='button'][normalize-space()='%s']"%(bp_hist)))).click()
    time.sleep(1) 

    ### NO THANKS 
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'No thank you, take me to results')]"))).click()
    time.sleep(1) 


    return bmi_value

def risk_score(waist,age,bmi,gender,ethnicity,relativesdb,highbp):
    riskscore = 0
    if int(age) >= 50 and int(age) <= 59:
        riskscore += 5
    if int(age) >= 60 and int(age) <= 69:
        riskscore += 9
    if int(age) >= 70:
        riskscore += 13

    if gender == "Male":
        riskscore += 1

    if ethnicity != "White":
        riskscore += 6

    if relativesdb == "Yes":
        riskscore += 5

    if float(waist) >= 90 and float(waist) <= 99.9:
        riskscore += 4
    if float(waist) >= 100 and float(waist) <= 109.9:
        riskscore += 6
    if float(waist) >= 110:
        riskscore += 9

    if float(bmi) >= 25 and float(bmi) <= 29.9:
        riskscore += 3
    if float(bmi) >= 30 and float(bmi) <= 34.9:
        riskscore += 5
    if float(bmi) >= 35:
        riskscore += 8

    if highbp == "Yes":
        riskscore += 5
    return riskscore
def secondpartwebscrape(name,consent,HC_name,DateofHC,location,postcode,register_gp,GPName,sex,age,ethnic,highblood,bmi,riskscore,bloodP,HeartRate,Pulse,Required,QRisk_Score,HbA1c,Lipids_CHOLHDL,lipids_HDL,lipids_CHOL):
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    browser.get('https://forms.office.com/Pages/ResponsePage.aspx?id=Zcs4idCYjkKIQ-B0nIw7p_ufpSCFf91HtFqjffmCTtxUNzRVWU9ORVpORU45TzBEWjlETkM3UUZIOCQlQCN0PWcu')
    #driver.maximize_window()
    wait = WebDriverWait(browser, 10)
    #consent_cb = sys.argv[2]
    #gp_register = sys.argv[9]
    print(bloodP)


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
    temp.send_keys(riskscore)

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
    

    if Required == "Yes":
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[21]/div[2]/div/span/input"))).click() 
        temp = browser.find_element(By.XPATH, "//div[@id='question-list']/div[21]/div[2]/div/span/input")
        temp.send_keys(lipids_CHOL)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[22]/div[2]/div/span/input"))).click() 
        temp = browser.find_element(By.XPATH, "//div[@id='question-list']/div[22]/div[2]/div/span/input")
        temp.send_keys(lipids_HDL) 

        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[23]/div[2]/div/span/input"))).click() 
        temp = browser.find_element(By.XPATH, "//div[@id='question-list']/div[21]/div[2]/div/span/input")
        temp.send_keys(Lipids_CHOLHDL) 

        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[24]/div[2]/div/span/input"))).click() 
        temp = browser.find_element(By.XPATH, "//div[@id='question-list']/div[24]/div[2]/div/span/input")
        temp.send_keys(HbA1c) 

        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='question-list']/div[25]/div[2]/div/span/input"))).click() 
        temp = browser.find_element(By.XPATH, "//div[@id='question-list']/div[25]/div[2]/div/span/input")
        temp.send_keys(QRisk_Score) 
    #wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='form-main-content1']/div/div/div[2]/div[3]/div/button"))).click()
    time.sleep(10)
