from datetime import datetime, timedelta
import time

def construct_request(elastic_connection, search_term, time_frame):
    gte_time = time.mktime( (datetime.today() - timedelta(days=time_frame)).timetuple() ) * 1000
    lte_time = time.mktime( (datetime.today()).timetuple() ) * 1000

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
                                "gte": long(gte_time),
                                "lte": long(lte_time),
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


