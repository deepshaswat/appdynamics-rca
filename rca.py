import requests, json, sys, itertools
from scipy.stats.stats import pearsonr

controller_url = sys.argv[1]
query_path = "/controller/rest/applications/"
application_name = "dis-perf-a"
time_range = 120
rest_url = controller_url + query_path + application_name
rollup_query = "&rollup=false"
json_query = "&output=json"

user = sys.argv[2]
password = sys.argv[3]

f = open("metrics","r")

##TODO: Understand difference between value and current - https://docs.appdynamics.com/display/PRO43/Metric+and+Snapshot+API
class MetricValue:
    count = -1
    minimum = -1
    summ = -1
    value = -1
    current = -1
    timestamp = -1
    occurences = -1
    standardDeviation = -1

    def __init__(self,metric_data):
        try:
            self.count = metric_data['count']
            self.minimum = metric_data['min']
            self.summ = metric_data['sum']
            self.value = metric_data['value']
            self.current = metric_data['current']
            self.timestamp = metric_data['startTimeInMillis']
            self.occurences = metric_data['occurrences']
            self.standardDeviation = metric_data['standardDeviation']
        except KeyError:
            print "All Data not Found for a metric"

    def printMetricData(self):
        print self.current, self.value

class Metric:
    metricList = []
    path = ""

    def __init__(self, path, metricList):
        self.path = path
        self.metricList = metricList

    def printMetricMetadata(self):
        print self.path, len(self.metricList)

    def getOneDValueArray(self):
        valueList = []
        for metric in self.metricList:
            metricData = MetricValue(metric)
            valueList.append(metricData.value)
        return valueList

allMetricValueLists = []

for line in f:
    metric_path = line.strip('\n')
    full_url = rest_url + metric_path + str(time_range) + rollup_query + json_query
    #print full_url
    r = requests.get(full_url, auth=(user, password))
    metric_data = json.loads(r.text)
    metricList = Metric(metric_path, metric_data[0]['metricValues'])
    allMetricValueLists.append(metricList.getOneDValueArray())

#print len(allMetricValueLists)

allPairs = list(itertools.combinations(allMetricValueLists, 2))
for pairs in allPairs:
    print pearsonr(pairs[0], pairs[1])

