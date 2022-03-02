from cmath import nan
import pandas as pd
from datetime import datetime
import csv
import re

class FileDataReader(object):
    
    def __init__(self):

        self.invalidskuregex = re.compile('[@_!#$%^&*()<>?|}{~]')
        pass
    
    #Todo if productcode length is > 32 should it be sliced to 32?
    #what type of data to be sent to the API list of dict or a dataframe?
    def readxlsxdata(self,src):

        exceptions = []
        df = pd.read_excel(src)
        # dtype={'<field1>': str, '<field2>': int,'<field3>':int}
        processed_data = df.to_dict('records')
        exempted_codes = [0.0,]
        cleaned_data = []
        
        for index,value in enumerate(processed_data):

            # exempting 0.0 from the product codes
            if value['Product Code'] not in exempted_codes:

                # validating the type of productcode to string and removing empty spaces
                if isinstance(value['Product Code'], str):
                    product_code = str(value['Product Code']).strip()                        
                elif isinstance(value['Product Code'], float):
                    product_code = str(value['Product Code']).strip()
                else:
                    product_code = str(value['Product Code'])
                    exceptions.append((index,value['Product Code']))
                    print(f'exception - {product_code}, @ cell - {index}, expected type str but found type {type(df.loc[index,"Product Code"])}')

                # checking for special characters in
                if self.invalidskuregex.search(product_code) == None :
                    # processed_data[index]['stockKeepingUnit'] = product_code
                    # processed_data[index]['stock'] = value['Stock_Level']
                    # processed_data[index]['On Order'] = value['On Order']
                    cleaned_data.append({'stockKeepingUnit':product_code,'stock':value['Stock_Level'],'On Order':value['On Order']})
                else:
                    print('found special character in sku.',product_code)
            else:
                exceptions.append((index,value['Product Code']))
        print(f'Total invalid data - {len(exceptions)}')
        return cleaned_data,exceptions

    def readcsvdata(self, src):
        exceptions = []
        with open(src, newline='\n') as vendFile:
            lines = 0
            vendReader = csv.DictReader(vendFile)
            vendReader = list(vendReader)
            for index,value in enumerate(vendReader):
                vendReader[index]['stockKeepingUnit'] = value["supplier_code"]
                vendReader[index]['stock'] = value["inventory_Gresham_Street"]
        return vendReader,exceptions