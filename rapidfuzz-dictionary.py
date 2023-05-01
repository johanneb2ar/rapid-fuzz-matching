import pandas as pd
left_df = pd.read_csv('left_dataset.csv')
right_df = pd.read_csv('right_dataset.csv')
left_df = left_df.rename(columns={'entity_id': 'id'})
left_df = left_df.rename(columns={'postal_code': 'zip_code'})
right_df = right_df.rename(columns={'business_id': 'id'})

#define a fucntion to convert dataframe to dictionary while only keep name address and id
def create_dict_from_df(df, selected_columns=['name', 'address']):
    result_dict = {}
    for row_index, row in df.iterrows():
        key = row_index+1
        value = tuple(row[col] for col in selected_columns)
        result_dict[key] = value
    return result_dict

#covert right_df to dictionary
right_dict = create_dict_from_df(right_df)
print(len(right_dict))
for key, value in right_dict.items():
    print(f'{key}: {value}')
    print()
    
#covert left_df to dictionary
left_dict = create_dict_from_df(left_df)
print(len(left_dict))
for key, value in left_dict.items():
    print(f'{key}: {value}')
    print()

from rapidfuzz import fuzz
#define a function to compute matching score between two dicts
def compute_matching_score(left_dict, right_dict):
    score_dict = {}
    for left_key, left_value in left_dict.items():
        for right_key, right_value in right_dict.items():
            if left_value == right_value:
                score_dict[(left_key, right_key)] = 1.0
            else:
                name_score = fuzz.token_sort_ratio(left_value[0], right_value[0])
                address_score = fuzz.token_sort_ratio(left_value[1], right_value[1])
                score = (name_score + address_score) / 200
                if score > 0.8:
                    score_dict[(left_key, right_key)] = score
    return score_dict

compute_matching_score(left_dict,right_dict)


