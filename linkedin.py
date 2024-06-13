import time, math, random, os
import utils, constants, config
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from utils import prRed, prYellow, prGreen

class Linkedin:
    def __init__(self):
        browser = config.browser[0].lower()
        linkedinEmail = config.email
        linkedinPassword = config.password
        
        if browser == "firefox":
            if len(linkedinEmail) > 0:
                if platform.system() == "Linux":
                    prYellow("On Linux you need to define profile path to run the bot with Firefox. Go about:profiles find root directory of your profile paste in line 8 of config file next to firefoxProfileRootDir ")
                    exit()
                else:
                    self.driver = webdriver.Firefox()
                    self.login_linkedin(linkedinEmail, linkedinPassword)
            else:
                self.driver = webdriver.Firefox()
        elif browser == "chrome":
            self.driver = webdriver.Chrome()
            self.login_linkedin(linkedinEmail, linkedinPassword)

    def login_linkedin(self, email, password):
        self.driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
        prYellow("Trying to log in linkedin.")
        try:
            self.driver.find_element(By.ID, "username").send_keys(email)
            self.driver.find_element(By.ID, "password").send_keys(password)
            time.sleep(5)
            self.driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button').click()
        except Exception as e:
            prRed(e)

    def generateUrls(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        try:
            with open('data/urlData.txt', 'w', encoding="utf-8") as file:
                linkedinJobLinks = utils.LinkedinUrlGenerate().generateUrlLinks()
                for url in linkedinJobLinks:
                    file.write(url + "\n")
            prGreen("Urls are created successfully, now the bot will visit those urls.")
        except Exception as e:
            prRed(f"Could not generate url: {str(e)}. Make sure you have /data folder and modified config.py file for your preferences.")

    def linkJobApply(self):
        self.generateUrls()
        countApplied = 0
        countJobs = 0

        urlData = utils.getUrlDataFile()

        for url in urlData:
            self.driver.get(url)
            try:
                totalJobs = self.driver.find_element(By.XPATH, '//small').text
            except:
                print("No Matching Jobs Found")
                continue
            totalPages = utils.jobsToPages(totalJobs)

            urlWords = utils.urlToKeywords(url)
            lineToWrite = f"\n Category: {urlWords[0]}, Location: {urlWords[1]}, Applying {totalJobs} jobs."
            self.displayWriteResults(lineToWrite)

            for page in range(totalPages):
                currentPageJobs = constants.jobsPerPage * page
                pageUrl = f"{url}&start={currentPageJobs}"
                self.driver.get(pageUrl)
                time.sleep(random.uniform(1, constants.botSpeed))

                offersPerPage = self.driver.find_elements(By.XPATH, '//li[@data-occludable-job-id]')

                offerIds = [int(offer.get_attribute("data-occludable-job-id").split(":")[-1]) for offer in offersPerPage]

                for jobID in offerIds:
                    offerPage = f'https://www.linkedin.com/jobs/view/{jobID}'
                    self.driver.get(offerPage)
                    time.sleep(random.uniform(1, constants.botSpeed))

                    countJobs += 1

                    jobProperties = self.getJobProperties(countJobs)
                    button = self.easyApplyButton()

                    if button:
                        button.click()
                        time.sleep(random.uniform(1, constants.botSpeed))
                        countApplied += 1
                        self.submitApplication(jobProperties, offerPage)
                    else:
                        lineToWrite = f"{jobProperties} | * 🥳 Already applied! Job: {offerPage}"
                        self.displayWriteResults(lineToWrite)

            prYellow(f"Category: {urlWords[0]}, {urlWords[1]} applied: {countApplied} jobs out of {countJobs}.")

    def getJobProperties(self, count):
        properties = {
            "jobTitle": "//h1[contains(@class, 'job-title')]",
            "jobCompany": "//a[contains(@class, 'ember-view t-black t-normal')]",
            "jobLocation": "//span[contains(@class, 'bullet')]",
            "jobWorkPlace": "//span[contains(@class, 'workplace-type')]",
            "jobPostedDate": "//span[contains(@class, 'posted-date')]",
            "jobApplications": "//span[contains(@class, 'applicant-count')]"
        }

        jobDetails = [str(count)]
        for prop, xpath in properties.items():
            try:
                jobDetails.append(self.driver.find_element(By.XPATH, xpath).get_attribute("innerHTML").strip())
            except Exception as e:
                prYellow(f"Warning in getting {prop}: {str(e)[:50]}")
                jobDetails.append("")

        # Adding default job experience details
        experience = "Experience: 4 years | Previous Jobs: 1 | Current Job: 1"
        jobDetails.append(experience)

        return " | ".join(jobDetails)

    def easyApplyButton(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "jobs-apply-button")]'))
            )
        except Exception as e:
            prYellow(f"Easy apply button not found: {str(e)[:50]}")
            return False

    def submitApplication(self, jobProperties, offerPage):
        try:
            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
            time.sleep(random.uniform(1, constants.botSpeed))
            lineToWrite = f"{jobProperties} | * 🥳 Just Applied to this job: {offerPage}"
            self.displayWriteResults(lineToWrite)
        except:
            self.handleAdditionalSteps(jobProperties, offerPage)

    def handleAdditionalSteps(self, jobProperties, offerPage):
        try:
            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']").click()
            time.sleep(random.uniform(1, constants.botSpeed))
            comPercentage = self.driver.find_element(By.XPATH, 'html/body/div[3]/div/div/div[2]/div/div/span').text
            percenNumber = int(comPercentage.split("%")[0])
            result = self.applyProcess(percenNumber, offerPage)
            lineToWrite = f"{jobProperties} | {result}"
            self.displayWriteResults(lineToWrite)
        except Exception as e:
            prYellow(f"Additional steps failed: {str(e)[:50]}")
            lineToWrite = f"{jobProperties} | * 🥵 Cannot apply to this Job! {offerPage}"
            self.displayWriteResults(lineToWrite)

    def applyProcess(self, percentage, offerPage):
        applyPages = math.floor(100 / percentage)
        result = ""
        try:
            for _ in range(applyPages - 2):
                self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']").click()
                time.sleep(random.uniform(1, constants.botSpeed))

            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Review your application']").click()
            time.sleep(random.uniform(1, constants.botSpeed))

            if not config.followCompanies:
                self.driver.find_element(By.CSS_SELECTOR, "label[for='follow-company-checkbox']").click()
                time.sleep(random.uniform(1, constants.botSpeed))

            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
            time.sleep(random.uniform(1, constants.botSpeed))

            result = f"* 🥳 Just Applied to this job: {offerPage}"
        except Exception as e:
            prYellow(f"Apply process failed: {str(e)[:50]}")
            result = f"* 🥵 Couldn't apply to this job! Extra info needed. Link: {offerPage}"
        return result

    def displayWriteResults(self, lineToWrite: str):
        try:
            print(lineToWrite)
            utils.writeResults(lineToWrite)
        except Exception as e:
            prRed(f"Error in DisplayWriteResults: {str(e)}")


start = time.time()
while True:
    try:
        Linkedin().linkJobApply()
    except Exception as e:
        prRed(f"Error in main: {str(e)}")
        end = time.time()
        prYellow(f"---Took: {str(round((end - start)/60))} minute(s).")
        Linkedin().driver.quit()
