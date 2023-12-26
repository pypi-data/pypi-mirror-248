# Validity

import pandas as pd
from datetime import datetime

dimName = "Validity"

def validate_age(df, age_column, min_age, max_age, calculate='No'):
    import pandas as pd
    df = pd.DataFrame(df)
    df['Age Validity'] = (df[age_column] >= min_age) & (df[age_column] <= max_age)

    valid_count = df['Age Validity'].sum()
    invalid_count = len(df) - valid_count
    total_rows = len(df)

    valid_percentage = (valid_count / total_rows) * 100
    invalid_percentage = (total_rows - valid_count) / total_rows * 100

    # decision for data or summary
    if calculate == "No":
        df = df
    elif calculate == "Yes":
       _temp_df = pd.DataFrame({
            'DateTime': [datetime.now()],
            'DQ#': 'DQFGVL01',
            'Dataset_name': '[LOCAL]',
            'DQ_Dimension': dimName,
            'DQ_Rule/Function_name': 'validate_age',
            'Error_in_JSON': 'No',
            'Error log': 'No error in JSON config',
            'DQ_Rule/Function_description': 'validate_age',
            'DQ_Valid_count': [valid_count],
            'DQ_Invalid_count': [invalid_count],
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

#email valid?
def valid_email_pattern(location,email_column_name, calculate='No'):
    import pandas as pd
    import re

    df = pd.DataFrame(location)

    # Define a regular expression pattern to match valid email addresses
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Check if the email addresses follow the valid format
    df['Valid Email'] = df[email_column_name].apply(lambda x: bool(re.match(email_pattern, x)))

    valid_count = df['Valid Email'].sum()
    invalid_count = len(df) - valid_count
    total_rows = len(df)

    valid_percentage = (valid_count / total_rows) * 100
    invalid_percentage = (total_rows - valid_count) / total_rows * 100

    # decision for data or summary
    if calculate == "No":
        df = df
    elif calculate == "Yes":
       _temp_df = pd.DataFrame({
            'DateTime': [datetime.now()],
            'DQ#': 'DQFGVL02',
            'Dataset_name': '[LOCAL]',
            'DQ_Dimension': dimName,
            'DQ_Rule/Function_name': 'valid_email_pattern',
            'Error_in_JSON': 'No',
            'Error log': 'No error in JSON config',
            'DQ_Rule/Function_description': 'valid_email_pattern',
            'DQ_Valid_count': [valid_count],
            'DQ_Invalid_count': [invalid_count],
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

def isMetadataMember(df, column_name_to_look, array_list, calculate='No'):
    import pandas as pd

    df = pd.DataFrame(df)
    df['isMetadataMember'] = df[column_name_to_look].isin(array_list)

    valid_count = df['isMetadataMember'].sum()
    invalid_count = len(df) - valid_count
    total_rows = len(df)

    valid_percentage = (valid_count / total_rows) * 100
    invalid_percentage = (total_rows - valid_count) / total_rows * 100

    # decision for data or summary
    if calculate == "No":
        df = df
    elif calculate == "Yes":
       _temp_df = pd.DataFrame({
            'DateTime': [datetime.now()],
            'DQ#': 'DQFGVL03',
            'Dataset_name': '[LOCAL]',
            'DQ_Dimension': dimName,
            'DQ_Rule/Function_name': 'isMetadataMember',
            'Error_in_JSON': 'No',
            'Error log': 'No error in JSON config',
            'DQ_Rule/Function_description': 'isMetadataMember',
            'DQ_Valid_count': [valid_count],
            'DQ_Invalid_count': [invalid_count],
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

def contains_number_in_column(df, column_name, calculate='No'):
    df[column_name] = df[column_name].astype(str)
    df['contains_number'] = df[column_name].str.contains('\d', regex=True)

    valid_count = df['contains_number'].sum()
    invalid_count = len(df) - valid_count
    total_rows = len(df)

    valid_percentage = (valid_count / total_rows) * 100
    invalid_percentage = (total_rows - valid_count) / total_rows * 100

    # decision for data or summary
    if calculate == "No":
        df = df
    elif calculate == "Yes":
       _temp_df = pd.DataFrame({
            'DateTime': [datetime.now()],
            'DQ#': 'DQFGVL04',
            'Dataset_name': '[LOCAL]',
            'DQ_Dimension': dimName,
            'DQ_Rule/Function_name': 'contains_number_in_column',
            'Error_in_JSON': 'No',
            'Error log': 'No error in JSON config',
            'DQ_Rule/Function_description': 'contains_number_in_column',
            'DQ_Valid_count': [valid_count],
            'DQ_Invalid_count': [invalid_count],
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

def is_column_numeric(df, column_name, calculate='No'):
    df['is_column_numeric'] = pd.to_numeric(df[column_name], errors='coerce').notna()

    valid_count = df['is_column_numeric'].sum()
    invalid_count = len(df) - valid_count
    total_rows = len(df)

    valid_percentage = (valid_count / total_rows) * 100
    invalid_percentage = (total_rows - valid_count) / total_rows * 100

    # decision for data or summary
    if calculate == "No":
        df = df
    elif calculate == "Yes":
       _temp_df = pd.DataFrame({
            'DateTime': [datetime.now()],
            'DQ#': 'DQFGVL05',
            'Dataset_name': '[LOCAL]',
            'DQ_Dimension': dimName,
            'DQ_Rule/Function_name': 'is_column_numeric',
            'Error_in_JSON': 'No',
            'Error log': 'No error in JSON config',
            'DQ_Rule/Function_description': 'is_column_numeric',
            'DQ_Valid_count': [valid_count],
            'DQ_Invalid_count': [invalid_count],
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

def is_number_in_dataset(df, calculate='No'):
    def is_number(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    for column in df.columns:
        result_series = df[column].apply(lambda x: is_number(x))
        df[f'{column}_is_number'] = result_series

    # decision for data or summary
    if calculate == "No":
        df = df
    elif calculate == "Yes":
       _temp_df = pd.DataFrame({
            'DateTime': [datetime.now()],
            'DQ#': 'DQFGVL06',
            'Dataset_name': '[LOCAL]',
            'DQ_Dimension': dimName,
            'DQ_Rule/Function_name': 'is_number_in_dataset',
            'Error_in_JSON': 'No',
            'Error log': 'No error in JSON config',
            'DQ_Rule/Function_description': 'is_number_in_dataset',
            'DQ_Valid_count': 'NotApplicable',
            'DQ_Invalid_count': 'NotApplicable',
            'DQ_Total_count': [len(df)],
            'DQ_Valid%': 'NotApplicable',
            'DQ_Invalid%': 'NotApplicable',
            'DQ_Flag_Inclusion': 'Y',
            'Data_enabled':'NotApplicable',
            'Function_enabled': 'NotApplicable',
            'Parameter_enabled': 'NotApplicable',
            'Source': '[LOCAL]'
            })
       df = _temp_df

    return df

def textonly_in_column(df, column_name, calculate='No'):
    def contains_only_text(value):
        return all(char.isalpha() or not char.isnumeric() for char in str(value))

    df[f'{column_name}_contains_only_text'] = df[column_name].apply(lambda x: contains_only_text(x))

    valid_count = df[f'{column_name}_contains_only_text'].sum()
    invalid_count = len(df) - valid_count
    total_rows = len(df)

    valid_percentage = (valid_count / total_rows) * 100
    invalid_percentage = (total_rows - valid_count) / total_rows * 100

    # decision for data or summary
    if calculate == "No":
        df = df
    elif calculate == "Yes":
       _temp_df = pd.DataFrame({
            'DateTime': [datetime.now()],
            'DQ#': 'DQFGVL07',
            'Dataset_name': '[LOCAL]',
            'DQ_Dimension': dimName,
            'DQ_Rule/Function_name': 'textonly_in_column',
            'Error_in_JSON': 'No',
            'Error log': 'No error in JSON config',
            'DQ_Rule/Function_description': 'textonly_in_column',
            'DQ_Valid_count': [valid_count],
            'DQ_Invalid_count': [invalid_count],
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

def is_text_in_dataset(df, calculate='No'):
    def is_text(value):
        return str(value).isalpha()

    for column in df.columns:
        result_series = df[column].apply(lambda x: is_text(x))
        df[f'{column}_is_text'] = result_series

    # decision for data or summary
    if calculate == "No":
        df = df
    elif calculate == "Yes":
       _temp_df = pd.DataFrame({
            'DateTime': [datetime.now()],
            'DQ#': 'DQFGVL08',
            'Dataset_name': '[LOCAL]',
            'DQ_Dimension': dimName,
            'DQ_Rule/Function_name': 'is_text_in_dataset',
            'Error_in_JSON': 'No',
            'Error log': 'No error in JSON config',
            'DQ_Rule/Function_description': 'is_text_in_dataset',
            'DQ_Valid_count': 'NotApplicable',
            'DQ_Invalid_count': 'NotApplicable',
            'DQ_Total_count': [len(df)],
            'DQ_Valid%': 'NotApplicable',
            'DQ_Invalid%': 'NotApplicable',
            'DQ_Flag_Inclusion': 'Y',
            'Data_enabled':'NotApplicable',
            'Function_enabled': 'NotApplicable',
            'Parameter_enabled': 'NotApplicable',
            'Source': '[LOCAL]'
            })
       df = _temp_df

    return df

def is_date_in_column(df, column_name, date_format, calculate='No'):
    import pandas as pd
    def is_date(value):
        try:
            pd.to_datetime(value, format=date_format)
            return True
        except (ValueError, TypeError):
            return False

    df[f'{column_name}_is_date'] = df[column_name].apply(lambda x: is_date(x))

    valid_count = df[f'{column_name}_is_date'].sum()
    invalid_count = len(df) - valid_count
    total_rows = len(df)

    valid_percentage = (valid_count / total_rows) * 100
    invalid_percentage = (total_rows - valid_count) / total_rows * 100

    # decision for data or summary
    if calculate == "No":
        df = df
    elif calculate == "Yes":
       _temp_df = pd.DataFrame({
            'DateTime': [datetime.now()],
            'DQ#': 'DQFGVL09',
            'Dataset_name': '[LOCAL]',
            'DQ_Dimension': dimName,
            'DQ_Rule/Function_name': 'is_date_in_column',
            'Error_in_JSON': 'No',
            'Error log': 'No error in JSON config',
            'DQ_Rule/Function_description': 'is_date_in_column',
            'DQ_Valid_count': [valid_count],
            'DQ_Invalid_count': [invalid_count],
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

def is_date_in_dataset(df, date_format, calculate='No'):
    import pandas as pd
    def is_date(value):
        try:
            pd.to_datetime(value, format=date_format)
            return True
        except (ValueError, TypeError):
            return False

    for column in df.columns:
        new_column_name = f'{column}_is_date'
        df.loc[:, new_column_name] = pd.to_datetime(df[column], format=date_format, errors='coerce').notna()

    # decision for data or summary
    if calculate == "No":
        df = df
    elif calculate == "Yes":
       _temp_df = pd.DataFrame({
            'DateTime': [datetime.now()],
            'DQ#': 'DQFGVL10',
            'Dataset_name': '[LOCAL]',
            'DQ_Dimension': dimName,
            'DQ_Rule/Function_name': 'is_date_in_dataset',
            'Error_in_JSON': 'No',
            'Error log': 'No error in JSON config',
            'DQ_Rule/Function_description': 'is_date_in_dataset',
            'DQ_Valid_count': 'NotApplicable',
            'DQ_Invalid_count': 'NotApplicable',
            'DQ_Total_count': [len(df)],
            'DQ_Valid%': 'NotApplicable',
            'DQ_Invalid%': 'NotApplicable',
            'DQ_Flag_Inclusion': 'Y',
            'Data_enabled':'NotApplicable',
            'Function_enabled': 'NotApplicable',
            'Parameter_enabled': 'NotApplicable',
            'Source': '[LOCAL]'
            })
       df = _temp_df

    return df