import requests
import json
import pprint

class LiveStockUpdate(object):

    def __init__(self):
        self.facilityID = "e3a9f238-5dbf-4a7c-9a49-4bcc8c7b766a"
        self.endpointID = "82ea97f5-e586-498f-8183-6311d25b7545"
        self.productVariantURL = 'http://127.0.0.1:8000/api/v1/productvariant/'
        self.stockReportURL = 'http://127.0.0.1:8000/api/v1/stockreport/'

    def GetProductVariants(self):
        print("Loading Database Dictionary")
        responseRaw = requests.get(url=self.productVariantURL)
        responseRaw.raise_for_status()

        if (responseRaw.headers['Content-Type'] != 'application/json'):
            raise ValueError("Response header not json.")

        print("Importing existing product variants.")

        responseContent = responseRaw.content
        responseJson = json.loads(responseContent)
        print(responseJson,' responsejson')
        curProductVariants = {}

        for productVariantJson in responseJson['results']:
            productVariant = {}
            sku = ""

            for k, v in productVariantJson.items():
                print(k,v)
                productVariant[k] = v

                if (k == "stockKeepingUnit"):
                    sku = v

            curProductVariants[sku] = productVariant
        
        return curProductVariants

    def AddStockReport(self, stockReportURL, stockKeepingUnit, stock, ProductvariantID=''):

        postJson = {
            "product_sku":stockKeepingUnit,
            "stock_units": stock
        }

        post = requests.post(stockReportURL, json=postJson)
        if ((post.status_code < 200) or (post.status_code > 299)):
            print("\tUnexpected response from Stock Report productVariantID: " + stockKeepingUnit)

            response = post.json()
            pprint.pprint(response)
            post.raise_for_status()    

        return 'success'

    def Addstock(self, data):
        self.availableproductvariants = self.GetProductVariants()
        validLines = 0
        productsWithStock = 0
        totalStock = 0
        totalLines = len(data)
        lines = 0
        for index,row in enumerate(data):
            stockKeepingUnit = row["stockKeepingUnit"]
            if (len(stockKeepingUnit) != 0):
                try:
                    stock = int(row["stock"])
                    print(stock,' - ',stockKeepingUnit)
                    if stockKeepingUnit in self.availableproductvariants:
                        prodvariantid = self.availableproductvariants[stockKeepingUnit]["productVariantID"]
                        self.AddStockReport(self.stockReportURL, stockKeepingUnit, stock, prodvariantid )
                    else:
                        self.AddStockReport(self.stockReportURL, stockKeepingUnit, stock)
                    validLines = validLines + 1
                    if (stock > 0):
                        productsWithStock = productsWithStock + 1
                        totalStock = totalStock + stock
                except ValueError:
                    print("\tStock value (" + row["stock"] + ") invalid for SKU: " + stockKeepingUnit)
                
                except KeyError:
                    pass

            lines = lines + 1

            if ((lines % 100) == 0):
                print("Processed " + str(round((lines/totalLines) * 100)) + "% " + str(lines) + "/" + str(totalLines))


    def Updatelivestock(self, data):
        unprocessed_data = []       
        try:
            addstock_res = self.Addstock(data)
        except Exception as e:
            print('exception Raised while Adding Stock')
        return unprocessed_data
