from django.shortcuts import render
import requests
import json
import numpy as np
import os
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from django.contrib.auth.decorators import login_required
from visualizer.views import stocks_daily

# Create your views here.


@login_required
def stocks_price_predictor(request, symbol):
    context = {'symbol': symbol}
    if request.method == 'POST':
        model = request.POST.get('model')

        if model == 'arima':
            context['output'] = ''
        elif model == 'lstm':

            if os.path.exists('predictor/models/stocks/lstm/' + context['symbol'] + '_lstm_predictor'):
                daily_response = stocks_daily(symbol)
                daily_obj = json.loads(daily_response)
                time_series_daily = daily_obj['Time Series (Daily)']

                data_date = list(time_series_daily.keys())[0]

                data_close_price = [float(time_series_daily[date]['4. close']) for date in
                                    list(time_series_daily.keys())[:20]]
                data_close_price.reverse()

                # print(data_date)
                # print(data_close_price)

                context['ltp'] = data_close_price[-1]
                context['ltd'] = data_date

                np_data_close_price = np.array(data_close_price).reshape(-1, 1)
                scalar = MinMaxScaler()
                normalized_data_close_price = scalar.fit_transform(np_data_close_price)

                print(normalized_data_close_price)
                print(normalized_data_close_price.shape)

                x_input = normalized_data_close_price.reshape(1, 20, 1)

                print(x_input)
                print(x_input.shape)

                price_predictor = load_model('predictor/models/stocks/lstm/' + context['symbol'] + '_lstm_predictor')
                price = price_predictor.predict(x_input)

                context['output'] = scalar.inverse_transform(price)[0][0]
                print(price)

            else:
                context['output'] = context['symbol'] + ' model not found'

        elif model == 'gru':
            context['output'] = ''

        return render(request, 'predictor/stocks_price_predictor.html', context)

    else:
        return render(request, 'predictor/stocks_price_predictor.html', context)
