from datetime import datetime
import statistics

dimName = 'Completeness'

def missing_values_in_dataset(df, calculate='No'):
    import pandas as pd
    import statistics
    
    # Load dataset
    df = pd.DataFrame(df)
    missing_values = df.isnull().sum()
    valid_entries = df.count()
    total_entries = len(df)

    _df = pd.DataFrame({
        'Total rows': total_entries,
        'Missing values': missing_values,
        'Valid entries': valid_entries,
        'Completeness %': (valid_entries / total_entries)*100
        })
    _df['Total average %'] = statistics.mean(_df['Completeness %'])

    # decision for data or summary
    if calculate == "No":
        df = _df
    elif calculate == "Yes":
       _temp_df = pd.DataFrame({
            'DateTime': [datetime.now()],
            'DQ#': 'DQFGCP01',
            'Dataset_name': '[LOCAL]',
            'DQ_Dimension': dimName,
            'DQ_Rule/Function_name': 'missing_values_in_dataset',
            'Error_in_JSON': 'No',
            'Error log': 'No error in JSON config',
            'DQ_Rule/Function_description': 'missing_values_in_dataset',
            'DQ_Valid_count': (len(df) * len(df.columns)) - df.isnull().sum().sum(),
            'DQ_Invalid_count': df.isnull().sum().sum(),
            'DQ_Total_count': total_entries,
            'DQ_Valid%': statistics.mean((len(df) - df.isnull().sum()) / len(df)) * 100,
            'DQ_Invalid%': statistics.mean(df.isnull().sum() / len(df)) * 100,
            'DQ_Flag_Inclusion': 'Y',
            'Data_enabled':'True',
            'Function_enabled': 'True',
            'Parameter_enabled': 'True',
            'Source': '[LOCAL]'
            })
       df = _temp_df

    return df

def missing_values_in_column(df, columnname, calculate='No'):
    import pandas as pd
    import statistics
    
    # Load dataset
    df = pd.DataFrame(df)
    missing_values = df[columnname].isnull().sum()
    valid_entries = df[columnname].count()
    total_entries = len(df)

    df = pd.DataFrame({
        'Column name': columnname,
        'Total rows': total_entries,
        'Missing values': missing_values,
        'Valid entries': valid_entries,
        'Completeness %': [(valid_entries / total_entries)*100]
        })
    df['Total average %'] = statistics.mean(df['Completeness %'])

    # decision for data or summary
    if calculate == "No":
        df = df
    elif calculate == "Yes":
       _temp_df = pd.DataFrame({
            'DateTime': [datetime.now()],
            'DQ#': 'DQFGCP02',
            'Dataset_name': '[LOCAL]',
            'DQ_Dimension': dimName,
            'DQ_Rule/Function_name': 'missing_values_in_column',
            'Error_in_JSON': 'No',
            'Error log': 'No error in JSON config',
            'DQ_Rule/Function_description': 'missing_values_in_column',
            'DQ_Valid_count': valid_entries,
            'DQ_Invalid_count': missing_values,
            'DQ_Total_count': total_entries,
            'DQ_Valid%': (valid_entries / total_entries)*100,
            'DQ_Invalid%': (missing_values)/(total_entries)*100,
            'DQ_Flag_Inclusion': 'Y',
            'Data_enabled':'True',
            'Function_enabled': 'True',
            'Parameter_enabled': 'True',
            'Source': '[LOCAL]'
            })
       df = _temp_df

    return df
