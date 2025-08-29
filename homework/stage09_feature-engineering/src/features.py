def add_features(df):
    df['spend_income_ratio'] = df['monthly_spend'] / df['income']
    df['rolling_spend_mean'] = df['monthly_spend'].rolling(window=3, min_periods=1).mean()
    if 'credit_score' in df.columns:
        df['income_x_credit'] = df['income'] * df['credit_score']
    return df