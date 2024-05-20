import requests
import json

# accepted values # [['message','flag', 'env', 'proj', 'done', 'error', 'time'],['','0', '0', '0', 'False', 'False', '']]

def func_CallAPI(sMode, sURL, s_valuePairs):     # expecting {'value': 'value'}
    nSet = 0

    sVlaues = (
        "/clear_status" if sMode == "clear" else
        "/update_status?" if sMode =="put" else
        "/events?" if sMode == "get" else
        ""
    )
    if (sVlaues == ""):
        return '{"status": "es_pushSSE Received an Invalid Mode"}'
    
    for key, value in s_valuePairs.items():     # SSE receiver sse_ex.py will only accept one value at a time. this loop is just future proof
        if (nSet > 0):
            sVlaues += "&"
        sVlaues += 'itemname=' + f"{key}" + "&"
        sVlaues += 'value=' + f"{value}"
        nSet += 1
    
    api = sURL + sVlaues    # JSON string of value pairs. its up to the receiver to use the content. 
   
    try:
        urlResponse = requests.get(f"{api}")
        # Find the indices of the first "{" and the last "}"
        start_index = urlResponse.text.find('{')
        end_index = urlResponse.text.rfind('}')

        # Extract the substring between "{" and "}"
        json_string = urlResponse.text[start_index:end_index + 1]

        return True, json_string
    except Exception as e:
        return False, str(e)

z=func_CallAPI('put','http://localhost:5050', {'flag':'90'})
z=func_CallAPI('put','http://localhost:5050', {'message':'hello....'})
x= func_CallAPI('get','http://localhost:5050', {'':''})
print(x)