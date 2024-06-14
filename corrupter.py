import pandas as pd
import numpy as np
import random
import re
import string

# String manipulation functions 
def corrupt_spelling(string_type):
    def corrupt(old_string):
        if string_type == 'char':
            candidate_filter = r'[a-z]'
            replacement_possibilities = string.ascii_lowercase
        elif string_type == 'num':
            candidate_filter = r'\d'
            replacement_possibilities = [str(i) for i in range(10)]
        chars = re.findall(candidate_filter, old_string)
        old_char = random.choice(chars)
        possible_replacements = [ch for ch in replacement_possibilities if ch != old_char]
        new_char = random.choice(possible_replacements)
        new_string = re.sub(old_char, new_char, old_string, 1)
        return new_string
    return corrupt

def corrupt_random_swap(list_of_options):
    def corrupt(old_string):
        optional_strings = [string for string in list_of_options if string != old_string]
        new_string = random.choice(optional_strings)
        return new_string
    return corrupt

def corrupt_postcode(postcode_list):
    def corrupt(old_postcode):
        optional_postcodes = [postcode for postcode in postcode_list if postcode != old_postcode]
        start = old_postcode.split(' ')[0]
        end = random.choice(optional_postcodes).split(' ')[1]
        new_postcode = start + ' ' + end
        return new_postcode
    return corrupt

def corrupt_name(name_list):
    def corrupt(old_name):
        optional_names = [name for name in name_list if name != old_name]
        new_name = old_name + '-' + random.choice(optional_names)
        return new_name
    return corrupt

# Application of string manipulators 
def apply_corrupt_to_row(row, field_corruptions):
    corrupted_row = row.copy()
    for col_name, corruption_functions in field_corruptions.items():
        for function in corruption_functions:
            corrupted_row[col_name] = function(corrupted_row[col_name])
    return corrupted_row

def apply_corrupt_to_df(df, field_corruptions):

    df_base = df.copy()
    df_corrupted = df_base.apply(lambda row: apply_corrupt_to_row(row, field_corruptions), axis=1)
    df_corrupted['unique_id'] = df_corrupted['unique_id'].str.replace('-1', '-2')

    final_df = pd.concat([df_base, df_corrupted], ignore_index=True)

    return final_df
