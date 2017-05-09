from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from utils.query_builder import construct_request
from utils.args import get_args
import json

from config import IP, PORT

def data_dump():
    print('CURRENTLY DISABLED, USE download_quick.py INSTREAD')
    import sys
    sys.exit()

    args = get_args()
    
    es = Elasticsearch([dict(host=IP, port=PORT)],
                       timeout=30, max_retries=10, retry_on_timeout=True)

    time_frame  = args.time_frame
    search_term = args.search_term

    request = construct_request(es, search_term, time_frame)

    scan_result = scan(
        es,
        query=request,
        scroll='5m',
        size=1000
    )

    results = []
    for result in scan_result:
        results.append(result['_source'])

    with open(args.output,'w') as f:
        f.write(json.dumps(results))
        
    return results

if __name__ == '__main__':
    print('CURRENTLY DISABLED, USE download_quick.py INSTREAD')
    #data_dump()
