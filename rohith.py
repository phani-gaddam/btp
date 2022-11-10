import json
import logging
import os

from graph import Graph, Metrics
debug_on = False

filepath = "./test_results/test_1/1.json"
serviceName = "S1"
operationName = "O1"
rootTrace = True
def process(filename):
    # process one Jaeger JSON trace file
    with open(os.path.join(filename), 'r') as f:
        data = json.load(f)
        graph = Graph(data, serviceName, operationName, filename, rootTrace)
        if graph.rootNode == None:
            return Metrics({}, {}, {}, {}, {}, {}, {}, 0, 0, 0)

        res = graph.findCriticalPath()
        for n in res:
            print(n)
        print("\n\n\n")
        res = graph.findCriticalPathExcludingErrors()
        for n in res:
            print(n)
        debug_on and logging.debug("critical path:" + str(res))


        metrics = graph.getMetrics(res)
        debug_on and logging.debug(metrics.opTimeExclusive)

        debug_on and logging.debug(
            "Test result = " +
            str(graph.checkResults(metrics.opTimeExclusive)))

        # artifically introduce the totalTime entry
        metrics.opTimeExclusive['totalTime'] = graph.rootNode.duration
        metrics.opTimeInclusive['totalTime'] = graph.rootNode.duration
        return metrics


process(filepath)