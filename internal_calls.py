# Use this inside of the container, iterating over the list of queries and showing no memory growth
from queries import queries
from run_ov import run_ov
import time
ov = run_ov()
start_time = time.perf_counter()
for test in queries:
    print( ov.predict(test)[:8])
end_time = time.perf_counter()
print(f"{len(queries)} embeddings done in {round(end_time-start_time,2)} seconds.")



