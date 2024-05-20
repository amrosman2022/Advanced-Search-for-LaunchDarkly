"""
Uploads a CSV file to the server and saves it to the 'uploads' directory.

Args:
    csvFile (werkzeug.datastructures.FileStorage): The CSV file uploaded by the user.
    userID (str): The ID of the user uploading the file.

Returns:
    tuple: A tuple containing the simple file name and a success message, or an error message on failure.
"""


from flask import Flask, request
import os
from flask_cors import CORS, cross_origin 

app = Flask(__name__)
CORS(app)

#root_dir = os.path.dirname(os.path.abspath(__file__)) +  '/uploads'
userID = ""
 

@app.route('/upload_csv', methods=['POST'])
@cross_origin()
def upload_csv():
    if 'csvFile' not in request.files:
        #return 'No CSV file provided', 400
        print("No CSV file provided")
        return "400"

    csv_file = request.files['csvFile']
    userID = request.form['userID']
    userID = userID.replace(" ", "")
    root_dir = request.form['uploadDir']
    print(f"Saving file to: {root_dir}")
    if csv_file.filename == '':
        #return 'No selected CSV file', 400
        print("No selected CSV file")
        return "400"

    try:
        # Read the file data from the request
        file_data = csv_file.read()

        # Custom file saving logic
        # You can perform additional validation, processing, and error handling here
        # For example, save the file to a specific location
        sFileName = root_dir + '/' + userID + "_csvMigrationFile.csv" #+ csv_file.filename 
        sSimpleFileName = userID + "_csvMigrationFile.csv" #+ csv_file.filename
        with open(sFileName, 'wb') as f:
            f.write(file_data)

        #return sSimpleFileName, '[' + sSimpleFileName + '] uploaded successfully', "200"
        print (sSimpleFileName, '[' + sSimpleFileName + '] uploaded successfully')
        return "200"
    except Exception as e:
        #return f'Failed to save CSV file: {e}', 500
        print (f'Failed to save CSV file: {e}')
        return "500"

if __name__ == '__main__':
    app.run(debug=False, port=9080,host='0.0.0.0')

