def report(location):
    import pandas as pd

    # Create an empty DataFrame
    columns = ['URN#',
               'Total row(s)', 
               'Total column(s)']

    df = pd.DataFrame(columns=columns)
    new_rows = pd.DataFrame(location)
    report_data = pd.concat([df, new_rows], ignore_index=True)

    return report_data