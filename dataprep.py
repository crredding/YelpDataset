import pandas as pd
import string

def split_categories(categories):
    '''
    Function to modfy category string into list of cleaned words.

    Parameters:
    -----------
    categories: string -- String containing comma-seperated categories.

    Output:
    -------
    category_split: list -- Cleaned list of category values.
    '''

    try:
        output = categories.split(',')
        return [x.strip().lower() for x in output]
    except:
        return ""

# def drop_columns(df, cols_to_drop=[]):
#     '''
#     Function used to drop multiple columns from dataset.

#     Paramenters:
#     ------------
#     df: DataFrame
#     cols_to_drop: List -- Column names to drop from the dataset

#     Output:
#     -------
#     output: DataFrame -- Datset with columns dropped
#     '''
#     if len(cols_to_drop) < 1:
#         return df
#     else:
#         output = df.copy()
#         for column in cols_to_drop:
#             output = output.drop(column, axis=1)
#     return output

def clean_business_data(df, cols_to_drop=['hours', 'attributes', 'attributes.BusinessParking', 'attributes.HairSpecializesIn', 'attributes.RestaurantsAttire', 'attributes.BestNights',
                       'attributes.Open24Hours', 'attributes.Music', 'attributes.AgesAllowed', 'attributes.BusinessAcceptsCreditCards', 'attributes.DietaryRestrictions']):
    '''
    Function used to clean the business data set.

    Paramenters:
    ------------
    df: DataFrame -- Yelp business dataset
    cols_to_drop: List -- Column names to drop from the dataset

    Output:
    -------
    df: DataFrame -- Cleaned Yelp business dataset
    '''
    # df = drop_columns(df, cols_to_drop)
    df = df.drop(cols_to_drop, axis=1)

    # Likely not necessary, but updating unicode string import issue leading to leading 'u's
    unicode_fix_columns = ['attributes.Alcohol', 'attributes.Smoking', 'attributes.NoiseLevel', 'attributes.BYOBCorkage']

    for column in unicode_fix_columns:
        df[column] = df[column].str.lstrip('u').str.strip()

    # Update names to strip punctuation and lowercase
    df['name'] = df['name'].str.strip().str.lower().str.translate(str.maketrans('', '', string.punctuation))
    
    # Updating corkage to fix duplicate values
    df['attributes.BYOBCorkage'] = df['attributes.BYOBCorkage'].str.split('_').str[0].value_counts()
      
    df['category_split'] = df.apply(lambda row: split_categories(row['categories']), axis=1)

    return df


def clean_review_data(df, cols_to_drop=[]):
    '''
    Function used to clean the business data set.

    Paramenters:
    ------------
    df: DataFrame -- Yelp review dataset
    cols_to_drop: List -- Column names to drop from the dataset

    Output:
    -------
    df: DataFrame -- Cleaned Yelp review dataset
    '''
   
    # df = drop_columns(df, cols_to_drop)
    df = df.drop(cols_to_drop, axis=1)

    # drop duplicates
    df.drop_duplicates('review_id', inplace=True)

    # Removing any additional duplicate reviews from same user with same text and business
    df.drop_duplicates(['business_id', 'user_id', 'text'], inplace=True)

    # Cleaning up text field
    df['text'] = df['text'].str.lstrip('u').str.strip().str.lower().str.translate(str.maketrans('-', ' ', string.punctuation))

    # Removing escaped characters that show up literally
    df['text'] = df['text'].str.translate(str.maketrans(dict([(chr(char), ' ') for char in range(1, 32)])))

    # Removing >1 whitespace chars
    df['text'] = df.apply(lambda row: ' '.join(row['text'].split()), axis=1)

    # Dropping few reviews that are NaN
    df = df[~df['text'].isna()]

    return df