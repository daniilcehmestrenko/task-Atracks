import os
import re
import requests
import logging

from bs4 import BeautifulSoup
from django.conf import settings


class FileManager:
    MEDIA_PATH = settings.MEDIA_ROOT + '/uploads'
    FILES_URL = settings.FILES_URL

    def remove_files_from_media(self) -> bool:
        try:
            if os.path.exists(self.MEDIA_PATH):
                for file in os.listdir(self.MEDIA_PATH):
                    os.remove(os.path.join(self.MEDIA_PATH, file))
                return True
            else:
                return True

        except FileNotFoundError:
            return True

        except Exception as err:
            logging.info(f'error - {str(err)}')
            return False

    def remove_file(self, file_name: str):
        os.remove(file_name)

    def create_files(self) -> list:
        files_data = list()
        response = requests.get(self.FILES_URL, verify=False)

        soup = BeautifulSoup(response.text, 'html.parser')
        tags = soup.find_all('a', {'class': 'text-primary-500 hover:text-primary-600'})

        links = [tag.attrs['href'] for tag in tags]
        for link in links:
            try:
                file_name = re.findall(r'\w+-\w+.csv', link.split('/')[-1])[-1]
                code = re.findall(r'\d', file_name)[-1]

                r = requests.get(link, verify=False)
                with open(file_name, 'wb') as file:
                    file.write(r.content)

                files_data.append((file_name, code))
            
            except Exception as err:
                logging.info(f'error - {str(err)}')

        return files_data
