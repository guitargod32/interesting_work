#currently this script can open window, login, either open print window or download incomplete html text, and logout
#After finishing we can place this as a resource in electron project and call it directly from JS

from selenium import webdriver 
from time import sleep 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options 

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



driver = webdriver.Chrome(ChromeDriverManager().install()) 

driver.get('https://www.bellevuecollege.edu/degreeaudit/')
print ("Opened page") 
sleep(1) 


#employee = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/main/main/div[3]/div/div/div/div[2]')

student = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/main/main/div[3]/div/div/div/div[1]/a')
student.click() 
print("on next page")

usr= input('Enter Student Id:') 
pin= input('Enter Pin:') 

def download_audit(usr, pin):
    username_box = driver.find_element_by_id('TB_ID') 
    username_box.send_keys(usr) 
    print ("Student Id entered") 
    sleep(1) 

    password_box = driver.find_element_by_id('TB_PIN') 
    password_box.send_keys(pin) 
    print ("Pin entered") 

    login_box = driver.find_element_by_id('B_Login') 
    login_box.click() 

    print ("Logged in") 

    sleep(1)
    #switch frame to work with drop box
    driver.switch_to.frame('stubtn')

    #select degree from dropdown
    #will need to deal with cohort too here
    cohort1 = False
    if cohort1:
        drop = driver.find_element_by_xpath("/html/body/form/table/tbody/tr[1]/td[2]/div/table/tbody/tr[2]/td[2]/select/option[74]")
        drop.click()
    else:
        drop = driver.find_element_by_xpath("//*[@id='LB_Program']/option[75]")
        drop.click()

    runbtn = driver.find_element_by_xpath("/html/body/form/table/tbody/tr[1]/td[2]/div/table/tbody/tr[2]/td[2]/input")
    runbtn.click()
    print("audit page reached, printing...")
    sleep(12)
    
    driver.switch_to.parent_frame()
    driver.switch_to.frame('stucont')
    
    openprintwindow = driver.find_element_by_xpath('/html/body/form/table[4]/tbody/tr/td[2]/a')
    openprintwindow.click()
    
    
    driver.switch_to.window(window_handle) 
    #driver.switch_to.window(driver.window_handles[-1])
    

    #this is xpath for save as pdf    //*[@id="destinationSelect"]//print-preview-settings-section[1]/div/select/option[2]


    
    
    
    option = driver.find_element_by_xpath('//*[@id="destinationSettings"]')
    option.click()
    
    #save = driver.find_element_by_xpath('//*[@id="destinationSelect"]//print-preview-settings-section[1]/div/select')
    #save.click()

    sleep(45)
    driver.switch_to.parent_frame()
    driver.switch_to.frame('header')
    logout=driver.find_element_by_xpath('/html/body/form/table/tbody/tr[1]/td[3]/a')
    logout.click()
    


"""

    html = browser.page_source


    this code downloads incomplete html,
    driver.get(url)
    with open('usr.html', 'w') as f:
        f.write(driver.page_source)
"""


#input('Press anything to quit') 
#driver.quit() 
#print("Finished") 
while True: #file with student id has next line
    
    #student = txt.split(',')
    # student[0] = usr 
    # student[1] = pin 
    #student[2] = yearflag #should this be 1
    download_audit(usr,pin)
    driver.quit()
    