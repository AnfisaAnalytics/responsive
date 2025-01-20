import dash
from dash import html, dcc
import plotly.express as px
import numpy as np
import pandas as pd

app = dash.Dash(__name__)
server = app.server  # Добавьте эту строку

# Генерируем случайные данные
np.random.seed(42)
x = np.linspace(0, 10, 100)
y = 2 * x + np.random.normal(0, 1.5, 100)

df = pd.DataFrame({
    'x': x,
    'y': y
})

# Создаем график (убрали параметр trendline)
fig = px.scatter(df, x='x', y='y', 
                title='Простой график рассеяния')

# Определяем layout приложения
app.layout = html.Div([
    html.H1('Мое первое Dash приложение',
            style={'textAlign': 'center', 'marginBottom': 30}),
    
    dcc.Graph(
        id='scatter-plot',
        figure=fig
    ),
    
    html.Div([
        html.H4('Описание:'),
        html.P('Это простой график рассеяния. '
               'Данные сгенерированы с использованием линейной функции y = 2x + шум')
    ], style={'marginTop': 20, 'padding': '20px'})
])

if __name__ == '__main__':
    app.run(debug=True)
