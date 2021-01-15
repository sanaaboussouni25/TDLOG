import sys
import trace
import tracemalloc

"""1.Trace : count how many times statements have been executed"""

# create a Trace object, telling it what to ignore, and whether to do tracing or line-counting or both.
tracer = trace.Trace(
    ignoredirs=[sys.prefix, sys.exec_prefix], trace=1, count=1)

# run the new command using the given tracer
tracer.run('interface.py')

# make a report, placing output in the current directory
r = tracer.results()
r.write_results(show_missing=True, coverdir=".")

"""2.Tracemalloc : displays the ten executions that allow the most memory"""
'''
tracemalloc.start()

# run the application

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("[ Top 10 ]")
for stat in top_stats[:10]:
    print(stat)
'''

"""3.Coverage : to be runned from the terminal with the following command, 
making sure you're in the TDLog python file, 
    coverage run test.py
    coverage annotate -d ./Annotate
"""