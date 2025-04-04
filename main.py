import requests
import json

addresses_api_path = "addressesapi.txt"

class Address:
	def __init__(self, ip, colo):
		self.ip = ip
		self.colo = colo

	def __str__(self):
		return f"{self.ip}#{self.colo}"


data = []
with open(addresses_api_path, 'r') as f:
 	for l in f.readlines():
		ip, colo = l.strip().split('#')
		data.append(Address(ip, colo))


# api
api = 'https://api.hostmonit.com/get_optimization_ip'
res = requests.post(api, json.dumps({
	"key": "iDetkOys"
}))
if res.status_code == 200:
	new_data = res.json()

	if new_data['code'] == 200:
		for d in new_data['info']:
			ip = d['ip']
			colo = d['colo']
			new_address = Address(ip, colo)
			data.append(new_address)
	else:
		print("Request Failed")
else:
	print("Request Failed")

# sort & 去重 & save
data.sort(key=lambda x: (x.colo, x.ip))

index = 0
while index < len(data)-1:
	if data[index+1].ip == data[index].ip:
		print("Pop", str(data[index]))
		data.pop(index)
	else:
		index += 1

s = '\n'.join([str(i) for i in data])
print(s)

with open(addresses_api_path, 'w') as f:
	f.write(s)

print("Done")
