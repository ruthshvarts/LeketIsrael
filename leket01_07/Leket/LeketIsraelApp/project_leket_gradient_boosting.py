import sqlite3
import pandas as pd
import pandasql as ps
from django.contrib.auth.models import User
from django.conf import settings

def run():
    all_records = User.objects.all()
    # print("Connection Successful",conn)
    results = []
    for user in all_records:
        results.append(user.username)
    return results




# import sqlite3
# import pandas as pd
# import pandasql as ps
# from . import models
# from django.conf import settings
import os
import sys
# sys.path.append(
#     os.path.join(os.path.dirname(__file__), 'C:\\Users\\shirl\\LeketProject\\Leket')
# )
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Leket.settings")
# import django
# from django.conf import settings
# django.setup()
# from  LeketIsraelApp.models import Users1

# import sys
# import os
# import django
#
# sys.path.append('C:/Users/shirl/LeketProject/Leket')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'Leket.settings'
# django.setup()

print('------------------ Here are the users in USER database: ------------------')
results = run()
for name in results: print(name)
# from LeketIsraelApp.models import Users1
# # from Leket.LeketIsraelApp.models import Users1
# all_locations = Users1.object.all()
# # first_location = Locations.object.get(id=1)
# print (first_location.name())
# first_location.save()

#
# def check():
#     print("hello")
#     all_records = models.Users1.objects.all()
    # print("Connection Successful",conn)
    # print(all_records)

