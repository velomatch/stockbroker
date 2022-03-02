from Filereader import FileDataReader
from LiveStockUpdate import LiveStockUpdate

FileReader = FileDataReader()
UpdateStock = LiveStockUpdate()
datafilepath = 'data/Bike Stock Levels Bespoke.csv'
BespokeData,exceptions = FileReader.readcsvdata(datafilepath)
UpdateStock.Updatelivestock(BespokeData[:3])