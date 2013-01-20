import csv, json


def main():
	with open("/Users/Andrew/Desktop/classes.csv", 'rU') as rfile:
		with open("/Users/Andrew/Desktop/fields.csv", 'rU') as rfile2:
			freader = csv.reader(rfile2)
			fields = {}
			for line in freader:
				fields[line[0]] = [line[1], 0 ]
			
		reader = csv.reader(rfile)
		
		already_recorded = []
		
		data = []
		for line in reader:
			title = fields[line[0]][0] + ' ' + line[1] + ': '+line[2]
			if title not in already_recorded:
				
				fields[line[0]][1]+=1
				
				url = '/courses/%s/%s/' % (line[0], line[1])
				data.append( {'full_title': title,'title':line[2], 'url': url} )
				already_recorded.append(title)
			
		wfile = open("/Users/Andrew/Desktop/courses.json", 'w')
		wfile.write(json.dumps(data))
		wfile.close()
		
		data = []
		for field in fields.keys():
			data.append({'short': field, 'long':fields[field][0], 'n':fields[field][1]})
		wfile = open("/Users/Andrew/Desktop/fields.json", 'w')
		wfile.write(json.dumps(data))
		wfile.close()
		
		
		
main()			
		