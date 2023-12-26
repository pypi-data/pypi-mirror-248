import re

from rich import print

class Validation(object):
    def __init__(self) -> None:
        pass

    def is_valid_phone(self, phone_number: str) -> str:
        pattern = re.compile('^\+\d{1,}-?\d{1,}-?\d{1,}$')

        #dicocokan dengan regex
        match = pattern.match(phone_number)

        # Cek apakah nomor telepon cocok dengan pola regex
        if re.match(pattern, phone_number):
            return True
        else:
            return False
        
    def is_valid_pages_number(self, page_number: str) -> int:
        matches = re.findall(r'\d+', page_number)
        #return bool(matches.match(str(page_number)))
    
        if matches:
            result = int(matches[0])
            print("Extracted Page Number :", result)
            return result
        else:
            raise Exception(matches)
