from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
from bs4 import BeautifulSoup as BSoup 
import logging
import json
import pandas as pd
# Author: Pakin Wirojwatanakul

# Max time out if element does not appear. 
TIME_OUT = 5

def create_well_info_by_api(driver, api):
    # Input: api of a well.
    # Returns a json containing all the information about that well.
    # More information about the json format can be found in the README.md file. 


    # Go to the api
    param = {'api':api}
    url = "https://secure.conservation.ca.gov/WellSearch/Details?"
    address = url + urllib.parse.urlencode(param)
    driver.get(address)
    # display all the oil and gas production data 
    driver.find_element_by_xpath("//select[@name='productionTable_length']/option[@value='-1']").click()
    
    # waits until all the data is displayed. Indicated by a disabled next button.
    try: 
        WebDriverWait(driver, TIME_OUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "li#productionTable_next.paginate_button.next.disabled")))
    except:
        logging.error("api list didn't load!") 

    # soupify html content    
    soup = BSoup(driver.page_source, 'html.parser')
          
    # WellInfo_APINumber
    element = soup.find("label", {"for": "WellInfo_APINumber"}).parent.text
    api_num = None if len(element.split()) <= 2 else element.split()[2]

    # WellInfo_LeaseName
    element = soup.find("label", {"for": "WellInfo_LeaseName"}).parent.text
    lease_name = None if len(element.split()) <= 1 else' '.join(element.split()[1:])
    
    # WellInfo_WellNumber
    element = soup.find("label", {"for": "WellInfo_WellNumber"}).parent.text
    well_num = None if len(element.split()) <= 2 else element.split()[2]

    # WellInfo_CountyName
    element = soup.find("label", {"for": "WellInfo_CountyName"}).parent.text
    country_name = None if len(element.split()) <= 1 else' '.join(element.split()[1:])

    # WellInfo_DistrictName
    element = soup.find("label", {"for": "WellInfo_DistrictName"}).parent.text
    district_num = None if len(element.split()) <= 1 else element.split()[1]

    # WellInfo_OperatorName
    element = soup.find("label", {"for": "WellInfo_OperatorName"}).parent.text
    operator_name = None if len(element.split()) <= 1 else' '.join(element.split()[1:])

    # WellInfo_FieldName
    element = soup.find("label", {"for": "WellInfo_FieldName"}).parent.text
    field_name = None if len(element.split()) <= 1 else' '.join(element.split()[1:])

    # WellInfo_AreaName
    element = soup.find("label", {"for": "WellInfo_AreaName"}).parent.text
    area_name = None if len(element.split()) <= 1 else' '.join(element.split()[1:])

    # WellInfo_Section
    element = soup.find("label", {"for": "WellInfo_Section"}).parent.text
    section_num = None if len(element.split()) <= 1 else element.split()[1]
 
    # WellInfo_Township
    element = soup.find("label", {"for": "WellInfo_Township"}).parent.text
    township_num = None if len(element.split()) <= 1 else element.split()[1]

    # WellInfo_Range
    element = soup.find("label", {"for": "WellInfo_Range"}).parent.text
    range_num = None if len(element.split()) <= 1 else element.split()[1]

    # WellInfo_BaseMeridian
    element = soup.find("label", {"for": "WellInfo_BaseMeridian"}).parent.text
    base_meridian_num = None if len(element.split()) <= 2 else element.split()[2]
    
    # WellInfo_WellStatusCode
    element = soup.find("label", {"for": "WellInfo_WellStatusCode"}).parent.text
    well_status = None if len(element.split()) <= 2 else element.split()[2]

    # WellInfo_WellType
    element = soup.find("label", {"for": "WellInfo_WellType"}).parent.text
    well_type = None if len(element.split()) <= 2 else element.split()[2]
   
    # WellInfo_SPUDDate
    element = soup.find("label", {"for": "WellInfo_SPUDDate"}).parent.text
    spud_date = None if len(element.split()) <= 2 else element.split()[2]
    
    # WellInfo_GISSourceCode
    element = soup.find("label", {"for": "WellInfo_GISSourceCode"}).parent.text
    gis_source = None if len(element.split()) <= 2 else element.split()[2]

    # WellInfo_DatumCode
    element = soup.find("label", {"for": "WellInfo_DatumCode"}).parent.text
    datum = None if len(element.split()) <= 1 else element.split()[1]
   
    # WellInfo_Latitude
    element = soup.find("label", {"for": "WellInfo_Latitude"}).parent.text
    latitude = None if len(element.split()) <= 1 else element.split()[1]

    # WellInfo_Longitude
    element = soup.find("label", {"for": "WellInfo_Longitude"}).parent.text
    longitude = None if len(element.split()) <= 1 else element.split()[1]

    # collects all the oil and gas information production.
    # format = (date, Oil(bbl), Gas(Mcf))
    oil_gas_production = []
    for row in soup.find(id="productionTable").find("tbody").find_all("tr",{"role":"row"}):
        td_list = row.find_all("td")
        date = td_list[0].text
        oil_prod = td_list[1].text
        gas_prod = td_list[3].text      
        if "/" in date:
            oil_prod = oil_prod.replace(',', '')
            oil_prod = None if len(oil_prod) < 1 else int(oil_prod)
            gas_prod = gas_prod.replace(',', '')
            gas_prod = None if len(gas_prod) < 1 else int(gas_prod)
            oil_gas_production.append((date,oil_prod,gas_prod))

    well_info = {
        "api_num":api_num,
        "lease_name":lease_name,
        "well_num":well_num,
        "country_name":country_name,
        "district_num":district_num,
        "operator_name":operator_name,
        "field_name":field_name,
        "area_name":area_name,
        "section_num":section_num,
        "township_num":township_num,
        "range_num":range_num,
        "base_meridian_num":base_meridian_num,
        "well_status":well_status,
        "well_type":well_type,
        "spud_date":spud_date,
        "gis_source":gis_source,
        "datum":datum,
        "latitude":latitude,
        "longitude":longitude,
        "oil_gas_production":oil_gas_production
        }

    return well_info

