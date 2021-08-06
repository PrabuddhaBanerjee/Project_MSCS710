import pandas as pd

'''
Default model for reliability.
'''
def airline_reliability(df):
    delay_df = df[['ORIGIN_CITY_NAME','ORIGIN','DEP_DELAY_NEW']].copy()
    delay_df.loc[:,'DEP_DELAY_NEW'] = delay_df['DEP_DELAY_NEW'].astype(int)
    delay_df = delay_df.groupby(['ORIGIN_CITY_NAME','ORIGIN'])['DEP_DELAY_NEW'].mean().reset_index()
    delay_df.loc[:,'DEP_DELAY_NEW'] = delay_df['DEP_DELAY_NEW'] * (30/delay_df['DEP_DELAY_NEW'].max())  # weight 30 %
    
    canc_df = df[['ORIGIN_CITY_NAME','ORIGIN','CANCELLED']].copy()
    canc_df.loc[:,'CANCELLED'] = canc_df['CANCELLED'].astype(int)
    canc_df = canc_df.groupby(['ORIGIN_CITY_NAME','ORIGIN'])['CANCELLED'].mean().reset_index()
    canc_df.loc[:,'CANCELLED'] = canc_df['CANCELLED'] * 70  # weight 70 %

    df = delay_df.merge(canc_df, on=['ORIGIN_CITY_NAME','ORIGIN']).copy()
    df.loc[:,'RELIABILITY'] = 30 - df['DEP_DELAY_NEW'] + 70 - df['CANCELLED']

    df = df[['ORIGIN_CITY_NAME','ORIGIN','RELIABILITY']]
    
    # return only the top ten results
    df = df.sort_values('RELIABILITY', ascending=False)
    df = df.head(10)

    return df.to_json()
