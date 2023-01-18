import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


class IndeedBot:
    def __init__(self):
        """
        Initializes the Chrom webdriver.
        Sets the job search query string

        self.driver: sel
        """

        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.query_string = "https://www.indeed.com/jobs?q={job}&l={city}%2C+{state}"
        self.jobs = []
        self.indeed_apply_jobs = []

    def nav(self, url):
        self.driver.get(url)
        time.sleep(3)

    def __convert_query(self, job, city, state):
        """
        Reformats the query for expected syntax of the search

        Args:
            job: str -> Job type to search for
            city: str -> City location for the job
            state: str -> State location for the job

        Returns:
            job: str
            city: str
            state: str
        """

        job = '+'.join(job.split(" "))
        city = city.lower()

        # State must be valid two letter code
        if len(state) != 2:
            raise Exception("State must be valid two letter code.")
        state = state.upper()

        return job, city, state

    def query(self, job, city, state):
        """
        Searches Indeed for a job in a given city and state

        Args:
            job: str -> Job type to search for
            city: str -> City location for the job
            state: str -> State location for the job
        """
        job, city, state = self.__convert_query(job, city, state)

        query = self.query_string.format(job=job, city=city, state=state)

        self.nav(query)

    def find_indeed_apply_jobs(self):
        """
        Called after chromedriver Chrome  instance navigates to job search results.
        """

        self.jobs = self.driver.find_elements(
            By.CLASS_NAME, "shelfItem indeedApply")

        print(f'Number of jobs {len(self.jobs)}')

        for job in self.jobs:
            try:  # Indeed apply indicator
                job.find_element(By.CLASS_NAME, "shelfItem indeedApply")
                self.indeed_apply_jobs.append(job)
            except:  # Job is not Indeed apply
                pass

    def apply_to_indeed_apply_jobs(self, profile):
        """
        Extracts jobs with Indeed apply

        Args:
            profile: dict
        """

        print(f'Number of Indeed apply jobs {len(self.indeed_apply_jobs)}')

        for job in self.indeed_apply_jobs:
            self.__process_job(job)
            self.__process_apply_button()
            self.__fill_applicant_form(profile)

            self.driver.find_element(By.ID, "form-action-continue").click()

    def __process_apply_button(self):
        apply_button = self.driver.find_element(By.ID, "indeedApplyButton")
        apply_button.click()
        time.sleep(3)

    def __process_job(self, job):
        """
        Refines url of job posting and navigates to it

        Args:
            job:Selenium.Webdriver.Chrome.WebElement
        """

        job_a_tag = job.find_element(By.TAG_NAME, "a")
        job_href = job_a_tag.get_attribute("href")
        # Remove all extraneous indeed url query string parameters
        job_href = job_href.split("&from")[0]
        self.nav(job_href)

    def __fill_applicant_form(self, profile):
        """
        Finds elements on the applicant form

        Args:
            profile: dict
        """

        actions = ActionChains(self.driver)
        actions.send_keys(profile['name'] + Keys.TAB +
                          profile['email'] + Keys.TAB +
                          profile['phone_number'] + Keys.TAB)
        actions.perform()


if __name__ == '__main__':

    profile = {
        'name': "Colby Leed",
        'email': "colbyleed@yahoo.com",
        'phone_number': "206-538-7716",
        'resume': os.getcwd() + '\\resume.txt'
    }
    id_bot = IndeedBot()

    id_bot.query("java developer", "seattle", "wa")

    id_bot.find_indeed_apply_jobs()

    id_bot.apply_to_indeed_apply_jobs(profile)
