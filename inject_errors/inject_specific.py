import sys
import os
from pathlib import Path
import json


#helper method to find the parent span
def find_parent_span(span, spans):
    parent_span_id = None
    for reference in span.get('references', []):
        if reference.get('refType') == 'CHILD_OF':
            parent_span_id = reference.get('spanID')
            break
    if parent_span_id:
        parent_span = next((s for s in spans if s['spanID'] == parent_span_id), None)
        return parent_span
    return None

#method to find spans of all the services till the root-service
def climb_up_spans(span, spans):
    path = []
    while span:
        path.append(span)
        span = find_parent_span(span, spans)
    return path

#OUTPUT a folder called injected if it does not exist. This folder contains the json file(s) with services that have error tags attached.
os.makedirs('../injected/', exist_ok=True)

args = sys.argv

#INPUT: a file (json file) or the name of a folder (containing multiple json files). Error tags are attached to the services in these json file(s).ut. The input files remain untouched.
fileOrFolder = args[1]

#INPUTS that are hardcoded 

input_services1 = ["Service19", "Service7", "Service9", "Service17"]  # list of services which have errors injected into them. In addition, for each service in the list, all the services on the call path up to the root-service are considered and errors are injected into all those services. 
input_services2 = ["Service5", "Service10", "Service46"]  # additional list of services, which have errors injected into them.

files = []
if os.path.isfile(fileOrFolder):
    files = [fileOrFolder]
elif os.path.isdir(fileOrFolder):
    files = Path(fileOrFolder).glob('*.json')

#For each span in the provided data, the code checks if the associated service name is present in the input list of services. If so, it proceeds with error injection.
#For list of services mentioned in input_services1, the code climbs up the spans hierarchy, starting from the current span, to find the parent span, grandparent span, and so on leading up to the root span.
#For each span found along the hierarchy up, the code adds an "error" tag if the span doesn't already have any tags. This tag is a boolean value set to "true" and indicates the presence of an error.
#For list of services mentioned in input_services2, the error tag is added to the associated span only.

for file in files:
    data = json.load(open(file))
    fileName = os.path.split(file)[1]

    spans = data['data'][0]['spans']
    processes = data['data'][0]['processes']

    for span in spans:
        process_id = span['processID']
        service_name = processes.get(process_id, {}).get('serviceName')
        if service_name in input_services1:
            path = climb_up_spans(span, spans)
            for path_span in path:
                tags = path_span.get('tags', [])
                if len(tags) == 0:
                    path_span['tags'] = path_span.get('tags', []) + [
                        {
                            "key": "error",
                            "type": "bool",
                            "value": "true"
                        }
                    ]
        if service_name in input_services2:
            tags = span.get('tags', [])
            if len(tags) == 0:
                span['tags'] = span.get('tags', []) + [
                    {
                        "key": "error",
                        "type": "bool",
                        "value": "true"
                    }
                ]

    json.dump(data, open(f"../injected/{fileName}", 'w+'))

