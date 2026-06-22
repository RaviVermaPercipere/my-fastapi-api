def preprocess_dataframe(df):

    timedelta_cols = df.select_dtypes(
        include=['timedelta64[ns]']
    ).columns

    for col in timedelta_cols:
        df[col] = df[col].astype(str)

    return df