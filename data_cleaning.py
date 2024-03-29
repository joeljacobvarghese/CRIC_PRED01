import json
import csv
import os
import glob
import pandas as pd

# Base directory 
Base = os.getcwd()

# Directory containing JSON files
DatasetDir = os.path.join(Base, 'ODI_DATASET')

# Paths for source JSON file and the target CSV file
ModifiedDatasetPath = os.path.join(Base, 'odi.csv')
First_Innings_Path = os.path.join(Base, 'First_Innings.csv')
Second_Innings_Path = os.path.join(Base, 'Second_Innings.csv')


def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted existing file: {file_path}")

delete_file_if_exists(ModifiedDatasetPath)
delete_file_if_exists(First_Innings_Path)
delete_file_if_exists(Second_Innings_Path)



def convert_innings_to_dataset(dataset_path, output_csv_path):
    try:
        with open(dataset_path, 'r') as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {dataset_path}. File may be empty or invalid JSON.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while processing {dataset_path}: {e}")
        return

    if 'outcome' in data['info'] and data['info']['outcome'].get('result') == 'no result':
        print(f"Match had no result, skipping file: {dataset_path}")
        return  
    
    final_total_runs = 0
    for over in data['innings'][0]['overs']:
        for delivery in over['deliveries']:
            final_total_runs += delivery['runs']['total']
    
    write_header = not os.path.exists(output_csv_path) or os.path.getsize(output_csv_path) == 0
    
    
    with open(output_csv_path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        
        if write_header:
            writer.writerow(["Runs", "Overs", "Wickets", "Chasing score", "Total"])
        
        total_runs = 0
        total_wickets = 0
        
        # Loop through each over
        for over in data['innings'][0]['overs']:
            current_over  = over['over']           
            balls = 0

            for delivery in over['deliveries']:
                
                total_runs += delivery['runs']['total'] 
                if 'wickets' in delivery:  
                    total_wickets += 1

                if 'extras' not in delivery:
                    balls +=1
                    
                
                current_delivery = f"{current_over}.{balls}"
                
               
                writer.writerow([total_runs, current_delivery, total_wickets, -1,  final_total_runs])
            
        final_total_runs_second_innings = 0
        
        total_runs = 0
        total_wickets = 0
        
        for over in data['innings'][1]['overs']:
            for delivery in over['deliveries']:
                final_total_runs_second_innings += delivery['runs']['total']
        
        for over in data['innings'][1]['overs']:
            current_over  = over['over']           
            balls = 0

            for delivery in over['deliveries']:
                
                total_runs += delivery['runs']['total'] 
                if 'wickets' in delivery:  
                    total_wickets += 1

                if 'extras' not in delivery:
                    balls +=1
                    
                
                current_delivery = f"{current_over}.{balls}"
                
               
                writer.writerow([total_runs, current_delivery, total_wickets, final_total_runs, final_total_runs_second_innings])

for file_name in glob.glob(os.path.join(DatasetDir, '*.json')):
    print(file_name)
    convert_innings_to_dataset(file_name, ModifiedDatasetPath)
    print(f"Dataset created at {ModifiedDatasetPath}")

dataset = pd.read_csv(ModifiedDatasetPath)


First_Innings = dataset[dataset['Chasing score'] == -1].drop(columns=['Chasing score'])
Second_Innings = dataset[dataset['Chasing score'] != -1]


First_Innings.to_csv(First_Innings_Path, index=False)
Second_Innings.to_csv(Second_Innings_Path, index=False)






