import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State, ClientsideFunction

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('personal/my_transactions.csv')
df['amount'] = df['amount'].abs()
df['date'] = pd.to_datetime(df['date'])

#fig, ax = plt.subplots(figsize=(15,7))
# ax.xaxis_date()
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
# ax.bar(t_df.index, t_df['amount'])

categories = list(df['root_category'].value_counts().index)
category_options = [
    {"label": x, "value": x} for x in categories
]



app.layout = html.Div(children=[
    html.H1(children='My spendings'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    html.Div([
        dcc.Dropdown(
            id="categories",
            options=category_options,
            multi=True,
            value=categories,
            className="dcc_control",
        )
    ]),
    html.Div([
        html.Div(children=[
            dcc.Graph(
                id='pie_by_category'
            )      
        ], className='four columns'),
        html.Div(children=[
            dcc.Graph(
                id='pie_by_merchant'
            ) 
        ], className='four columns'),
        html.Div(children=[
             
        ], className='four columns')
    ], className='row'),
    dcc.Graph(
        id='spending_over_time'
    ),
    dash_table.DataTable(
        id='transactions-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
    )
])

@app.callback(
    Output("transactions-table", "data"),
    [
        Input("categories", "value")
    ]
)
def make_list_of_transactions(categories):
    dff = df[df['root_category'].isin(categories)]
    return dff.to_dict("rows")

@app.callback(
    Output("spending_over_time", "figure"),
    [
        Input("categories", "value")
    ]
)
def make_spending_over_time(categories):
    dff = df[df['root_category'].isin(categories)]

    spending_per_day_df = dff[dff['type']=='debit'].set_index('date').resample('D').sum()
    return go.Figure(data=[go.Bar(x=spending_per_day_df.index, y=spending_per_day_df['amount'])])

@app.callback(
    Output("pie_by_merchant", "figure"),
    [
        Input("categories", "value")
    ]
)
def make_pie_by_merchant(categories):
    dff = df[df['root_category'].isin(categories)]

    df_by_merchant = dff[dff['type']=='debit'][['merchant', 'amount']].groupby(['merchant']).sum().sort_values(by='amount', ascending=False)
    df_by_merchant = df_by_merchant.reset_index()
    return go.Figure(data=[go.Pie(labels=df_by_merchant['merchant'], values=df_by_merchant['amount'])])


@app.callback(
    Output("pie_by_category", "figure"),
    [
        Input("categories", "value")
    ]
)
def make_pie_by_category(categories):
    dff = df[df['root_category'].isin(categories)]
    df_by_cat = dff[dff['type']=='debit'][['root_category', 'amount']].groupby(['root_category']).sum().sort_values(by='amount', ascending=False)
    df_by_cat = df_by_cat.reset_index()
    return go.Figure(data=[go.Pie(labels=df_by_cat['root_category'], values=df_by_cat['amount'])])




if __name__ == '__main__':
    app.run_server(debug=True)
