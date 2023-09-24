import pandas as pd
# from tensorflow.keras.models import create_model

def parse_incomes(filepath: str):
    incomes = pd.read_csv(filepath)
    incomes_periodic = incomes[incomes['periodicity'] != 'none']
    incomes_nonperiodic = incomes[incomes['periodicity'] == 'none']

    incomes_nonperiodic['date'] = pd.to_datetime(incomes_nonperiodic['date'])
    headers = {'date': []}
    incomes_nonperiodic_grouped = pd.DataFrame({
        **headers,
        **{category: [] for category in incomes_nonperiodic['category'].unique()}
    })

    sum = 0
    prev_month = None

    for date in sorted(incomes_nonperiodic["date"].unique()):
      year = date.year 
      month = date.month 
      m = (month, year)

      if prev_month == None or m != prev_month:
        sum = 0
        prev_month = m

      temp = incomes_nonperiodic[incomes_nonperiodic["date"] == date].groupby(["category"]).agg({'amount': 'sum'})
      temp = temp.transpose()
      temp['total'] = temp.sum(axis=1) + sum
      sum = temp['total']
      temp['date'] = date
      incomes_nonperiodic_grouped = pd.concat([incomes_nonperiodic_grouped, temp])

    incomes_nonperiodic_grouped = incomes_nonperiodic_grouped.set_index('date')
    incomes_nonperiodic_grouped = incomes_nonperiodic_grouped.fillna(0)
    return incomes_nonperiodic_grouped  

def parse_expenses(filepath):
    expenses_df = pd.read_csv(filepath)

    expenses_periodic = expenses_df[expenses_df['periodicity'] != 'none']
    expenses_nonperiodic = expenses_df[expenses_df['periodicity'] == 'none']

    # Convert date to datetime to be able to group by month
    expenses_nonperiodic['date'] = pd.to_datetime(expenses_nonperiodic['date'])
    expenses_nonperiodic_grouped = pd.DataFrame()

    sum = 0
    prev_month = None

    for date in sorted(expenses_nonperiodic["date"].unique()):
      year = date.year 
      month = date.month 

      m = (month, year)

      if prev_month == None or m != prev_month:
        sum = 0
        prev_month = m

      total = expenses_nonperiodic[expenses_nonperiodic["date"] == date]['amount'].sum() + sum
      temp = pd.DataFrame({
          'total': [total],
          'date': [date]
      })
      sum = total
      expenses_nonperiodic_grouped = pd.concat([expenses_nonperiodic_grouped, temp])

    expenses_nonperiodic_grouped = expenses_nonperiodic_grouped.set_index('date')
    expenses_nonperiodic_grouped = expenses_nonperiodic_grouped.fillna(0)
    return expenses_nonperiodic_grouped
        
parse_incomes('./incomes.csv')
# def model(x_data, y_data):
#     model = create_model()
#
#     model.add(GRU(units=512,
#                   return_sequences=True,
#                   input_shape(None, x_))
#
#     model.add(Dense(y_data.reshape(-1,1).shape[1], activation='sigmoid'))
#
#     try:
#         model.load_weights(path_checkpoint)
#     except Exception as error:
#         print("Error trying to load checkpoint.")
#         print(error)
#
#    return model.predict(x_data) 
