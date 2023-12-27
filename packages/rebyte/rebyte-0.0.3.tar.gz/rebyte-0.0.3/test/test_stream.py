import requests

def stream_sync_api(url, headers=None, params=None):
    # Ensure that stream=True to stream the response
    with requests.get(url, headers=headers, params=params, stream=True) as response:
        if response.encoding is None:
            response.encoding = 'utf-8'
        
        # Check if the response status code is OK
        if response.status_code != 200:
            print("Error:", response.status_code)
            return
        
        # Iterate over lines in the response and print them
        for line in response.iter_lines(decode_unicode=True):
            if line:
                print(line)
data = {
    "version": "latest",       
    "inputs": [{"messages": [{"role": "user","content": "My name is John"}]}],
    "config": {},
    "stream": True
}
# Example usage of stream_sync_api function
stream_sync_api(
    url='https://rebyte.ai/api/sdk/p/d4e521a67bb8189c2189/a/a38ec8c60c3925696385/r',
    headers={'Accept': 'text/event-stream',
             "Authorization": "Bearer sk-"},
    params=data
)