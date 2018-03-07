from scipy import stats
import datetime

class Process:
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
        
    def add_arrow(self, option, next_data):
        next_name = next_data[0]
        next_id = next_data[1]
        next_dist_options = next_data[2]
        next_dist_prob = next_data[3]
        next_datasheet = next_data[4]
        next_parent = self
        next = Process(next_name, self, next_dist_options, next_dist_prob, next_datasheet)
        prob = self.distribution[option]
        self.arrows_out.append((prob, next))

# Some testing
student = Process("student",1, None, ["cheat", "not cheat"])
student.add_arrow("cheat",     ["first coin",2, ["heads", "tails"], None, None])
student.add_arrow("not cheat", ["first coin",3, ["heads", "tails"], None, None])  
first_coin_1 = student.arrows_out[1]
first_coin_1.add_arrow
