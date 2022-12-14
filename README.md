# CRISP: Critical Path Analysis of Microservice Traces

This repo contains code to compute and present critical path summary from [Jaeger](https://github.com/jaegertracing/jaeger) microservice traces.
To use first collect the microservice traces of a specific endpoint in a directory (say `traces`).
Let the traces be for `OP` operation and `SVC` service (these are Jaeger termonologies).
`python3 process.py --operationName OP --serviceName SVC -t <path to trace> -o . --parallelism 8` will produce the critical path summary using 8 concurrent processes. 
The summary will be output in the current directory as an HTML file with a heatmap, flamegraph, and summary text in `criticalPaths.html`.
It will also produce three flamegraphs `flame-graph-*.svg` for three different percentile values.

The script accepts the following options:

```
python3 process.py --help
usage: process.py [-h] -a OPERATIONNAME -s SERVICENAME [-t TRACEDIR] [--file FILE] -o OUTPUTDIR
                  [--parallelism PARALLELISM] [--topN TOPN] [--numTrace NUMTRACE] [--numOperation NUMOPERATION]

optional arguments:
  -h, --help            show this help message and exit
  -a OPERATIONNAME, --operationName OPERATIONNAME
                        operation name
  -s SERVICENAME, --serviceName SERVICENAME
                        name of the service
  -t TRACEDIR, --traceDir TRACEDIR
                        path of the trace directory (mutually exclusive with --file)
  --file FILE           input path of the trace file (mutually exclusivbe with --traceDir)
  -o OUTPUTDIR, --outputDir OUTPUTDIR
                        directory where output will be produced
  --parallelism PARALLELISM
                        number of concurrent python processes.
  --topN TOPN           number of services to show in the summary
  --numTrace NUMTRACE   number of traces to show in the heatmap
  --numOperation NUMOPERATION
                        number of operations to show in the heatmap
  -we, --withErrors
                        get critical path that only shows errors in the original critical path
  -ee, --excludingErrors
                        get critical path and exclude error containing nodes in identification. 
```
