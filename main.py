import requests
import json

addresses_api_path = "addressesapi.txt"

max_item_number = 100
min_loca_number = 3
default_loca = "US"
loca_colo: dict[str, list[str]] = {
    "HK": [
        "HK",
        "HKG",
    ],
    "JP": [
        "NRT",
        "KIX",
		"FUK",
		"OKA",
    ],
    "US": [
        "Default",
    ]
}


class Address:
	def __init__(self, ip, colo):
		self.ip = ip
		self.colo = colo

	def __str__(self):
		return f"{self.ip}#{self.colo}"

	def get_loca(self) -> str:
		for key, val in loca_colo.items():
			if self.colo in val:
				return key
		return default_loca


def get_sum(d: dict[str, list[Address]]) -> int:
	s = 0
	for v in d.values():
		s += len(v)
	return s

def include(d: dict[str, list[Address]], v: Address) -> bool:
	for val in d.values():
		if v in val:
			return True
	return False


data: list[Address] = []
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
			data.insert(0, new_address)
	else:
		print("Request Failed")
else:
	print("Request Failed")

# 去重 & save
index = 0
while index < len(data)-1:
	if data[index+1].ip == data[index].ip:
		print("Pop", str(data[index]))
		data.pop(index)
	else:
		index += 1

data_with_loca: dict[str, list[Address]] = {}
for l in loca_colo.keys():
	data_with_loca[l] = []
	for d in data:
		if d.get_loca() == l:
			data_with_loca[l].append(d)
		if len(data_with_loca[l]) >= min_loca_number:
			break

for d in data:
	if not include(data_with_loca, d):
		data_with_loca[d.get_loca()].append(d)
	if get_sum(data_with_loca) >= max_item_number:
		break

data = [j for i in data_with_loca.values() for j in i]

s = '\n'.join([str(i) for i in data])
print(s)

with open(addresses_api_path, 'w') as f:
	f.write(s)

print("Done")
