import os
import pandas as pd
import numpy as np

##Function to rename & retain columns of interest the df dictionary
def rename_columns_for_year(df, year):
    if "Country or region" in df.columns:
        print(type(df.columns))
        df.rename(
            columns={
                "Country or region": "Country",
                "Score": f"Score_{year}"
            },
            inplace=True,
        )

    elif "Country name" in df.columns:
        df.rename(
            columns={
                "Country name": "Country",
                "Ladder score": f"Score_{year}"
            },
            inplace=True,
        )
    elif "Country" in df.columns:
        column_values = ["Happiness.Score", "Happiness Score", "Happiness score"]
        matched_column = [col for col in df.columns if col in column_values][0]
        df.rename(
                columns={
                    matched_column: f"Score_{year}"
                },
                inplace=True,
            )
    else:
        raise ValueError("Wrong column specified")
    
    required_cols = ["Country", f"Score_{year}"]

    for col in df.columns:
        if col not in required_cols:
            df.drop(col, axis=1, inplace=True)

    return df


## Renaming columns with year suffix within the dict
def rename_and_retain_cols_for_all_dfs(dfs_dict):
    for year, df in dfs_dict.items():
        dfs_dict[year] = rename_columns_for_year(df, year)
    return dfs_dict

## Importing all data files into dict 
def import_all_dfs(years, path):
    
    dfs_dict = {}
    
    for year in years:
        file_name = f"{year}.csv"
        file_path = os.path.join(path, file_name)
        
        if os.path.exists(file_path):
            dfs_dict[year] = pd.read_csv(file_path)
        else:
            print(f"No file found for year {year}")
    
    return dfs_dict

def add_fuzzy_matches_key_column(df, fuzzy_dict_ref, column_key):
 
    df[column_key] = ''  
    
    for key, values in fuzzy_dict_ref.items():
        for value in values:
    
            df.loc[df['Country'] == value, column_key] = key
    
    return df

def merge_dfs(df1, df2):
    
    diffs_cols = df1.columns.difference(df2.columns)
    only_diff_in_subsets = df1[diffs_cols]
    merged_diff_df = pd.merge(df2, only_diff_in_subsets, left_index=True, right_index=True, how='inner')
    
    return merged_diff_df