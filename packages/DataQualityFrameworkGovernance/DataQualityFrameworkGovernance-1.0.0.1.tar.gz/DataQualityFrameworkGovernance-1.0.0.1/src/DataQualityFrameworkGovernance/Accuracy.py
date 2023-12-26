#Accuracy
from datetime import datetime

dimName = 'Accuracy'

def accuracy_tolerance_numeric(df, base_column, lookup_column, tolerance_percentage, calculate='No'):
    import pandas as pd
    df = pd.DataFrame(df)

    # Calculate the accuracy of each value
    accuracy = [1 - abs((calculated - correct) / correct) for calculated, correct in zip(df[base_column], df[lookup_column])]

    # Convert accuracy to percentages
    accuracy_percentage = [acc * 100 for acc in accuracy]

    # Check if accuracy is within a tolerance level
    tol_percentage = tolerance_percentage
    within_tolerance = [(100 - tol_percentage) <= acc <= (100 + tol_percentage) for acc in accuracy_percentage]

    df = pd.DataFrame({
        'Base Values': df[base_column],
        'Lookup Values': df[lookup_column],
        'Accuracy (%)': accuracy_percentage,
        'Tolerance (%)': (100 - tol_percentage),
        f'{"Within tolernance"} ({tol_percentage})%' : within_tolerance
        })
    
    # decision for data or summary
    if calculate == "No":
        df = df
    elif calculate == "Yes":
       _temp_df = pd.DataFrame({
            'DateTime': datetime.now(),
            'DQ#': 'DQFGAC01',
            'Dataset_name': '[LOCAL]',
            'DQ_Dimension': dimName,
            'DQ_Rule/Function_name': 'accuracy_tolerance_numeric',
            'Error_in_JSON': 'No',
            'Error log': 'No error in JSON config',
            'DQ_Rule/Function_description': 'accuracy_tolerance_numeric',
            'DQ_Valid_count': [df[f'{"Within tolernance"} ({tol_percentage})%'].sum()],
            'DQ_Invalid_count': [(~df[f'{"Within tolernance"} ({tol_percentage})%']).sum()],
            'DQ_Total_count': [len(df)],
            'DQ_Valid%': [(df[f'{"Within tolernance"} ({tol_percentage})%'].sum())/(len(df))*100],
            'DQ_Invalid%': [((~df[f'{"Within tolernance"} ({tol_percentage})%']).sum())/(len(df))*100],
            'DQ_Flag_Inclusion': 'Y',
            'Data_enabled': 'True',
            'Function_enabled': 'True',
            'Parameter_enabled': 'True',
            'Source':' [LOCAL]'
            })
       df = _temp_df

    return df

def accurate_number_range(df, range_column_name, lower_bound, upper_bound, calculate='No'):
    import pandas as pd
    df = pd.DataFrame(df)
    # Check if the number is within the expected range
    df['Within Range'] = (df[range_column_name] >= lower_bound) & (df[range_column_name] <= upper_bound)
    
    # decision for data or summary
    if calculate == "No":
        df = df
    elif calculate == "Yes":
       _temp_df = pd.DataFrame({
            'DateTime': datetime.now(),
            'DQ#': 'DQFGAC02',
            'Dataset_name': '[LOCAL]',
            'DQ_Dimension': dimName,
            'DQ_Rule/Function_name': 'accurate_number_range',
            'Error_in_JSON': 'No',
            'Error log': 'No error in JSON config',
            'DQ_Rule/Function_description': 'accurate_number_range',
            'DQ_Valid_count': [df['Within Range'].sum()],
            'DQ_Invalid_count': [(~df['Within Range']).sum()],
            'DQ_Total_count': [len(df)],
            'DQ_Valid%': [(df['Within Range'].sum())/(len(df))*100],
            'DQ_Invalid%': [((~df['Within Range']).sum())/(len(df))*100],
            'DQ_Flag_Inclusion': 'Y',
            'Data_enabled':'True',
            'Function_enabled': 'True',
            'Parameter_enabled': 'True',
            'Source': '[LOCAL]'
            })
       df = _temp_df   
    
    return df

def accurate_datetime_range(df, range_column_name, from_date, to_date, date_format, calculate='No'):
    import pandas as pd
    df = pd.DataFrame(df)
    df['Within Range'] = (df[range_column_name] >= from_date) & (df[range_column_name] <= to_date)

    # decision for data or summary
    if calculate == "No":
        df = df
    elif calculate == "Yes":
       _temp_df = pd.DataFrame({
            'DateTime': datetime.now(),
            'DQ#': 'DQFGAC03',
            'Dataset_name': '[LOCAL]',
            'DQ_Dimension': dimName,
            'DQ_Rule/Function_name': 'accurate_datetime_range',
            'Error_in_JSON': 'No',
            'Error log': 'No error in JSON config',
            'DQ_Rule/Function_description': 'accurate_datetime_range',
            'DQ_Valid_count': [df['Within Range'].sum()],
            'DQ_Invalid_count': [(~df['Within Range']).sum()],
            'DQ_Total_count': [len(df)],
            'DQ_Valid%': [(df['Within Range'].sum())/(len(df))*100],
            'DQ_Invalid%': [((~df['Within Range']).sum())/(len(df))*100],
            'DQ_Flag_Inclusion': 'Y',
            'Data_enabled':'True',
            'Function_enabled': 'True',
            'Parameter_enabled': 'True',
            'Source': '[LOCAL]'
            })
       df = _temp_df
       
    return df
