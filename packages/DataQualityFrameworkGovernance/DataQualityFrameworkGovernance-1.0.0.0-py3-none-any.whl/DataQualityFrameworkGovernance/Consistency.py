import pandas as pd
from datetime import datetime

dimName = 'Consistency'

def start_end_date_consistency(df, start_date_column_name, end_date_column_name, date_format, calculate='No'):
    df = pd.DataFrame(df)

    #convert date columns to datetime objects
    df['is_' + start_date_column_name] = pd.to_datetime(df[start_date_column_name], errors='coerce',format=date_format).notna()
    df['is_' + end_date_column_name] = pd.to_datetime(df[end_date_column_name], errors='coerce',format=date_format).notna()

    df['Consistency'] = (df['is_' + start_date_column_name] & df['is_' + end_date_column_name]) & (pd.to_datetime(df[start_date_column_name], errors='coerce',format=date_format) <= pd.to_datetime(df[end_date_column_name], errors='coerce',format=date_format))
    consistency_check = (df['is_' + start_date_column_name] & df['is_' + end_date_column_name]) & (pd.to_datetime(df[start_date_column_name], errors='coerce',format=date_format) <= pd.to_datetime(df[end_date_column_name], errors='coerce',format=date_format))

    # Count the number of consistent and inconsistent rows
    consistent_count = consistency_check.sum()
    inconsistent_count = len(df) - consistent_count

    # decision for data or summary
    if calculate == "No":
        df = df
    elif calculate == "Yes":
       _temp_df = pd.DataFrame({
            'DateTime': [datetime.now()],
            'DQ#': 'DQFGCT01',
            'Dataset_name': '[LOCAL]',
            'DQ_Dimension': dimName,
            'DQ_Rule/Function_name': 'start_end_date_consistency',
            'Error_in_JSON': 'No',
            'Error log': 'No error in JSON config',
            'DQ_Rule/Function_description': 'start_end_date_consistency',
            'DQ_Valid_count': [consistent_count],
            'DQ_Invalid_count': [inconsistent_count],
            'DQ_Total_count': [len(df)],
            'DQ_Valid%': (consistent_count / [len(df)])*100,
            'DQ_Invalid%': (inconsistent_count / [len(df)])*100,
            'DQ_Flag_Inclusion': 'Y',
            'Data_enabled':'True',
            'Function_enabled': 'True',
            'Parameter_enabled': 'True',
            'Source': '[LOCAL]'
            })
       df = _temp_df

    return df