# conn = sqlite3.connect('db.sqlite3')
# df = pd.read_sql('SELECT * FROM LeketIsraelApp_input_for_prediction', conn)
# print(df.head())
# raw_df = pd.read_csv('Farmers_hebrew.csv')
#
# #raw_df.info()
#
# raw_df["date"] = pd.to_datetime(raw_df["date"]) # convert object type to date type
# raw_df.info()
#
# raw_df.drop(raw_df[raw_df['amount_kg'] == 0].index, inplace = True)
# # df = raw_df[raw_df['type'].notna()]
#
# raw_df.head()
#
# # import yearly rain data from 'https://data.gov.il/dataset/481/resource/c141f389-e1c8-45b9-b041-ad9565a38fbc?inner_span=True'
# # rain_df = pd.read_csv('new_isr_rain_yearly_web.csv')
# # remove unnecessery columns
# # rain_df = rain_df[["stn_num", "time_obs", "rain_ttl"]] # stn_num = station_number
# # filter only relevant years
# # rain_df.drop(rain_df[rain_df['time_obs'] < 2010].index, inplace = True)
# # rename columns
# # rain_df.rename(columns = {'time_obs':'year', 'rain_ttl':'yearly_rain_in_mm'}, inplace = True)
# # rain_df.head()
#
# # import df to conver station number to city \ area from 'https://data.gov.il/dataset/481/resource/83841660-b9c4-4ecc-a403-d435b3e8c92f'
# # this csv has also yearly rain but not sure its up to date
# # stn_tbl = pd.read_csv('new_stn_table_web.csv')
# # remove unnecessery columns
# # stn_tbl = stn_tbl[["stn_num", "stn_name"]]
#
# # join rain_df and stn_tbl
# # rain_df = pd.merge(rain_df, stn_tbl, on=['stn_num'])
# # remove station number
# # rain_df = rain_df[['year', 'yearly_rain_in_mm', 'stn_name']]
# # rain_df.head()
#
# # OPTIONAL SECTION:
#
# # add weather API to the model
#
# # import json
# # import requests
# # "url = "https://api.ims.gov.il/v1/Envista/stations
# # { = headers
# # 'Authorization': 'ApiToken XXXXXXXX'
# # }
# # response = requests.request("GET", url, headers=headers)
# # data= json.loads(response.text.encode('utf8'))
# # print (data)
#
# q1= """
#   SELECT
#     count (distinct missionID) as num_of_orders,
#     strftime('%Y', date) year,
#     strftime('%W', date) week,
#     area,
#     location,
#     farmerID,
#     type,
#
#     sum(amount_kg) as sum_amount_kg
#   FROM raw_df
#   GROUP BY 2,3,4,5,6,7
# """
# df = ps.sqldf(q1)
#
# # df.dtypes
#
# df.info()
#
# # raw_df['date'].describe()
#
# df.head()
#
# # import pandas as pd
#
# # # Load the data into a Pandas dataframe
#
# # # Group the data by year and calculate the mean sum_amount_kg for each year
# # mean_by_year = df.groupby('year')['sum_amount_kg'].mean()
#
# # # Loop through the rows of the dataframe and assign the predicted sum_amount_kg based on the mean value for the year
# # for index, row in df.iterrows():
# #     year = row['year']
# #     df.at[index, 'predicted_sum_amount_kg'] = mean_by_year[year]
#
# # # Print the resulting dataframe
# # df
#
# """This model is based on a moving average, since the mean value for each year is calculated based on all the data from that year. The resulting dataframe will contain a new column predicted_sum_amount_kg with the predicted values for each row.
#
# #linear regression
# """
#
# # import pandas as pd
# # from sklearn.linear_model import LinearRegression
#
#
# # # Select the columns to use as features
# # features = ['num_of_orders', 'year', 'week', 'area', 'location', 'farmerID', 'type']
#
# # # Split the data into a training set and a test set
# # X_train = df[features]
# # y_train = df['sum_amount_kg']
#
# # # Fit the linear regression model to the training data
# # model = LinearRegression()
# # model.fit(X_train, y_train)
#
# # # Use the trained model to make predictions on the test data
# # y_pred = model.predict(X_test)
#
# """This will train a linear regression model on the sum_amount_kg column using the other columns as features. You can then use the model.predict() method to make predictions on new data.
#
# Keep in mind that this is just one possible approach to predicting the sum_amount_kg column, and there are many other machine learning algorithms and techniques that you could try as well. The choice of algorithm and features will depend on the characteristics of your data and the specific prediction task you are trying to accomplish.
#
# *italicized text*#Gradient Boosting
# """
#
# from sklearn.ensemble import GradientBoostingRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import OneHotEncoder
# from sklearn.compose import ColumnTransformer
# from sklearn.pipeline import Pipeline
# from sklearn.impute import SimpleImputer
#
# # Define the columns of categorical variables
# cat_cols = ['type', 'location','farmerID', 'area']
# num_cols = ['year', 'week']
#
# # define the preprocessing steps
# # column transformer to apply different preprocessing step to different columns
# # Handle unknown categories in OneHotEncoder by ignoring them
# preprocessor = ColumnTransformer(
#     transformers=[
#         ('num', SimpleImputer(), num_cols),
#         ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)])
#
# # define the predictor variables and the response variable
# X = df[['type', 'area', 'location', 'farmerID', 'year', 'week']]
# y = df['sum_amount_kg']
#
# # split the data into a training set and a test set
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
# # fit the Gradient Boosting Regressor to the training data
# gb = GradientBoostingRegressor()
#
# # Define the pipeline
# pipe = Pipeline([('preprocessor', preprocessor), ('model', gb)])
# pipe.fit(X_train, y_train)
#
# # make predictions on the test set
# y_pred = pipe.predict(X_test)
#
# # add the predictions as a new column to the test set DataFrame
# X_test['predictions'] = y_pred
#
# # evaluate the model performance
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# print("\033[33mMean Absolute Error:\033[0m", mean_absolute_error(y_test, y_pred))
# print("\033[33mMean Squared Error:\033[0m", mean_squared_error(y_test, y_pred))
# print("\033[33mR-squared:\033[0m", r2_score(y_test, y_pred))
#
# X_test['predictions'].describe()
#
# # Add a column for predictions
# df['predictions'] = pipe.predict(df[['type', 'area', 'location', 'farmerID', 'year', 'week']])
# df