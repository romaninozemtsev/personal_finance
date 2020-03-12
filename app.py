import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('personal/my_transactions.csv')
df['amount'] = df['amount'].abs()
df['date'] = pd.to_datetime(df['date'])

df_by_cat = df[df['type']=='debit'][['root_category', 'amount']].groupby(['root_category']).sum().sort_values(by='amount', ascending=False)
df_by_cat = df_by_cat.reset_index()

df_by_merchant = df[df['type']=='debit'][['merchant', 'amount']].groupby(['merchant']).sum().sort_values(by='amount', ascending=False)
df_by_merchant = df_by_merchant.reset_index()


import matplotlib.pyplot as plt
import matplotlib.dates as mdates

spending_per_day_df = df[df['type']=='debit'].set_index('date').resample('D').sum()
#fig, ax = plt.subplots(figsize=(15,7))
# ax.xaxis_date()
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
# ax.bar(t_df.index, t_df['amount'])

app.layout = html.Div(children=[
    html.H1(children='My spendings'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    html.Div([
        html.Div(children=[
            dcc.Graph(
                id='pie_by_category',
                figure=go.Figure(data=[go.Pie(labels=df_by_cat['root_category'], values=df_by_cat['amount'])])
            )      
        ], className='four columns'),
        html.Div(children=[
            dcc.Graph(
                id='pie_by_merchant',
                figure=go.Figure(data=[go.Pie(labels=df_by_merchant['merchant'], values=df_by_cat['amount'])])
            ) 
        ], className='four columns'),
        html.Div(children=[
             
        ], className='four columns')
    ], className='row'),
    dcc.Graph(
        id='spending_over_time',
        figure=go.Figure(data=[go.Bar(x=spending_per_day_df.index, y=spending_per_day_df['amount'])])
    ),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
