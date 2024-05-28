'''
    Author: Juan Manuel Abréu
    Date: 05-28-2024
    Description: This script contains the functions to load the data from the source files.
'''

import pandas as pd
from source_file import SOURCE_WEATHER, SOURCE_FOOTBALL

def get_min_something(file_subset, col1, col2, results_col):
    file_subset[results_col] = file_subset[col1] - file_subset[col2]
    value = file_subset.loc[file_subset[results_col].idxmin()]

    return value

def get_min_temperature_spread(file):
    try:
        weather_data = pd.read_csv(file, sep = r"\s+", skiprows = 2,
                                   names = ['Day', 'MxT', 'MnT', 'AvT', 'HDDay', 'AvDP', '1HrP',
                                            'TPcpn', 'WxType', 'PDir', 'AvSp', 'Dir', 'MxS', 'SkyC',
                                            'MxR', 'MnR', 'AvSLP'],
                                    on_bad_lines = 'skip')

        columns_to_keep = ['Day', 'MxT', 'MnT']
        weather_data_subset = weather_data.drop(columns = weather_data.columns.difference(columns_to_keep))
        weather_data_subset['MxT'] = weather_data['MxT'].str.replace('*', '').astype(float)
        weather_data_subset['MnT'] = weather_data['MnT'].str.replace('*', '').astype(float)

        '''
        weather_data_subset['Temp_Sprd'] = weather_data_subset['MxT'] - weather_data_subset['MnT']
        min_temp_sprd = weather_data_subset.loc[weather_data_subset['Temp_Sprd'].idxmin()]
        '''

        min_temp_sprd = get_min_something(weather_data_subset, 'MxT', 'MnT', 'Temp_Sprd')

        return min_temp_sprd['Day']

    except FileNotFoundError as e:
        print(f"Error: {e}")

def get_team_with_smallest_diff(file):
    try:
        football_data = pd.read_csv(file, delim_whitespace = True, skiprows = 1, header = None,
                                   names = ['Equipos', 'Team', 'P', 'W', 'L', 'D', 'F', 'A', 'Pts'],
                                    on_bad_lines = 'skip')

        columns_to_keep = ['Equipos', 'D', 'A']
        football_data_subset = football_data.drop(columns = football_data.columns.difference(columns_to_keep))
        football_data_subset['D'] = football_data['D'].astype(float)
        football_data_subset['A'] = football_data['A'].astype(float)

        '''
        football_data_subset['F-A_Diff'] = football_data_subset['D'] - football_data_subset['A']
        for_against_diff = football_data_subset.loc[football_data_subset['F-A_Diff'].idxmin()]
        '''

        for_against_diff = get_min_something(football_data_subset, 'D', 'A', 'F-A_Diff')

        return for_against_diff['Equipos']

    except FileNotFoundError as e:
        print(f"Error: {e}")

print(get_min_temperature_spread(SOURCE_WEATHER))
print(get_team_with_smallest_diff(SOURCE_FOOTBALL))
