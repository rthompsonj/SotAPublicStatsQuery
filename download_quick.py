from elasticsearch import Elasticsearch
from utils.query_builder import construct_request
from utils.args import get_args
import json

from config import IP, PORT

def data_dump():
    args = get_args()
    
    es = Elasticsearch([dict(host=IP, port=PORT)])

    time_frame_start = args.time_frame_start
    time_frame  = args.time_frame
    search_term = args.search_term

    request = construct_request(es, search_term, time_frame_start, time_frame)

    result = es.search(
        size = 10000,    # hard limit for es.search()
        body = request
    )

    results = [i['_source'] for i in result['hits']['hits']]

    with open(args.output, 'w') as f:
        f.write(json.dumps(results))

    return results

if __name__ == '__main__':
    data_dump()
