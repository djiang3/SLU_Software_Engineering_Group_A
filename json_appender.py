import json
import sys

if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print "Format arguments as two json files. The second file will be appended to the first and saved as the first file."
        exit()
jsonFile1 = open(sys.argv[2])
jsonFile2 = open(sys.argv[3])

jsonString1 = jsonFile1.read()
jsonString2 = jsonFile1.read()

jsonFile2.close()

jsonData1 = json.loads(jsonString1)
jsonData2 = json.loads(jsonString2)

for jsonDict in jsonData2:
    jsonData1.append(jsonDict)
    
jsonString1 = json.dumps(jsonData1)

jsonFile1.seek(0)
jsonFile1.write(jsonString1)
jsonFile1.close()

exit()