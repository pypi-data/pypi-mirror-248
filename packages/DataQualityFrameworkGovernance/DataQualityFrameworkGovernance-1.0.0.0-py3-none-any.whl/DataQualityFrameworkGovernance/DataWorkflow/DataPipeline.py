import pandas as pd
import json
from datetime import datetime
import requests

def load_function_from_path(function_path):
    module_path, function_name = function_path.rsplit('.', 1)
    module = __import__(module_path, fromlist=[function_name])
    return getattr(module, function_name, None)

def validate_parameters(function, parameters):
    expected_params = list(function.__code__.co_varnames)
    for param_key in parameters:
        if param_key not in expected_params:
            raise ValueError(f"Invalid parameter '{param_key}' in JSON for function '{function.__name__}'. Expected parameters are {expected_params}")

# main function call to process the framework based on JSON file, JSON file is the parameter
def processing_framework(json_config_file, output_csv=None):
    #created an empty dataframe to save the final result after declaring the columns
    columns = ['DateTime', 'DQ#', 'Dataset_name','DQ_Dimension','DQ_Rule/Function_name','Error_in_JSON','Error log','DQ_Rule/Function_description',
               'DQ_Valid_count','DQ_Invalid_count','DQ_Total_count','DQ_Valid%','DQ_Invalid%','DQ_Flag_Inclusion','Data_enabled','Function_enabled',
               'Parameter_enabled','Source']
    
    final_result = pd.DataFrame(columns=columns)

    # handling the json file if it is saved in web / https / local drive
    if json_config_file.startswith('http://') or json_config_file.startswith('https://'):
        response = requests.get(json_config_file)

        if response.status_code == 200:
            config = json.loads(response.text)
            dataframe_configs = config.get('DataFrameDictionary', {})
            functions = config.get('DataFunctionConfig', [])
    else:
        # read configuration from JSON file - Locally
        with open(json_config_file, 'r') as json_file:
            config = json.load(json_file)
            dataframe_configs = config.get('DataFrameDictionary', {})
            functions = config.get('DataFunctionConfig', [])

    #create a dictionary to hold loaded DataFrames
    loaded_dataframes = {}
    #process each dataframe and save it in a list
    dataframe_list = []

    #create a new dataframe with its name and location / source
    dataframe_name = pd.DataFrame(columns=['df_name', 'data_path'])

    for df_name, df_config in dataframe_configs.items():
        if df_config.get('enabled', True):
            data_path = df_config.get('data_path', None)
            if data_path is not None:
                df = pd.read_csv(data_path)
                loaded_dataframes[df_name] = df
                dataframe_list.append(df)
                #list of all dataframe name and source / location
                dataframe_name = pd.concat([dataframe_name, pd.DataFrame({'df_name': [df_name], 'data_path': [data_path]})], ignore_index=True)
            else:
                print(f"{datetime.now()} : Missing data path for DataFrame '{df_name}'.")
        else:
            print(f"{datetime.now()} : DataFrame '{df_name}' is disabled.")

    #process each function
    for function_info in functions:
        if function_info.get('enabled', True):
            function_path = function_info.get('function_path', None)
            parameter_sets = function_info.get('parameters', [])

            # dynamically load the function from the specified path
            selected_function = load_function_from_path(function_path)

            if selected_function is not None and callable(selected_function):
                #process each set of parameters
                for parameters in parameter_sets:
                    if parameters.get('enabled', True):
                        #exclude keys that are not expected parameters
                        filtered_params = {k: v for k, v in parameters.items() if k != 'enabled'}

                        #validate parameters
                        validate_parameters(selected_function, filtered_params)

                        #flag to check calculate value No
                        flagParam = 0 
                        param_pairs = []
                        df_namelist = [] #df name list empty
                        df_pathlist = [] # df path list empty

                        #Capturing error in csv file
                        for param_key, param_value in filtered_params.items():
                            # Cpaturing dataset_name and dataset path within the loop
                            for value in dataframe_name['df_name'].values:
                                if value == param_value:
                                    dfname = dataframe_name.loc[dataframe_name['df_name'] == param_value, 'df_name'].values[0]
                                    dfpath = dataframe_name.loc[dataframe_name['df_name'] == param_value, 'data_path'].values[0]
                                    
                                    df_namelist.append(dfname)
                                    df_pathlist.append(dfpath)

                                    df_namelist_str = ', '.join(map(str, df_namelist))
                                    df_pathlist_str = ', '.join(map(str, df_pathlist))

                            if param_key == "calculate" and param_value == "No":
                                flagParam = 1
                                param_pairs.append(f"{param_key}: '{param_value}'")
                                param_all_for_description = 'Parameter: ' + ', '.join(param_pairs)
                                result = pd.DataFrame({
                                                        'DateTime': datetime.now(),
                                                        'DQ#': '[ERROR]',
                                                        'Dataset_name': df_namelist_str,
                                                        'DQ_Dimension': '[ERROR]',
                                                        'DQ_Rule/Function_name': function_path,
                                                        'Error_in_JSON': 'Yes',
                                                        'Error log': [f"{function_path} 'calculate' set to 'No', instead of 'Yes' in JSON config file"],
                                                        'DQ_Rule/Function_description': param_all_for_description,
                                                        'DQ_Valid_count': 'NotApplicable',
                                                        'DQ_Invalid_count': 'NotApplicable',
                                                        'DQ_Total_count': 'NotApplicable',
                                                        'DQ_Valid%': 'NotApplicable',
                                                        'DQ_Invalid%': 'NotApplicable',
                                                        'DQ_Flag_Inclusion': 'N',
                                                        'Data_enabled': df_config.get('enabled', True),
                                                        'Function_enabled': function_info.get('enabled', True),
                                                        'Parameter_enabled': parameters.get('enabled', True),
                                                        'Source': df_pathlist_str
                                                        })
                                
                                final_result = pd.concat([final_result, result], ignore_index=True)
                                print(f"{datetime.now()} : [ERROR] Function call with error")

                        #Process each specified DataFrame in parameters
                        if flagParam == 0:
                            df_namelist = [] #df name list empty
                            df_pathlist = [] # df path list empty

                            for param_key, param_value in filtered_params.items():
                                # Cpaturing dataset_name and dataset path within the loop
                                for value in dataframe_name['df_name'].values:
                                    if value == param_value:
                                        dfname = dataframe_name.loc[dataframe_name['df_name'] == param_value, 'df_name'].values[0]
                                        dfpath = dataframe_name.loc[dataframe_name['df_name'] == param_value, 'data_path'].values[0]
                                        
                                        df_namelist.append(dfname)
                                        df_pathlist.append(dfpath)

                                        df_namelist_str = ', '.join(map(str, df_namelist))
                                        df_pathlist_str = ', '.join(map(str, df_pathlist))

                                if isinstance(param_value, str) and param_value in loaded_dataframes:
                                    # Update the parameter to use the loaded DataFrame
                                    filtered_params[param_key] = loaded_dataframes[param_value]

                                param_pairs.append(f"{param_key}: '{param_value}'")
                                param_all_for_description = 'Parameter: ' + ', '.join(param_pairs)

                            #call the specified function with the dataframes and parameters
                            result = selected_function(**filtered_params)

                            if flagParam == 0:
                                #Amend the result dataset
                                result['Dataset_name'] = df_namelist_str
                                result['DQ_Rule/Function_name'] = function_path
                                result['DQ_Rule/Function_description'] = param_all_for_description
                                result['Data_enabled'] = df_config.get('enabled', True)
                                result['Function_enabled'] =  function_info.get('enabled', True)
                                result['Parameter_enabled'] =  parameters.get('enabled', True)
                                result['Source'] = df_pathlist_str

                                final_result = pd.concat([final_result, result], ignore_index=True)
                                print(f"{datetime.now()} : [SUCCESS] Function call completed")
                    else:
                        print(f"{datetime.now()} : Parameter set is disabled for . {selected_function}")
            else:
                print(f"{datetime.now()} : Function '{function_path}' not found or not callable.")
        else:
            print(f"{datetime.now()} : Function is disabled {function_info}")
    
    #Decision of output performed here, saving or returning call :)
    if output_csv is not None:
        final_result.to_csv(output_csv, index=False)
        print(f"{datetime.now()} : [SUCCESS] Saved output in {output_csv}")
    else:
        print("--------------------------------------------------------------")
        print(f"{datetime.now()} : [SUCCESS] Processed the output according to the JSON file, handle the processed output by either storing the result in a variable for later use or displaying it on the screen.")
        return final_result

#if __name__ == "__main__":
    #json_config_path = 'https://raw.githubusercontent.com/RajithPrabakaran/DataQualityFrameworkGovernance/main/Files/dq_pipeline_config.json'
    #json_config_path = '/Users/rajithprabhakaran/Library/Mobile Documents/com~apple~CloudDocs/Documents/Python/Python Package/src/DataQualityFrameworkGovernance/DataWorkflow/dq_pipeline_config.json'
    #output_csv = '/Users/rajithprabhakaran/Library/Mobile Documents/com~apple~CloudDocs/Documents/Python/Output.csv'
    #processing_framework(json_config_path, output_csv)
    #print(processing_framework(json_config_path))