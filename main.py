from __future__ import print_function
import sys


from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
import json_graph as graph



app = Flask(__name__)
import json

@app.route("/draw_nodes")
def draw_nodes():
    talca_graph=graph.json_graph('static/talca_cl.json')
    return talca_graph.draw_nodes()

@app.route("/draw_graph")
def draw_graph():
    talca_graph=graph.json_graph('static/talca_cl.json')
    return talca_graph.draw_graph()

@app.route("/intersection", methods=['POST'])
def intersection(): # 
	id_node = request.get_data()
	with open('static/talca_cl.json') as json_file:  
	    data = json.load(json_file)
	intersection = []
	for s in data['links']:
		if s['source'] == str(id_node) or s['target'] == str(id_node):
			if len(intersection) != 2:
				if len(intersection) == 0:
					try:
						intersection.append(s['name'])
					except:
						intersection.append('no_name')
				else:
					try:
						if intersection[0] != s['name']:
							intersection.append(s['name'])
					except:
						intersection.append('no_mame')

	return '/'.join(intersection)

@app.route("/dijkstra", methods=['POST'])
def dijkstra():
	l = request.get_data()
	data  = json.loads(l)
	points = data['points']

	s = int(points[0]) # source
	t = int(points[2]) # target

	talca_graph=graph.json_graph('static/talca_cl.json')
	distances,pred = talca_graph.dijkstra(s)

	# BUILD THE PATH
	streets_path = []
	path = talca_graph.shortest_path(pred,s,t)
	with open('static/talca_cl.json') as json_file:  
		data = json.load(json_file)

	for id_node in path:
		intersection = []
		for s in data['links']:
			if s['source'] == str(id_node) or s['target'] == str(id_node):
				if len(intersection) != 2:
					if len(intersection) == 0:
						try:
							intersection.append(str(s['name']))
						except:
							intersection.append('no_name')
					else:
						try:
							if intersection[0] != s['name']:
								intersection.append(str(s['name']))
						except:
							intersection.append('no_mame')
		streets_path.append('/'.join(intersection))

	

	# TOTAL DISTANCE 
	d = 0
	for i in range(len(path)-1):
		for e in data['links']:
			if e['source'] == str(path[i]) and e['target'] == str(path[i+1]):
				d += float(e['length'])
	print (path,d)
	return jsonify({'path':path, 'streets':streets_path,'d':d})

@app.route("/draw_streets", methods = ['POST'])
def draw_streets():
	p = request.get_data()
	data  = json.loads(p)
	path = data['path']
	talca_graph=graph.json_graph('static/talca_cl.json')
	return talca_graph.draw_path(path)







@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(port=5000, debug=True)