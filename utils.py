import os
from vectorDB.load_db import LoadVectorDB, Query
from Parse_Data.USC_LogParser import LogParser


def parse_and_query_vector(filepath):
    data_results = LogParser().process_data(filepath)
    collection = None

    for data in data_results:
        vector_query = f"{data['test_name']}; {data['keyword_failed']}; {data['test_name']}"
        if collection is None:
            collection = LoadVectorDB()
        query_results = Query(collection, vector_query)
        data['AI_data_failure'] = query_results
        print(query_results)
    return data_results

def calculate_failure_rate(data):
    data = data['AI_data_failure']
    result_percent = {}
    total_failures = len(data)
    failure_counts = {}
    for item in data:
        failure_reason = item['Failure_Reason']
        failure_counts[failure_reason] = failure_counts.get(failure_reason, 0) + 1

    for reason, count in failure_counts.items():
        result_percent[reason] = (count / total_failures) * 100
    print(result_percent)

    return result_percent

def process_data_response(response):
    response_data = []

    for res in response:
        AI_results = calculate_failure_rate(res)
        data = {
            "Week": "22",
            "Product": "SBC_CORE",
            "Test_File_Name": res['source'],
            "Test_case_name": res['test_name'],
            "Failed_Keyword": res['keyword_failed'],
            "Robot_log": res['failure_reason']
        }
        for key, value in AI_results.items():
            data[key] = f"{value}%"
        response_data.append(data)
    return response_data
