from datetime import datetime, timedelta
import time

def construct_request(elastic_connection, search_term, time_frame_start, time_frame):
    start_time = datetime.today() - timedelta(days=time_frame_start)
    
    gte_time = time.mktime( (start_time - timedelta(days=time_frame)).timetuple() ) * 1000
    lte_time = time.mktime( (start_time).timetuple() ) * 1000
    
    try:
        gte_time = long(gte_time)
        lte_time = long(lte_time)
    except (NameError):
        gte_time = int(gte_time)
        lte_time = int(lte_time)        
    
    REQUEST = {
        #"size": 500,
        "sort": [
            {
                "@timestamp": {
                    "order": "desc",
                    "unmapped_type": "boolean"
                }
            }
        ],
        "query": {
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "query": search_term,
                            "analyze_wildcard": True
                        }
                    },
                    {
                        "range": {
                            "@timestamp": {
                                "gte": gte_time,
                                "lte": lte_time,
                                "format": "epoch_millis"
                            }
                        }
                    }
                ],
                "must_not": []
            }
        },
    }
    
    return REQUEST