# get a list of all the well apis from the exported csv file.
df = pd.read_csv("exported.csv")
api_list = df['Formatted API #'].values


def scrape(thread_name, start_idx, end_idx):
    """
    Description: The script reads the `exported.csv` file and extracts a list of well apis. Then it scrapes the well apis from the extracted well api list starting from `start_idx` (inclusive) and ending in `end_idx` (exclusive). The script returns a list of json objects with the well and production data ( the data format will be discussed in a bit). The list of json is named  `well_info_{start_idx}_{end_idx}.json` and is dumped as a json file in the directory `./well_info_jsons_threaded`.  

    For more information please refer to the READ.md file. 
    """

    logging.info('%s: Starting...' % thread_name)

    # create incognito chrome driver
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    option.add_argument("headless")
    driver = webdriver.Chrome(executable_path='./chromedriver', options=option)


    # list containing all the information about a well including the oil and gas production data of the well.
    all_well_info = []

    # loops through the api_list starting from index start_idx till index end_idx.
    for idx, api in enumerate(api_list[start_idx:end_idx]):
        api = str(api)
        logging.info("%s, idx: %s" % (thread_name, str(idx)))
        logging.info("%s, api: %s" % (thread_name, api))
        api = api.replace('-','')
        # scrapes the api and appends the information to all_well_info.
        all_well_info.append(create_well_info_by_api(driver, api))


    driver.quit()

    # writes the output to json file.
    exported_file_name = "./well_info_jsons_threaded/well_info_{}_{}.json".format(start_idx, end_idx)
    with open(exported_file_name, 'w') as outfile:
        json.dump(all_well_info, outfile)

    logging.info('%s: Exiting...' % thread_name)
   