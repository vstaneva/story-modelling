# from scipy import stats
import datetime
import json

class Process:
    
    all = {}

    def options_dist(options, probs=None):
        if probs is None:
            probs = [1/len(options)]*len(options)
        else: #normalise the probabilities
            probs = [float(prob)/sum(probs) for prob in probs]
        dist_dict = {}
        for i in range(len(options)):
            dist_dict[options[i]] = probs[i]
        return dist_dict
        
    def __init__(self, name, id, parent, dist_options, dist_probs=None, data=None):
        self.name = name
        self.id = id
        self.distribution = Process.options_dist(dist_options, dist_probs)
        self.data = data
        self.tmstamp = datetime.datetime.now()
        self.arrows_out = []
        self.parent = parent
        Process.all[id] = self
        
    def add_arrow(self, arrow_label, next_data):
        next_name = next_data[0]
        next_id = next_data[1]
        next_dist_options = next_data[2]
        next_dist_prob = next_data[3]
        next_datasheet = next_data[4]
        next_parent = self
        next = Process(next_name, id, self, next_dist_options, next_dist_prob, next_datasheet)
        prob = self.distribution[arrow_label]
        self.arrows_out.append((arrow_label, prob, next))

def read_from_json(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
        if data["type"] == "process": # add more later on!
            info = data["info"]
            name = info["name"]
            id = info["id"]
            parent = info["parent"]
            options = info["options"]
            probs = info["probs"]
            data = info["data"]
            return Process(name, id, parent, options, probs, data)
        if data["type"] == "arrow":
            info = data["info"]
            id = info["id"]
            parent = info["parent"]
            name = info["name"]
            arrow_label = info["arrow_label"]
            options = info["options"]
            probs = info["probs"]
            data = info["data"]
            arrow = [name, id, options, probs, data]
            process = Process.all[parent]
            process.add_arrow(arrow_label, arrow)


# Some testing
student = Process("student",10, None, ["cheat", "not cheat"])
student.add_arrow("cheat",     ["first coin",20, ["heads", "tails"], None, None])
student.add_arrow("not cheat", ["first coin",30, ["heads", "tails"], None, None])  
first_coin_1 = student.arrows_out[0]
print (student.arrows_out[0][0])

# Test with the js
stdnt = read_from_json("student.json")
read_from_json("add_first_coin_1.json")
print (stdnt.arrows_out[0][0])
