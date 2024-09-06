from app import handler

event = {
    'keyphrases': 'ML',
    'queries': {'DFT': 'nasicon'},
    'num_results': 5
}

context = {}

result = handler(event, context)

# Convert the keyphrases and queries from the event
keyphrases = event['keyphrases'].split('-')
queries = event['queries']

print(result)

