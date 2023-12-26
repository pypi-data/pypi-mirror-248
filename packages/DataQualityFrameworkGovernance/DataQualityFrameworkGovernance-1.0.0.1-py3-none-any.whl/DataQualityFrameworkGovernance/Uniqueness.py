# Uniqueness
import pandas as pd
from datetime import datetime

dimName = "Uniqueness"

def duplicate_rows(df, calculate='No'):
    import pandas as pd
    df = pd.DataFrame(df)
    df['IsDuplicate'] = df.duplicated(keep=False).map({True: True, False: False})
    df = df.sort_values(by=['IsDuplicate'] + list(df.columns), ascending = False)

    total_duplicates = df['IsDuplicate'].sum()
    valid_duplicates = df[df['IsDuplicate']]['IsDuplicate'].sum()

    total_rows = len(df)
    valid_percentage = (valid_duplicates / total_rows) * 100
    invalid_percentage = (total_rows - valid_duplicates) / total_rows * 100

    # decision for data or summary
    if calculate == "No":
        df = df
    elif calculate == "Yes":
       _temp_df = pd.DataFrame({
            'DateTime': [datetime.now()],
            'DQ#': 'DQFGUQ01',
            'Dataset_name': '[LOCAL]',
            'DQ_Dimension': dimName,
            'DQ_Rule/Function_name': 'duplicate_rows',
            'Error_in_JSON': 'No',
            'Error log': 'No error in JSON config',
            'DQ_Rule/Function_description': 'duplicate_rows',
            'DQ_Valid_count': [valid_duplicates],
            'DQ_Invalid_count': [total_rows - valid_duplicates],
            'DQ_Total_count': [len(df)],
            'DQ_Valid%': valid_percentage,
            'DQ_Invalid%': invalid_percentage,
            'DQ_Flag_Inclusion': 'Y',
            'Data_enabled':'True',
            'Function_enabled': 'True',
            'Parameter_enabled': 'True',
            'Source': '[LOCAL]'
            })
       df = _temp_df

    return df

def unique_column_values(df, col_name, calculate='No'):
    import pandas as pd

    df = pd.DataFrame(df)
    # Check the uniqueness of values
    df['IsUnique'] = df[col_name].duplicated(keep=False)
    df = df.sort_values(by=['product_id'] + list(df.columns))

    total_duplicates = df['IsUnique'].sum()
    valid_duplicates = df[df['IsUnique']]['IsUnique'].sum()

    total_rows = len(df)
    valid_percentage = (valid_duplicates / total_rows) * 100
    invalid_percentage = (total_rows - valid_duplicates) / total_rows * 100

    # decision for data or summary
    if calculate == "No":
        df = df
    elif calculate == "Yes":
       _temp_df = pd.DataFrame({
            'DateTime': [datetime.now()],
            'DQ#': 'DQFGUQ02',
            'Dataset_name': '[LOCAL]',
            'DQ_Dimension': dimName,
            'DQ_Rule/Function_name': 'unique_column_values',
            'Error_in_JSON': 'No',
            'Error log': 'No error in JSON config',
            'DQ_Rule/Function_description': 'unique_column_values',
            'DQ_Valid_count': [valid_duplicates],
            'DQ_Invalid_count': [total_rows - valid_duplicates],
            'DQ_Total_count': [len(df)],
            'DQ_Valid%': valid_percentage,
            'DQ_Invalid%': invalid_percentage,
            'DQ_Flag_Inclusion': 'Y',
            'Data_enabled':'True',
            'Function_enabled': 'True',
            'Parameter_enabled': 'True',
            'Source': '[LOCAL]'
            })
       df = _temp_df

    return df
