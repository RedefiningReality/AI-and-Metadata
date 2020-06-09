# Features Mod
By: your one and only John Ford aka 2.0

(contrary to popular belief, this is not actually a Minecraft mod)

### Documentation:
`CSVReader()`

initialise with filename "features.csv"


`CSVReader(filename)`

initialise with custom filename


##### CSVReader Functions:

`update_csv(filename="features.csv")`

read from new csv file filename
	
	
`images(feature)`

get all images with feature
	(returns a list containing all images)
	
	
`feature(images)`

get all features for image
	(returns a list containing all features)


### Sample usage:
```
from featuresmod import CSVReader

# Creates new CSVReader with default filename "features.csv"
reader = CSVReader()

# Retrieves and prints list containing features for image cat.png
print(reader.features("cat.png"))

# Sets reader to read from csv file "cow.csv"
reader.update_csv("cow.csv")

# Retrieves and prints list containing images with feature fluffy
print(reader.images("fluffy"))
```
