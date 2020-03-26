import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt


def vis_future(data, col):
    plt.figure()
    plt.plot(data['ds'], data['yhat'], label='predicted')
    plt.plot(data['ds'], data['y'], label='actual')
    plt.legend()
    plt.title(str(col))
    plt.show()

# Forecasting future
# TODO Tune parameters on seasonality and
#  add additional external predictors to get the accurate model
def predict_future(data, col):
    data_pred = pd.DataFrame()
    data_pred['ds'] = data['Date']
    data_pred['y'] = data[col]

    m = Prophet()
    m.fit(data_pred)
    future = m.make_future_dataframe(periods=14)
    future_pred = m.predict(future)
    plt.figure()
    m.plot(future_pred)
    plt.figure()
    m.plot_components(future_pred)
    vis_data = future_pred[['ds', 'yhat']]
    vis_data.loc[:, 'y'] = data_pred['y']
    vis_future(vis_data, col)
    return future_pred


def main():
    # Import data from github
    data = pd.read_csv('data/time_series_19-covid-Confirmed.csv')

    # Reshape data to convert date columns to date rows
    melted_data = data.melt(id_vars=['Province/State','Country/Region','Lat','Long'], var_name='Date')

    # Separate each country into individual column
    pivoted_data = melted_data.pivot_table(index='Date', columns='Country/Region', values='value', aggfunc='sum')
    p = pivoted_data.reset_index()
    p['Date'] = pd.to_datetime(p['Date'])

    # Align all countries by the first day of the first case reported
    p = p.sort_values(by=['Date'])
    ind = p.ne(0).idxmax()

    df = pd.DataFrame()
    for col in p.columns:
        if col != 'Date':
            d = p.loc[ind[col]:, col]
            d.reset_index(drop=True, inplace=True)
            df = pd.concat([df, d], ignore_index=True, axis=1)

    df.columns = pivoted_data.columns
    data_reshaped = df.iloc[:, :-1]
    data_reshaped['Date'] = p['Date'].reset_index(drop=True)

    # Save data
    data_reshaped.to_csv('data/data_reshaped.csv')

    # Forecasting the future with FBProphet
    predict_future(data_reshaped, 'US')


if __name__ == '__main__':
    main()

