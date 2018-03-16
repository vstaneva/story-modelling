# from scipy import stats
import datetime
import json
import jsonpickle

class Process:
    
    all = {}

    def norm_probs(options, probs):
        if probs is None:
            probs = [1/len(options)]*len(options)
        else: #normalise the probabilities
            probs = [float(prob)/sum(probs) for prob in probs]
        return probs

    def options_dist(options, probs=None):
        probs = Process.norm_probs(options, probs)
        dist_dict = {}
        for i in range(len(options)):
            dist_dict[options[i]] = probs[i]
        return dist_dict
        
    def __init__(self, dict):
        self.dict = dict
        if self.dict["distribution"]["type"] == "discrete options":
            options = self.dict["distribution"]["options"]
            probs = self.dict["distribution"]["probs"]
            self.dict["distribution"] = Process.options_dist(options, probs)
        self.dict["tmstamp"] = datetime.datetime.now().strftime("%s")
        self.dict["arrows_out"] = {}
        
        self.id = self.dict["id"]
        self.tmstamp = self.dict["tmstamp"]
        Process.all[self.id] = self
        
    def add_arrow(self, arrow_label, next_data):
        prob = self.dict["distribution"][arrow_label]
        next = Process(next_data)
        self.dict["arrows_out"][arrow_label] = (prob, next)

def read_from_json(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
        if data["type"] == "process": # add more later on!
            info = data["info"]
            return Process(info)
        if data["type"] == "arrow":
            info = data["info"]
            arrow_keys = ["name", "id", "distribution", "data"]
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
            
def take_snapshot(root_id):
    process = Process.all[root_id]
    json_content = {}
    json_content["type"] = "timestamp dump"
    json_content["info"] = process
    json_load = jsonpickle.encode(json_content)
    timestamp = datetime.datetime.now().strftime("%s")
    filename = str(timestamp)+".json"
    # below, check if "logs" dir exists
    with open("logs/"+filename, "w") as file:
        file.write(json_load)

# Some testing
student = Process({
        "name": "student",
        "id": 10,
        "parent": None,
        "distribution": {
            "type": "discrete options",
            "options": ["cheat", "not cheat"],
            "probs": None}
        })
student.add_arrow(
    "cheat", {
        "name": "first coin",
        "parent": 10,
        "id": 20,
        "distribution":{
            "type": "discrete options",
            "options": ["heads", "tails"],
            "probs": None },
        "data": None})
student.add_arrow(
    "not cheat", {
        "name": "first coin",
        "parent": 10,
        "id": 30,
        "distribution": {
            "type": "discrete options",
            "options": ["heads", "tails"],
            "probs": None},
        "data": None})  
first_coin_1 = student.dict["arrows_out"]["cheat"]
print (student.dict["arrows_out"]["cheat"][0])

# Test with the js
stdnt = read_from_json("student.json")
read_from_json("add_first_coin_1.json")
read_from_json("add_first_coin_2.json")
print (stdnt.dict["arrows_out"]["not cheat"][1].dict["name"])
take_snapshot(stdnt.dict["id"])
