from seldon_core.seldon_client import SeldonClient
import time
from queries import queries


def runtest():
    client = SeldonClient(deployment_name="run_ov", namespace="seldon", gateway_endpoint="127.0.0.1:5000", gateway="ambassador")
    start_time = time.perf_counter()
    for test in queries:
        data = {"data":{"names":["text"],"ndarray":[test]}}
        embeds = client.predict(transport="grpc", raw_data=data)
        print(embeds.response['data']['ndarray'][0][:4], flush=True)
        print('#######', flush=True)
    end_time = time.perf_counter()
    print(f"{len(queries)} embeddings done in {end_time-start_time} seconds")

if __name__=='__main__':
    for i in range(10):
        runtest()

