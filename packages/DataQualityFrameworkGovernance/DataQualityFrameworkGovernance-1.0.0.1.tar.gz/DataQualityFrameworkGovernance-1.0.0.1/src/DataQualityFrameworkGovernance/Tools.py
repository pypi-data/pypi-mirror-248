import csv
import json

def csv_to_json(input_csv_file, output_json_file):
    #read data from CSV file
    with open(input_csv_file, 'r') as csv_input:
        csv_reader = csv.DictReader(csv_input)
        data = list(csv_reader)

    #write data to JSON file
    with open(output_json_file, 'w') as json_output:
        json.dump(data, json_output, indent=2)

def json_to_csv(input_json_file, output_csv_file):
    #read data from JSON file
    with open(input_json_file, 'r') as json_input:
        data = json.load(json_input)

    #xtract column headers from the first row of data
    headers = list(data[0].keys())

    #write data to CSV file
    with open(output_csv_file, 'w', newline='') as csv_output:
        csv_writer = csv.DictWriter(csv_output, fieldnames=headers)
        
        #write header row
        csv_writer.writeheader()
        
        #write data rows
        csv_writer.writerows(data)

#if __name__ == "__main__":
#    input_json_file = '/Users/rajithprabhakaran/Library/Mobile Documents/com~apple~CloudDocs/Documents/Python/json_output.json'
#    output_csv_file = '/Users/rajithprabhakaran/Library/Mobile Documents/com~apple~CloudDocs/Documents/Python/Output.csv'
#    csv_to_json(output_csv_file, input_json_file)
    