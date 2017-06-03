from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import csv

chrome_path = r"/Users/Lenny/Downloads/chromedriver"
driver = webdriver.Chrome(chrome_path)

# Going to CTEC login page
driver.get("https://websso.it.northwestern.edu/amserver/UI/Login?goto=https%3A%2F%2Fcaesar.ent.northwestern.edu%3A443%2Fpsp%2Fs9prod%2F%3F%26cmd%3Dstart")

driver.implicitly_wait(2)

# Login
username_path = driver.find_element_by_css_selector("input#IDToken1")
password_path = driver.find_element_by_css_selector("input#IDToken2")
login_path = driver.find_element_by_name("Login.Submit")

username_path.send_keys("dsf")
password_path.send_keys("asdf!!")
login_path.submit()

####### Duo Mobile should be done manually
path = driver.find_element_by_name('Login.Submit')
path.click()

# Go into CTEC
driver.get("https://caesar.ent.northwestern.edu/psp/s9prod/EMPLOYEE/HRMS/c/NWCT.NW_CT_PUBLIC_VIEW.GBL?PORTALPARAM_PTCNAV=NW_CT_PUBLIC_VIEW_GBL&EOPP.SCNode=HRMS&EOPP.SCPortal=EMPLOYEE&EOPP.SCName=NWCT&EOPP.SCLabel=Course%20and%20Teacher%20Evaluations&EOPP.SCPTfname=NWCT&FolderPath=PORTAL_ROOT_OBJECT.NWCT.NW_CT_PUBLIC_VIEW_GBL&IsFolder=false")

driver.implicitly_wait(5)

# Select Academic Career / Subject
driver.switch_to_frame("TargetContent")
driver.implicitly_wait(1)
select_form = Select(driver.find_element_by_id("NW_CT_PB_SRCH_ACAD_CAREER"))
select_form.select_by_value('UGRD')
driver.implicitly_wait(3)

# Collect all subjects
subjects = []
select_form = driver.find_element_by_id("NW_CT_PB_SRCH_SUBJECT")
for option in select_form.find_elements_by_tag_name("option"):
  driver.implicitly_wait(3)
  value = option.get_attribute("value")
  value = value.encode('ascii', 'ignore')
  print("value: ", value)
  subjects.append(value)


print("subjects: \n", subjects)
subjects = subjects[1:]

select_form = Select(driver.find_element_by_id("NW_CT_PB_SRCH_SUBJECT"))
driver.implicitly_wait(1)
select_form.select_by_value(subjects[3])

# click Search by Course
path = driver.find_element_by_name('NW_CT_PB_SRCH_NW_CTEC_SRCH_CHOIC$10$')
path.click()

# click Search
path = driver.find_element_by_name('NW_CT_PB_SRCH_SRCH_BTN')
path.click()
driver.implicitly_wait(1)

# Get the table that shows all courses
path = driver.find_element_by_xpath('//*[@id="NW_CT_PV_DRV$scroll$0"]/tbody')
courses = path.find_elements_by_tag_name('tr')
link = courses[1].find_element_by_tag_name('a')

# Get the table that shows all quarters of selected course
for course in courses[1:]:
  link = course.find_element_by_tag_name('a')
  link.click()
  driver.implicitly_wait(2)
  tables = driver.find_elements_by_class_name('PSLEVEL1GRIDNBO')
  for quarter in tables[:-1]:
    course_links = quarter.find_elements_by_tag_name('a')
    courses_window = driver.current_window_handle
    for link in course_links[3:]:
      link.click()
      handle = driver.window_handles[1]
      driver.switch_to_window(handle) # now inside the CTEC review
      driver.switch_to_frame("TargetContent")
      prof_name = driver.find_element_by_css_selector('.PSEDITBOX_DISPONLY#NW_CT_PV_NAME_NAME')
      prof_name = prof_name.text.encode('ascii', 'ignore')
      path = driver.find_element_by_xpath('//*[@id="win16divNW_CT_PV3_DRV_DESCRLONG$0"]/div/p/font')
      review = path.text.encode('ascii', 'ignore') # professor name & reviews selected
      data = [prof_name, review]
      with open('reviews.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)



















