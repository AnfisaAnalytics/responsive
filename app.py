import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Инициализация приложения
app = dash.Dash(__name__)
server = app.server  # Важно для деплоя на Render

# Создаем тестовые данные
df = pd.DataFrame({
    'Фрукт': ['Яблоки', 'Бананы', 'Апельсины', 'Груши'],
    'Количество': [20, 15, 25, 10]
})

# Создаем график
fig = px.bar(df, x='Фрукт', y='Количество', title='Количество фруктов')

# Определяем layout приложения
app.layout = html.Div([
    html.H1('Мое тестовое Dash приложение', className='header'),
    html.P('Это простое приложение для демонстрации работы с Dash'),
    dcc.Graph(
        id='fruit-graph',
        figure=fig
    ),
    html.Div([
        html.H3('О приложении'),
        html.P('Это приложение создано с использованием Dash и опубликовано на Render.com')
    ], className='info-section')
])

if __name__ == '__main__':
    app.run_server(debug=True)
