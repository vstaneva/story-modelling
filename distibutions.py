from scipy import stats
import datetime

Class Process:
    def dist_from_name(name, attributes): # maybe use in the future, for now -- not
        if name == "uniform":
            low, high = attribites[0], attributes[1]
            return stats.uniform(low, high)
        elif name == "discrete uniform":
            low, high = attributes[0], attributes[1]
            return stats.randint(low, high)
        elif name == "coin": #right now we only use this, I think
            p = attributes[0]
            return stats.bernoulli(p)
    
    def options_dist(options, probs=None):
        if probs is None:
            probs = [1/size(options)]*size(options)
        else: #normalise the probabilities
            probs = [float(prob)/sum(probs) for prob in probs]
        dist_dict = {}
        for i  in xrange(size(options)):
            dist_dict[options[i]] = probs[i]
        return dist_dict
        
    def __init__(self, name, parent, dist_options, dist_probs=None, data=None):
        self.name = name
        self.distribution = options_dist(dist_options, dist_probs)
        self.data = data
        self.tmstamp = datetime.datetime.now()
        self.arrows_out = []
        self.parent = parent
        
    def add_arrow(self, option, next_data):
        next_name = next_data[0]
        next_dist_options = next_data[1]
        next_dist_prob = next_data[2]
        next_datasheet = next_data[3]
        next_parent = self
        next = Process(next_name, next_dist_options, next_dist_prob, next_datasheet, next_data, self)
        prob = self.dist[option]
        self.arrows_out.append((prob, next))

# Some testing
student = Process("student", None, ["cheat", "not cheat"])
student.add_arrow("cheat",     ["first coin", ["heads", "tails"], None, None])
student.add_arrow("not cheat", ["first coin", ["heads", "tails"], None, None])  
