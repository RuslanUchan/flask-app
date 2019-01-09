import json

# decode json
output = json.load(open('cars.json'))

# display output
print(output)

# change the looks
print(json.dumps(output, indent=4, sort_keys=True))

# display one json output
print(output['CARS'][0]['MODEL'])
