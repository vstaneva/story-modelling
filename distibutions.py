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
        dist_list = []
        for i in xrange(size(options)):
            prob, option = probs[i], options[i]
            dist_list.append((prob,option))
        return dist_list
        
    
    def __init__(self, name, dist_options, dist_probs=None, data, parent):
        self.name = name
        self.distribution = options_dist(dist_options, dist_probs)
        self.data = data
        self.tmstamp = datetime.datetime.now()
        self.arrows_out = []
        self.parent = parent
        
    def add_arrow(prob, next):
        self.arrows_out.append((prob, next))

