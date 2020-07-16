import json
import heapq
import numpy as np
from math import radians, cos, sin, asin, sqrt

class abstract_graph:
    
    def __init__(self,_edges):
        self.edges=_edges
        self.nodes={u for u,v in self.edges} | {v for u,v in self.edges}
    
    def adjacency_list(self):
        pass
    
class weighted_graph(abstract_graph):
    
    def __init__(self,_edges):
        self.edges=_edges
        self.nodes={u for u,v in self.edges.keys()} | {v for u,v in self.edges.keys()}
        
    def adjacency_list(self):
        adjacent=lambda n : {v:self.edges[(u,v)] for u,v in self.edges.keys() if u==n }
        return {v:adjacent(v) for v in self.nodes}




class json_graph(weighted_graph):

    def __init__(self,_path):
        with open(_path) as file:
            self.data=json.load(file)
        self.edges={ (int(e['source']),int(e['target'])):float(e['length']) for e in self.data['links']}
        self.nodes={u for u,v in self.edges.keys()} | {v for u,v in self.edges.keys()}
        self.nodes_location={int(n['id']):(float(n['y']),float(n['x'])) for n in self.data['nodes']}
    
    def adjacency_list(self):
        adjacent=lambda n : {v:self.edges[(u,v)] for u,v in self.edges.keys() if u==n }
        return {v:adjacent(v) for v in self.nodes}

    def draw_graph(self):
        coords_from_edge = lambda e : [ [float(w) for w in u.split()] for u in e['geometry'].split(' ',1)[1].encode('latin-1').replace('(','').replace(')','').split(',')]
        geo_json=[]
        for e in self.data['links']:
            if 'geometry' in e:
                line_string = {
                    'type': 'Feature',
                    'properties':{
                        'length':e['length'],
                        'source':e['source'],
                        'target':e['target']
                    },
                    'geometry':{
                        'type':'LineString',
                        'coordinates': coords_from_edge(e)
                    }   
                }
                geo_json.append(line_string)
            else:
                if int(e['source']) in self.nodes_location and int(e['target']) in self.nodes_location:
                    node_s=self.nodes_location[int(e['source'])]
                    node_t=self.nodes_location[int(e['target'])]
                    line_string = {
                        'type': 'Feature',
                        'properties':{
                            'length':e['length'],
                            'source':e['source'],
                            'target':e['target']
                        },
                        'geometry':{
                            'type':'LineString',
                            'coordinates': [[node_s[1],node_s[0]],[node_t[1],node_t[0]]]
                        }   
                    }
                    geo_json.append(line_string)
        geometries = {
            'type': 'FeatureCollection',
            'features': geo_json,
        }
        geo_str = json.dumps(geometries)
        return geo_str

    def draw_path(self,path):
        # recibe camino desde js dijkstra
        coords_from_edge = lambda e : [ [float(w) for w in u.split()] for u in e['geometry'].split(' ',1)[1].encode('latin-1').replace('(','').replace(')','').split(',')]
        geo_json=[]

        for e in self.data['links']:
            for i in range(len(path)-1):
                if str(path[i]) == e['source'] and str(path[i+1]) == e['target'] :
                    if 'geometry' in e:
                        line_string = {
                            'type': 'Feature',
                            'properties':{
                                'length':e['length'],
                                'source':e['source'],
                                'target':e['target']
                            },
                            'geometry':{
                                'type':'LineString',
                                'coordinates': coords_from_edge(e)
                            }   
                        }
                        geo_json.append(line_string)
                    else:
                        if int(e['source']) in self.nodes_location and int(e['target']) in self.nodes_location:
                            node_s=self.nodes_location[int(e['source'])]
                            node_t=self.nodes_location[int(e['target'])]
                            line_string = {
                                'type': 'Feature',
                                'properties':{
                                    'length':e['length'],
                                    'source':e['source'],
                                    'target':e['target']
                                },
                                'geometry':{
                                    'type':'LineString',
                                    'coordinates': [[node_s[1],node_s[0]],[node_t[1],node_t[0]]]
                                }   
                            }
                            geo_json.append(line_string)
        geometries = {
            'type': 'FeatureCollection',
            'features': geo_json,
        }
        geo_str = json.dumps(geometries)
        return geo_str

    def draw_nodes(self):
        geo_json=[]
        for n,pos in self.nodes_location.items():
            line_string = {
                'type': 'Feature',
                'properties':{
                    'name':str(n)
                },
                'geometry':{
                    'type':'Point',
                    'coordinates': [pos[1],pos[0]]
                    }   
                }
            geo_json.append(line_string)
        geometries = {
            'type': 'FeatureCollection',
            'features': geo_json,
        }
        geo_str = json.dumps(geometries)
        return geo_str

    def dijkstra(self,start):
        pq = []
        neighbors = self.adjacency_list()
       
        dists = {v:float('inf') for v in self.nodes}
        pred = dict()
        dists.update({start:0})
        #for v,w in dists.items():              # linea 1
        #   heapq.heappush(pq,(w,v))
        heapq.heappush(pq,(start,dists[start])) # linea 2
        while len(pq)>0:
            u,wu = heapq.heappop(pq) # get the min weight and the vertex
            for neig,weight in neighbors[u].items():
                new = dists[u] + weight
                if float(new) < float(dists[neig]):
                    heapq.heappush(pq,(neig,new))
                    dists.update({neig:new})
                    pred.update({neig:u})
        return dists,pred

    def shortest_path(self,parent,start,end):
        path=[end]
        k=end
        while k!= start:
            try:
                path.insert(0,parent[k])
                k=parent[k]
            except:
                return 'No hay camino'
        return path

    def print_paths(self,parent, start, nodes):
        return {v:shortest_path(parent, start, v) for v in nodes}
