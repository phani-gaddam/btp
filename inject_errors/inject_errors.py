import json
import sys
import random

def newError():
    return {
        "key": "error",
        "type": "bool",
        "value": "true"
    }

args = sys.argv
# print(args)
err_prcnt = 0.0
if len(args) == 1:
    err_prcnt = 0.2

err_prcnt = int(args[1]) / 100

# working with test_cases/demo.json copied as inject.json

# load json
data = json.load(open("./inject.json"))
# get specific tag
# check if there is error already
# inject error accordingly


# print(data['data'][0]['spans'])

for span in data['data'][0]['spans']:
    # check if there are tags
    if span.get('tags') is not None:
        # check if there are error tags
        for tag in span.get('tags'):
            # has error = true
            if tag.get('key') == 'error' and tag.get('type') == 'bool' and tag.get('value') == 'true':
                # print(span)
                pass
            else:
                if random.random() < err_prcnt:
                    span['tags'].append(newError())
    else:
        if random.random() < err_prcnt:
                span['tags'] = newError()



json.dump(data,open("./injected.json",'w'))