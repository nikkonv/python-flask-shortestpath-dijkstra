import json

with open('talca_cl.json') as json_file:  
    data = json.load(json_file)
    for p in data['nodes']:
    	if p['y'] == '-35.4132794' and p['x'] =='-71.6586913':
    		street = p['id']
intersection = []
for s in data['links']:
	if s['source'] == street or s['target'] == street:
		try:
			intersection.append(s['name'])
		except:
			pass

print intersection[0]+' con '+ intersection[1]


for p in data['nodes']:
    	if p['id'] == "702785057":
    		print('yeah')