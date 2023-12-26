
# Data Quality Framework Governance (DQFG)

**Data Quality Framework Governance** is a structured approach to assessing, monitoring, and improving the quality of data. An effective **Data Quality Framework** considers these dimensions and integrates them into a structured approach to ensure that data serves its intended purpose, supports informed decision-making, and maintains the trust of users and stakeholders. **Data Quality** is an ongoing process that requires continuous monitoring, assessment, and improvement to adapt to changing data requirements and evolving business needs.



**Example:** To call functions from the library.

	#variable declaration
	df = pd.read_csv('https://raw.githubusercontent.com/RajithPrabakaran/DataQualityFrameworkGovernance/main/Files/ecommerce_dataset.csv')
	meta_member = ["Yes", "N"]

	from  DataQualityFrameworkGovernance  import  Validity as vl
	print(vl.isMetadataMember(df, 'replaced', meta_member,"No"))

## 1. Installation of package
    pip install DataQualityFrameworkGovernance

## 2. JSON configuration

For configuration, consider using online JSON configuration tools such as [markdownlivepreview](https://markdownlivepreview.com), [jsoneditoronline](https://jsoneditoronline.org), or any other tool of your preference.


<details>
<summary><i>Configuration Guidelines</i></summary>

- Ensure that the **DataFrameDictionary** specifies the source for all required datasets in CSV format.
- In the **DataFunctionConfig** section, invoke functions from the library.
- Use the **enabled** parameter, which can be set to True or False, to guide the framework on enabling or disabling specific functionalities.
- Specify the **function_path** to indicate the function name and its path for a particular activity.
- In the **parameters** field, provide the necessary parameters for the function, ensuring that the passed parameters align with the function's expected parameters.
- The **calculate** parameter is crucial; set it to "Yes" to generate a data quality assessment report. While optional in cloud environments, it is recommended to set it to "Yes" for summarizing the data quality assessment report.
- The first parameter in **DataFunctionConfig**, *user_info*, *comments*, etc., is developer comments.

Consider these points during the configuration of the JSON file.

</details>

<details>
<summary><i>Expand to view JSON sample (header)</i></summary>

    {
    "DataFrameDictionary": 
    {
        "data1": {"enabled": true,"data_path": "https://raw.githubusercontent.com/RajithPrabakaran/DataQualityFrameworkGovernance/main/Files/data1.csv"},
        "ecomm_data": {"enabled": true,"data_path": "https://raw.githubusercontent.com/RajithPrabakaran/DataQualityFrameworkGovernance/main/Files/ecommerce_dataset.csv"}
    },

    "DataFunctionConfig":
    [
        {
            "user_info":"Identifying completeness in a column - this line is user remark [OPTIONAL]",
            "enabled": true,
            "function_path": "DataQualityFrameworkGovernance.Completeness.missing_values_in_column",
            "parameters": [{
                "enabled": true,
                "df":"ecomm_data",
                "columnname":"address2",
                "calculate":"Yes"
                }]
        },
        {
            "Comments":"Important: Array list to be called without double quotes outside array list",
            "enabled": true,
            "function_path": "DataQualityFrameworkGovernance.Validity.isMetadataMember",
            "parameters": [{
                "enabled": true,
                "df":"ecomm_data",
                "column_name_to_look":"replaced",
                "array_list":["Yes", "N"],
                "calculate":"Yes"
                }]
        }
    ]
    }

</details>

[View Github JSON sample](https://github.com/RajithPrabakaran/DataQualityFrameworkGovernance/blob/main/Files/dq_pipeline_config.json)

## 3. Run Data Quality Framework (DataWorkflow & DataPipeline)

<details open>
<summary><b>DataWorkflow.DataPipeline</b></summary>

<ul>

<details>
<summary><i>processing_framework</i></summary>

User configures **DataframeDictionary** and **DataFunctionConfig** in JSON file, based on the JSON file, data pipeline tasks will be performed in  processing framework.

	from DataQualityFrameworkGovernance.DataWorkflow import DataPipeline as dp
	
	json_config_file = 'https://raw.githubusercontent.com/RajithPrabakaran/DataQualityFrameworkGovernance/main/Files/dq_pipeline_config.json'
	#output_csv = 'full path of system location to save the output / result - [OPTIONAL, if the result to be saved in a CSV file]'
	
	print(dp.processing_framework(json_config_file))

*The output_csv parameter is optional in 'processing_framework' function, and if specified, the result will be saved **exclusively in CSV file format.** Please provide the full path, including the desired CSV file name, for saving the output.*

*Refer [DataWorkflow](https://github.com/RajithPrabakaran/DataQualityFrameworkGovernance/blob/main/DataQualityFrameworkGovernance.png)*, *[Pre-configured Json](https://raw.githubusercontent.com/RajithPrabakaran/DataQualityFrameworkGovernance/main/Files/dq_pipeline_config.json)*


<details>
<summary><i>View result</i></summary>

|DateTime|DQ#|Dataset_name|DQ_Dimension|DQ_Rule/Function_name|Error_in_JSON|Error log|DQ_Rule/Function_description|DQ_Valid_count|DQ_Invalid_count|DQ_Total_count|DQ_Valid%|DQ_Invalid%|DQ_Flag_Inclusion|Data_enabled|Function_enabled|Parameter_enabled|Source|
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
|2023-12-23 11:44:13.324231|DQFGCP02|ecomm_data|Completeness|DataQualityFrameworkGovernance.Completeness.missing_values_in_column|No|No error in JSON config|"Parameter: df: 'ecomm_data', columnname: 'address2', calculate: 'Yes'"|7|43|50|14.000000000000002|86.0|Y|True|True|True|https://raw.githubusercontent.com/RajithPrabakaran/DataQualityFrameworkGovernance/main/Files/ecommerce_dataset.csv|
|2023-12-23 11:44:13.339754|DQFGCP01|ecomm_data|Completeness|DataQualityFrameworkGovernance.Completeness.missing_values_in_dataset|No|No error in JSON config|"Parameter: df: 'ecomm_data', calculate: 'Yes'"|770|80|50|90.58823529411765|9.411764705882353|Y|True|True|True|https://raw.githubusercontent.com/RajithPrabakaran/DataQualityFrameworkGovernance/main/Files/ecommerce_dataset.csv|
|2023-12-23 11:44:13.361530|DQFGAC01|ecomm_data|Accuracy|DataQualityFrameworkGovernance.Accuracy.accuracy_tolerance_numeric|No|No error in JSON config|"Parameter: df: 'ecomm_data', base_column: 'actual_price', lookup_column: 'discounted_price', tolerance_percentage: '0', calculate: 'Yes'"|0|50|50|0.0|100.0|Y|True|True|True|https://raw.githubusercontent.com/RajithPrabakaran/DataQualityFrameworkGovernance/main/Files/ecommerce_dataset.csv|
|2023-12-23 11:44:13.379107|DQFGAC02|ecomm_data|Accuracy|DataQualityFrameworkGovernance.Accuracy.accurate_number_range|No|No error in JSON config|"Parameter: df: 'ecomm_data', range_column_name: 'actual_price', lower_bound: '1', upper_bound: '1000', calculate: 'Yes'"|50|0|50|100.0|0.0|Y|True|True|True|https://raw.githubusercontent.com/RajithPrabakaran/DataQualityFrameworkGovernance/main/Files/ecommerce_dataset.csv|
|2023-12-23 11:44:13.395435|DQFGAC03|ecomm_data|Accuracy|DataQualityFrameworkGovernance.Accuracy.accurate_datetime_range|No|No error in JSON config|"Parameter: df: 'ecomm_data', range_column_name: 'purchase_datetime', from_date: '2023-05-01', to_date: '2023-05-28', date_format: '%Y-%m-%d', calculate: 'Yes'"|22|28|50|44.0|56.00000000000001|Y|True|True|True|https://raw.githubusercontent.com/RajithPrabakaran/DataQualityFrameworkGovernance/main/Files/ecommerce_dataset.csv|
</details>

</details>
</ul>
</details>

## 4. Data Quality Dimensions

<details>
<summary><b>Accuracy</b></summary>

<ul>

<details>
<summary><i>accuracy_tolerance_numeric</i></summary>

Calculating data quality accuracy of a set of values (base values) by comparing them to a known correct value (lookup value) by setting a user-defined tolerance percentage, applicable for numeric values.

	from  DataQualityFrameworkGovernance  import  Accuracy as ac
	print(ac.accuracy_tolerance_numeric(dataframe, 'base_column', 'lookup_column', tolerance_percentage))

</details>

<details>
<summary><i>accurate_number_range</i></summary>

Number range ensures that data values are accurate and conform to expected values or constraints. It is applicable to a variety of contexts, including exam scores, weather conditions, pricing, stock prices, age, income, speed limits for vehicles, water levels, and numerous other scenarios.

	from  DataQualityFrameworkGovernance  import  Accuracy as ac
	print(ac.accurate_number_range(dataframe, 'range_column_name', lower_bound, upper_bound))

	Example:
	print(ac.accurate_number_range(df, 'Age', 4, 12))
	(Output will extract the age between 4(lower bound) and 12 (upper bound) from column 'Age' in the dataset 'df')

</details>

<details>
<summary><i>accurate_datetime_range</i></summary>

The datetime range filter guarantees the accuracy and adherence of data values to predetermined criteria or constraints. It is applicable to a variety of contexts, including capturing outliers in date of birth, age and many more.

	from  DataQualityFrameworkGovernance  import  Accuracy as ac
	print(ac.accurate_datetime_range(Dataframe, 'range_column_name', 'from_date', 'to_date', 'date_format'))

	Example:
	print(ac.accurate_datetime_range(df, 'Date', '2023-01-15', '2023-03-01', '%Y-%m-%d'))

**Important**: Specify date format in *'%Y-%m-%d %H:%M:%S.%f'*  ***(It can be specified in any format aligned to source date format).***

</details>

</ul>
</details>

<details>
<summary><b>Completeness</b></summary>

<ul>

<details>
<summary><i>missing_values_in_column</i></summary>

Summary of missing values in each column.

	from  DataQualityFrameworkGovernance  import  Completeness as cp
	print(cp.missing_values_in_column(dataframe))

</details>

<details>
<summary><i>missing_values_in_dataset</i></summary>

Summary of missing values in a dataset.

	from  DataQualityFrameworkGovernance  import  Completeness as cp
	print(cp.missing_values_in_dataset(dataframe))

</details>

</ul>
</details>

<details>
<summary><b>Consistency</b></summary>

<ul>

<details>
<summary><i>start_end_date_consistency</i></summary>

If data in two columns is consistent, check if the "Start Date" and "End Date" column are in the correct chronological order. 

	from  DataQualityFrameworkGovernance  import  Consistency as ct
	#print(ct.start_end_date_consistency(dataframe, 'start_date_column_name', 'end_date_column_name', date_format))
	
	df = pd.read_csv('https://raw.githubusercontent.com/RajithPrabakaran/DataQualityFrameworkGovernance/main/Files/ecommerce_dataset.csv')
	print(ct.start_end_date_consistency(df, 'purchase_datetime', 'refund_date','%Y-%m-%d %H:%M:%S'))

**Important**: Specify date format in *'%Y-%m-%d %H:%M:%S.%f'*  ***(It can be specified in any format aligned to source date format).***

</details>

</ul>
</details>
  

<details>
<summary><b>Uniqueness</b></summary>

<ul>

<details>
<summary><i>duplicate_rows</i></summary>

Identify and display **duplicate** rows in a dataset. 

  
	from  DataQualityFrameworkGovernance  import  Uniqueness as uq
	print(uq.duplicate_rows(dataframe))

</details>

<details>
<summary><i>unique_column_values</i></summary>

Display **unique column values** in a dataset. 

	from  DataQualityFrameworkGovernance  import  Uniqueness as uq
	print(uq.unique_column_values(dataframe, 'column_name'))

</details>

</ul>
</details>


<details>
<summary><b>Validity</b></summary>

<ul>

<details>
<summary><i>validate_age</i></summary>

Validate age based on the criteria in a dataset. 

  	from  DataQualityFrameworkGovernance  import  Validity as vl
	print(vl.validate_age(dataframe, 'age_column', min_age, max_age))

</details>

<details>
<summary><i>vaild_email_pattern</i></summary>

Validating accuracy of email addresses in a dataset by verifying that they follow a valid email format.

	from  DataQualityFrameworkGovernance  import  Validity as vl
	print(vl.valid_email_pattern(dataframe,'email_column_name'))

</details>

<details>
<summary><i>isMetadataMember</i></summary>

If all values in a given array list are present in a specific column of a dataset then it provides a status message indicating whether all names are found or not. **Array values must be within square brackets.**
    
    #Examples
    #array list = ["Tom", "Jerry", "Donald"] - Text
	#array list = [10, 20, 30] - Numeric
	#array list = [True, False] - Boolean
	#array list = [0, 1] - Flag

	from  DataQualityFrameworkGovernance  import  Validity as vl
	df = pd.read_csv('https://raw.githubusercontent.com/RajithPrabakaran/DataQualityFrameworkGovernance/main/Files/ecommerce_dataset.csv')
	meta_member = ["Yes", "N"]
	
	print(vl.isMetadataMember(df, 'replaced', meta_member,"No"))
	#print(vl.isMetadataMember(dataframe, 'column_name_to_look', [array_list]))
	#Parameter 'No' is optional to enable and disable calculation


</details>

<details>
<summary><i>is_column_numeric</i></summary>

 Examines each value in a **column** and appends a new column to the existing column, indicating whether the column is numeric.

	from  DataQualityFrameworkGovernance  import  Validity as vl
	df = pd.read_csv('https://raw.githubusercontent.com/RajithPrabakaran/DataQualityFrameworkGovernance/main/Files/ecommerce_dataset.csv')
    print(vl.is_column_numeric(df, 'actual_price'))
	
	#print(vl.is_column_numeric(dataframe, 'column_name'))

</details>

<details>
<summary><i>contains_number_in_column</i></summary>

 Examines each value in a **column** and appends a new column to the existing column, indicating whether the values contains numeric.

	from  DataQualityFrameworkGovernance  import  Validity as vl
	df = pd.read_csv('https://raw.githubusercontent.com/RajithPrabakaran/DataQualityFrameworkGovernance/main/Files/ecommerce_dataset.csv')
    print(vl.contains_number_in_column(df, 'product_name'))
	
	#print(vl.contains_number_in_column(dataframe, 'column_name'))

</details>

<details>
<summary><i>is_number_in_dataset</i></summary>

Examines each value in a **dataset** and appends a new column for each existing column, indicating whether the values are numeric.

	from  DataQualityFrameworkGovernance  import  Validity as vl
	print(vl.is_number_in_dataset(dataframe))

	#Example for specific column selection
	is_number_in_dataset(dataframe[['column1','column7']])

</details>

<details>
<summary><i>textonly_in_column</i></summary>

 Examines each value in a **column** and appends a new column to the existing column, indicating whether the values are text. **Result would be false, if text or string contains number.**

	from  DataQualityFrameworkGovernance  import  Validity as vl
	df = pd.read_csv('https://raw.githubusercontent.com/RajithPrabakaran/DataQualityFrameworkGovernance/main/Files/ecommerce_dataset.csv')
    print(vl.textonly_in_column(df,'product_description'))

	#print(vl.textonly_in_column(dataframe, 'column_name'))

</details>

<details>
<summary><i>is_text_in_dataset</i></summary>

Examines each value in a **dataset** and appends a new column for each existing column, indicating whether the values are text. **Result would be false, if text or string contains number.**

	from  DataQualityFrameworkGovernance  import  Validity as vl
	print(vl.is_text_in_dataset(dataframe))

	#Example for specific column selection
	is_text_in_dataset(dataframe[['column1','column7']])

</details>

<details>
<summary><i>is_date_in_column</i></summary>

 Examines each value in a **column** and appends a new column to the existing column, indicating whether the values are in date time, in a speciifed format.

	from  DataQualityFrameworkGovernance  import  Validity as vl
	print(vl.is_date_in_column(dataframe,'column_name', date_format))

**Important**: Specify date format in *'%Y-%m-%d %H:%M:%S.%f'*  ***(It can be specified in any format aligned to source date format).***

</details>

<details>
<summary><i>is_date_in_dataset</i></summary>

 Examines each value in a **dataset** and appends a new column for each existing column, indicating whether the values are in date time, in a speciifed format.

	from  DataQualityFrameworkGovernance  import  Validity as vl
	df = pd.read_csv('https://raw.githubusercontent.com/RajithPrabakaran/DataQualityFrameworkGovernance/main/Files/ecommerce_dataset.csv')
	print(vl.is_date_in_dataset(df,'%Y-%m-%d %H:%M:%S'))

    #print(vl.is_date_in_dataset(df[['purchase_datetime','product_name']],'%Y-%m-%d %H:%M:%S'))
	#print(vl.is_date_in_dataset(dataframe, date_format))

	#Example for specific column selection
	is_date_in_dataset(dataframe[['column1','column7']], date_format='%Y-%m-%d')

**Important**: Specify date format in *'%Y-%m-%d %H:%M:%S.%f'*  ***(It can be specified in any format aligned to source date format).***

</details>

</details>


</ul>
</details>

</ul>
</details>

## Optional library structure
<details>
<summary><b>Datastats</b></summary>

<ul>

<details>
<summary><i>count_rows</i></summary>

Count the number of rows in a DataFrame. 
  
  	from  DataQualityFrameworkGovernance  import  Datastats as ds
	print(ds.count_rows(dataframe))

</details>

<details>
<summary><i>count_columns</i></summary>

Count the number of columns in a DataFrame. 

    
  	from  DataQualityFrameworkGovernance  import  Datastats as ds
	print(ds.count_columns(dataframe))

</details>

<details>
<summary><i>count_dataset</i></summary>

Count the number of rows & columns in a DataFrame. 
    
  	from  DataQualityFrameworkGovernance  import  Datastats as ds
	print(ds.count_dataset(dataframe))

</details>

<details>
<summary><i>limit_max_length</i></summary>

 Limits the maximum length of a string to specific length. Example, when applied to the input string 'ABCDEFGH', the function returns 'ABCDE', effectively truncating the original string to the first 5 characters.
    
  	from  DataQualityFrameworkGovernance  import  Datastats as ds
	print(ds.limit_max_length(dataframe, column_name, start_length, length))

	#Example: 'ABCDEFGH' input string returns 'ABCDE'
	print(limit_max_length(df,'column_name',0,5))

</details>

</ul>
</details>


<details>
<summary><b>Data Interoperability</b></summary>

<ul>

<details>
<summary><i>data_migration_reconciliation</i></summary>

**Data migration reconciliation** is a crucial step in ensuring the accuracy and integrity of data transfer between a source and target system. The process involves comparison of the source and target data to identify any disparities. If the columns in both datasets differ, the process returns an ouput to align the source and target dataset. 

**Output of column name mismatch**
| Column | MatchStatus | TableLocation |
|--|--|--|
| Department | Unmatched | Source |
| Departmentt | Unmatched | Target |
| EmployeeID | Matched | NotApplicable |

After structural alignment is confirmed, a comprehensive check is performed by comparing the content of each column. Any inconsistencies between the source and target data are flagged as mismatches. This includes the identification of specific 'column name(s)' where discrepancies occur, 'row number or position' and 'mismatched records' in both the source and target datasets. This comprehensive reporting ensures that discrepancies can be easily located and addressed, promoting data accuracy and the successful completion of the migration process.

  	from  DataQualityFrameworkGovernance  import  Interoperability as io
	print(io.data_migration_reconciliation(source_dataframe, target_dataframe))

	#Example of saving source and target dataframe from csv file

	import pandas as pd
	source_dataframe = pd.read_csv('source_data.csv')
	target_dataframe = pd.read_csv('target_data.csv')

**Result**
| Column | Row no. / Position |Source Data |Target Data |
|--|--|--|--|
| Column name | 2 | 33 | 3 |
| Column name | 289 | Donald Trump | Donald Duck |  

</details>


<details>
<summary><i>data_integration_reconciliation</i></summary>

**Data integration reconciliation** involves combining data from different sources into a unified view. This function compares two datasets, source_dataset and target_dataset, based on a unique identifier, ID. It checks for disparities in each column, cell by cell, between the two datasets. For each mismatch, it identifies the specific column and provides a status of "Matched" or "Mismatched." If the columns in both datasets differ, the process returns an ouput to align the source and target dataset. 

**Example output of column name mismatch**
| Column | MatchStatus | TableLocation |
|--|--|--|
| Department | Unmatched | Source |
| Departmentt | Unmatched | Target |
| EmployeeID | Matched | NotApplicable |

After structural alignment is confirmed, a comprehensive check is performed by comparing the content of each column. Any inconsistencies between the source and target data are flagged as mismatches.

**Parameters:**

**source_dataset:** The source dataset, a DataFrame containing the data to be compared.
**target_dataset:** The target dataset, a DataFrame containing the data to be compared against the source dataset
**ID**: A unique identifier column present in both datasets, used to match rows between the two datasets.

**Return Value:**

**status:** A string indicating the overall comparison status, either "Matched" or "Mismatched."
**mismatched_columns:** A list of columns that have mismatches between the two datasets.

	import pandas as pd
  	from  DataQualityFrameworkGovernance  import  Interoperability as io

	source_dataset = pd.DataFrame({
		'Ordinal': [54, 55, 56, 57],
		'Name': ['Theresa May','Boris Johnson', 'Liz Truss', 'Rishi Sunak'],
		'Monarch': ['Elizabeth II', 'Elizabeth II', 'Elizabeth II & Charles III', 'Charles III']
		})

	target_dataset = pd.DataFrame({
		'Ordinal': [55, 56, 57],
		'Name': ['Boris Johnson', 'Liz Truss', 'Rishi Sunak'],
		'Monarch': ['Elizabeth II', 'Elizabeth II', 'Charles III']
		})

	comparison_results = io.data_integration_reconciliation(source_dataset, target_dataset, 'Ordinal')
	print(comparison_results)


**Result**
| Ordinal | Status | Mismatched_Columns | MergeStatus | Name_source | Name_target | Monarch_source | Monarch_target |
|--|--|--|--|--|--|--|--|
|54|Mismatch|Name, Monarch|left_only|Theresa May|NaN|Elizabeth II|NaN|
|56|Mismatch|Monarch|both| Liz Truss| Liz Truss|Elizabeth II & Charles III|Elizabeth II|
|55|Match|None|both|Boris Johnson|Boris Johnson|Elizabeth II|Elizabeth II|
|57|Match|None|both|Rishi Sunak|Rishi Sunak|Charles III|Charles III|

</details>

<details>
<summary><i>data_consolidation</i></summary>

**Data consolidation** is a process of combining information from multiple datasets to create a unified dataset. This function with three parameters – dataset1, dataset2, and a parameter to determine consolidation direction (0 for rows ,1 for columns), users can choose between consolidating data by rows or columns.

**Compile by Rows (0):**

When choosing compile=0, the function will stack the datasets vertically, effectively appending the rows of dataset2 beneath the rows of dataset1.

**Compile by Columns (1):**

Alternatively, selecting compile=1 will concatenate the datasets side by side, merging columns from dataset2 to the right of those from dataset1.

  	from  DataQualityFrameworkGovernance  import  Interoperability as io

	CompileByColumns = io.data_consolidation(df1, df2,1)
	CompileByRows = io.data_consolidation(df1, df2,0)

</details>

</ul>
</details> 

<details>
<summary><b>Tools</b></summary>

<ul>

<details>
<summary><i>csv_to_json</i></summary>

CSV to JSON converter.

    from DataQualityFrameworkGovernance import Tools as tl
    print(tl.csv_to_json(input_csv_file, output_json_file))

</details>

<details>
<summary><i>json_to_csv</i></summary>

JSON to CSV converter.

    from DataQualityFrameworkGovernance import Tools as tl
    print(tl.json_to_csv(input_json_file, output_csv_file))

</details>

</ul>
</details>

## Supporting python libraries:
  

- Pandas, re, requests

[Homepage](https://github.com/RajithPrabakaran/DataQualityFrameworkGovernance)

[DQ Framework Design](https://github.com/RajithPrabakaran/DataQualityFrameworkGovernance/blob/main/DataQualityFrameworkGovernance.png)

[Github Documentation](https://github.com/RajithPrabakaran/DataQualityFrameworkGovernance)

[Bug Tracker](https://github.com/RajithPrabakaran/DataQualityFrameworkGovernance/issues) 

[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
