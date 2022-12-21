import json

# with open("config.json", "r") as jsonfile:
#     data = json.load(jsonfile)
#     print("Read successful")
# print(data)
# print(data['DATABASE_NAME'])

cf = open('config.conf')
conf = cf.read()
print(conf)

cf_dict = json.loads(conf)

print(cf_dict)
print(cf_dict['INPUT_PATH'])