import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate sample data
def generate_sample_data(n_days=100):
    dates = pd.date_range(start=datetime.now() - timedelta(days=n_days), 
                         end=datetime.now(), 
                         freq='D')
    
    products = ['Laptop', 'Phone', 'Tablet']
    data = []
    
    for date in dates:
        for product in products:
            sales = np.random.randint(10, 100)
            revenue = sales * np.random.uniform(500, 1500)
            data.append({
                'date': date,
                'product': product,
                'sales': sales,
                'revenue': revenue
            })
    
    return pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Generate data
df = generate_sample_data()

# Create visualizations
sales_by_product = px.bar(
    df.groupby('product')['sales'].sum().reset_index(),
    x='product',
    y='sales',
    title='Total Sales by Product'
)

revenue_trend = px.line(
    df.groupby('date')['revenue'].sum().reset_index(),
    x='date',
    y='revenue',
    title='Daily Revenue Trend'
)

# Define the layout
app.layout = html.Div(
    className='container mx-auto p-8',
    children=[
        html.H1('Sales Analytics Dashboard', 
                className='text-3xl font-bold mb-8 text-center'),
        
        # Metrics Row
        html.Div(
            className='grid grid-cols-3 gap-4 mb-8',
            children=[
                html.Div(
                    className='bg-white p-6 rounded-lg shadow',
                    children=[
                        html.H3('Total Sales', className='text-lg font-medium text-gray-700'),
                        html.P(f"{df['sales'].sum():,.0f}", 
                              className='text-2xl font-bold text-blue-600')
                    ]
                ),
                html.Div(
                    className='bg-white p-6 rounded-lg shadow',
                    children=[
                        html.H3('Total Revenue', className='text-lg font-medium text-gray-700'),
                        html.P(f"${df['revenue'].sum():,.2f}", 
                              className='text-2xl font-bold text-green-600')
                    ]
                ),
                html.Div(
                    className='bg-white p-6 rounded-lg shadow',
                    children=[
                        html.H3('Average Daily Sales', className='text-lg font-medium text-gray-700'),
                        html.P(f"{df.groupby('date')['sales'].sum().mean():,.1f}", 
                              className='text-2xl font-bold text-purple-600')
                    ]
                ),
            ]
        ),
        
        # Product Filter
        html.Div(
            className='bg-white p-4 rounded-lg shadow mb-8',
            children=[
                html.Label('Select Product:', className='block text-sm font-medium text-gray-700'),
                dcc.Dropdown(
                    id='product-filter',
                    options=[{'label': product, 'value': product} for product in df['product'].unique()],
                    value=df['product'].unique()[0],
                    className='mt-1'
                )
            ]
        ),
        
        # Charts
        html.Div(
            className='grid grid-cols-2 gap-4',
            children=[
                html.Div(
                    className='bg-white p-4 rounded-lg shadow',
                    children=[
                        dcc.Graph(figure=sales_by_product)
                    ]
                ),
                html.Div(
                    className='bg-white p-4 rounded-lg shadow',
                    children=[
                        dcc.Graph(figure=revenue_trend)
                    ]
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run(server=True, debug=True)
