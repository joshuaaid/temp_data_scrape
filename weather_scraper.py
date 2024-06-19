from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import datetime

class WebScraper:
    def __init__(self, url):
        self.service = Service(executable_path='chromedriver.exe')
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome(service=self.service, options=self.browserProfile)
        self.url = url
        self.district_values = []
        self.month_values = []
        self.year_values = []
        self.temperature_data = []
        self.browser.get(self.url)
        time.sleep(3)

    def get_country(self):
        select_element = self.browser.find_element(By.ID, "sd_country")
        self.options = select_element.find_elements(By.TAG_NAME, "option")
        self.country_dict = {option.text: option.get_attribute('value') for option in self.options}

    def show_client_message_get_id(self):
        print("**********Zəhmət olmasa ölkəni siyahıdan seçin*******")
        for country, value in self.country_dict.items():
            print(f"{country}: {value}")
        while True:
            selected_id = input("Zəhmət olmasa nümunə ölkə id-ni daxil edin:")
            try:
                if selected_id in self.country_dict.values():
                    self.selected_id = selected_id
                    break
                else:
                    print("Daxil edilən məlumatda uyğunsuzluq var. Yenidən daxil edin!")
            except ValueError:
                print("Error!!!!")

    def get_districts(self):
        for option in self.options:
            if option.get_attribute('value') == self.selected_id:
                option.click()
                time.sleep(1)
        select_element = self.browser.find_element(By.ID, "sd_city")
        self.distr_options = select_element.find_elements(By.TAG_NAME, "option")
        self.district_values = [option.get_attribute('value') for option in self.distr_options]
       
    def get_month(self):
        select_element = self.browser.find_element(By.ID, "date_Month")
        self.month_options = select_element.find_elements(By.TAG_NAME, "option")
        self.month_values = [option.get_attribute('value') for option in self.month_options]
        

    def get_year(self):
        while True:
            selected_year = input("Zəhmət olmasa başlanğıc tarixi seçin (1997-2024):")
            try:
                selected_year = int(selected_year)
                if 1997 <= selected_year <= 2024:
                    self.begin_year = selected_year
                    break
                else:
                    print("Zəhmət olmasa 1997-2024 aralığında bir tarix daxil edin.")
            except ValueError:
                print("Xəta baş verdi! Zəhmət olmasa yenidən cəhd edin.")

        while True:
            selected_year = input("Zəhmət olmasa son tarixi seçin (1997-2024):")
            try:
                selected_year = int(selected_year)
                if 1997 <= selected_year <= 2024:
                    if selected_year < self.begin_year:
                        print("Son tarix başlanğıc tarixdən kiçik ola bilməz. Yenidən seçim edin!")
                    else:
                        self.end_year = selected_year
                        break
                else:
                    print("Zəhmət olmasa 1997-2024 aralığında bir tarix daxil edin.")
            except ValueError:
                print("Xəta baş verdi! Zəhmət olmasa yenidən cəhd edin.")            
        self.year_values = [str(year) for year in range(self.begin_year, self.end_year+1)]

        return self.year_values
    
    def get_temperature(self):

        i = 0
        for district in self.district_values:
            for year  in self.year_values:
                for month in self.month_values:
                    link = f"{self.url}/{district}/{year}/{int(month)}"
                    self.browser.get(link)
                    time.sleep(0.5)

                    select_district_element = self.browser.find_element(By.ID, "sd_city")
                    options = select_district_element.find_elements(By.TAG_NAME, 'option')

                    for option in options:
                        if option.get_attribute('selected'):
                            district_name = option.text

                    empty_elem = self.browser.find_elements(By.CSS_SELECTOR, 'center.empty_phrase label')

                    if empty_elem:
                        tem_info={}
                        tem_info['year'] = year
                        tem_info['month'] = month
                        tem_info['district'] = district_name
                        tem_info['no_data'] = 'yes'
                        tem_info['day'] = "N/A"
                        tem_info['temp_day'] = "N/A"
                        tem_info['temp_night'] = "N/A"
                        self.temperature_data.append(tem_info)
                    else:
                        data_rows = self.browser.find_elements(By.CSS_SELECTOR,'#data_block > table > tbody:nth-child(2)>tr')
                        for row in data_rows:
                            tem_info={}
                            tem_info['year'] = year
                            tem_info['month'] = month
                            tem_info['district'] = district_name
                            self.temperature_data.append(tem_info)
                            cells = row.find_elements(By.TAG_NAME,'td')
                            tem_info['no_data'] = 'no'
                            tem_info['day'] = cells[0].text
                            if cells[1].text.strip():
                                tem_info['temp_day'] = cells[1].text
                            else:
                                tem_info['temp_day'] = "N/A"
                            
                            if cells[6].text.strip():
                                tem_info['temp_night'] = cells[6].text
                            else:
                                tem_info['temp_night'] = "N/A"
        
            i = i+1
            print(f"{i} sayda rayon üzrə məlumatların toplanılması yekunlaşıb. Növbəti rayona keçid edilir....")

    def save_info(self):
        df = pd.DataFrame(self.temperature_data)
        df.to_excel(f"temperature_data.xlsx")

    def close_browser(self):
        self.browser.quit()

    def main():
        url = "https://www.gismeteo.ru/diary"
        data = WebScraper(url)
        data.get_year()
        data.get_country()
        data.show_client_message_get_id()
        data.get_districts()
        data.get_month()
        data.get_temperature()
        data.save_info()
        data.close_browser()

if __name__ == "__main__":
    WebScraper.main()
