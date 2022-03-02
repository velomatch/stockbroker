from Filereader import FileDataReader
from LiveStockUpdate import LiveStockUpdate

FileReader = FileDataReader()
UpdateStock = LiveStockUpdate()
datafilepath = 'data/ruislipStock.xlsx'
ConceptData,exceptions = FileReader.readxlsxdata(datafilepath)
UpdateStock.Updatelivestock(ConceptData[:3])