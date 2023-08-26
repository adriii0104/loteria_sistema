import requests
from bs4 import BeautifulSoup
import time

def hour_rd():
        url = "https://www.worldtimeserver.com/hora-exacta-DO.aspx"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            html_content = response.text
        
            soup = BeautifulSoup(html_content, 'html.parser')
        
            params_for_hour = 'fontTS'
        
            h2_element = soup.find('span', class_=params_for_hour)
        
            if h2_element is not None and h2_element.text:
                hora_rd = h2_element.text.split()[0]  # Get the first element from the list
                return hora_rd
            else:
                return("Time element not found on the webpage.")
        else:
            return("Failed to retrieve the webpage. Status code:", response.status_code)
        

