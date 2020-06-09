from featuresmod import CSVReader

reader = CSVReader()
print(reader.features("cat.png"))
print(reader.images("caprify"))
print(reader.features("wow.png"))
print(reader.images("yowza"))
reader.update_csv("cow.csv")
print(reader.features("biotnehu"))
print(reader.images("doodly"))