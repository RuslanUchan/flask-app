from xml.etree import ElementTree as et
import requests

# parse the file
doc = et.parse('cars.xml')

# test print
# print(doc.find('CAR/MODEL').text)
# print(doc.find('CAR[2]/MODEL').text)

# test loop
# for element in doc.findall('CAR'):
#     print(element.find('MAKE').text + ' ' +
#           element.find('MODEL').text +
#           ', $' + element.find('COST').text)

# test get request
xml = requests.get("http://www.w3schools.com/xml/cd_catalog.xml")

with open('w3.xml', 'wb') as code:
    code.write(xml.content)

doc = et.parse('w3.xml')

for element in doc.findall('CD'):
    print("Album: ", element.find('TITLE').text)
    print("Artist: ", element.find('ARTIST').text)
    print("Year: ", element.find('YEAR').text, '\n')
