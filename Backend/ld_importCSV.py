import csv
import requests
import json


#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
def str2Bool(value):
    if value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False
    else:
        return value


#------------------------------------------------------------
# --------- Load the CSV data into a JSON structure ---------
#------------------------------------------------------------
def read_csv_and_generate_payload(csv_file_path):
    payloads = []
    projects = []
    try:
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                variations = []
                # Dynamically iterate over the variations columns
                for key, value in row.items():
                    if key.startswith('projectID'):     # set the projects list for every iteration
                        projects.append(value)
                        
                    if key.startswith('variations.') and key.endswith('.value'):
                        variation_number = key.split('.')[1]
                        variation = {
                            "value": str2Bool(value),  # Convert string to boolean
                            "description": row.get(f'variations.{variation_number}.description', ''),
                            "name": row.get(f'variations.{variation_number}.name', '')
                        }
                        if variation.get('value') != '': variations.append(variation)

                payload = {
                    "clientSideAvailability": {
                        "usingEnvironmentId": str2Bool(row.get('clientSideAvailability.usingEnvironmentId', True)),
                        "usingMobileKey": str2Bool(row.get('clientSideAvailability.usingMobileKey', True))
                    },
                    "key": row.get('key', ''),
                    "name": row.get('name', ''),
                    "description": row.get('description', ''),
                    "variations": variations,
                    "temporary": str2Bool(row.get('temporary', True)),
                    "tags": [tag.strip() for tag in row.get('tags', '').split(',') if tag.strip()]
                }
                payloads.append(payload)
    except Exception as e:
        print(f"{e} @ {csv_file_path}")
        return False, '{"error":%s}' %(e)

    return True, payloads, projects

#------------------------------------------------------------
#------Write payloads to LaunchDarkly -----------------------
#------------------------------------------------------------
def func_writeLDrecord(o_payloads, s_project_key, s_authorization):

    try:
        s_url = "https://app.launchdarkly.com/api/v2/flags/" + s_project_key

        o_headers = {
        "Content-Type": "application/json",
        "Authorization": s_authorization
        }

        response = requests.post(s_url, json=o_payloads, headers=o_headers)

        data = response.json()
        print(data)
        return True, response.status_code,s_project_key + '.' + o_payloads['key'],response.reason, data
    
    except Exception as e:
        return False, 500, '{"error":%s}' %(e)
    

# ---------------------------------------------------------------------
# --- Write payloads to LaunchDarkly API ---
# ---------------------------------------------------------------------
def func_copyCSVtoLD(csv_file_path, user_id, s_LDTargetSubscription):
    oResults=[]
    #s_LDTargetSubscription = "api-d5bb3095-3cd2-467d-a5fd-eb52409fce9e"
    #sCSVfullFilePath = '/Users/aosman/Documents/AllMyDocuments/LaunchDarkly/Demo-Materials/LaunchDarkly-Enterprise-Search-Project/Backend/upLoadSvr/uploads/amrosman_csvMigrationFile.csv'
    sCSVfullFilePath = csv_file_path + '/' + user_id + '_' + 'csvMigrationFile.csv'
    payloads = read_csv_and_generate_payload(sCSVfullFilePath)
    if payloads[0] == True:
        for payload, project in zip(payloads[1], payloads[2]):
            #print(payload)
            #print(project)
            s_Result = func_writeLDrecord(payload, project, s_LDTargetSubscription)
           
            oRecord = {
                "success": s_Result[0],
                "code": s_Result[1],
                "flag":  s_Result[2],
                #"message": sMessage
                "message": (s_Result[4]['code'] + ', ' + s_Result[4]['message']) if s_Result[1] != 201 else "The " + s_Result[4]['kind'] + " FLAG [" + s_Result[4]['key'] + "] was created successfully"
            }
            oResults.append(oRecord)
            #print (s_Result[0])
        return True, oResults
    else:
        return False, 500, '{"error": "Error reading CSV file and creating JSON payloads"}'
