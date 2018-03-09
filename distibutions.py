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
        next_name = next_data["name"]
        next_id = next_data["id"]
        next_dist_options = next_data["options"]
        next_dist_prob = next_data["probs"]
        next_datasheet = next_data["data"]
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
            arrow_keys = ["name", "id", "options", "probs", "data"]
            arrow = {key:value for key,value in info.items() if key in arrow_keys}
            parent = info["parent"]
            arrow_label = info["arrow_label"]
            process = Process.all[parent]
            process.add_arrow(arrow_label, arrow)
    def take_json_snapshot(root_id):
        # prepare the json
        data = {}
        # walk the process graph -- for DFS, switch to stack
        process_q = queue.Queue()
        process_q.put(root_id)
        visited = set()
        while not process_q.empty():
            current_id = process_q.get()
            if current_id in visited:
                continue
            visited.add(current_id)
            current = Process.all[current_id]
            


# Some testing
student = Process("student",10, None, ["cheat", "not cheat"])
student.add_arrow(
    "cheat", {
        "name": "first coin",
        "id": 20,
        "options": ["heads", "tails"],
        "probs": None,
        "data": None})
student.add_arrow(
    "not cheat", {
        "name": "first coin",
        "id": 30,
        "options": ["heads", "tails"],
        "probs": None,
        "data": None})  
first_coin_1 = student.arrows_out[0]
print (student.arrows_out[0][0])

# Test with the js
stdnt = read_from_json("student.json")
read_from_json("add_first_coin_1.json")
read_from_json("add_first_coin_2.json")
print (stdnt.arrows_out[0][0])
