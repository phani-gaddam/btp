# Error Analysis of Microservice Traces

This repo contains code to compute and present critical path summary from [Jaeger](https://github.com/jaegertracing/jaeger) microservice traces.

It also contains code to compute critical paths considering errors which show the amount of useful and wasted work. This functionality is triggered using special parser flags and those flags are in the help section below.

It also contains functionality to generate pair-wise error metrics and represent them in bar plots and dot graphs.

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
  -ae, --analyseErrors
                        Analyse the errors and produce graphs for the same
```

Analyze Erros Flag will analyze the errors in the traces and represent the errors in services in bar plots and dot graphs.

The functions to generate pair-wise metrics are all in the `merge.py` file.

This function calls the `plot_all` function from the graphers module. The graphers module contains five files, each house is a fucntion that sorts the inout dictionary based on different variables and generates plots accordingly.

The `merge.py` file also contains a function `generatehtml` which generates a dot graph based on the matrix and incorporates it into a html file.