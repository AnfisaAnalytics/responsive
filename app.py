from flask import Flask, render_template, jsonify, request
import pandas as pd
import plotly
import plotly.express as px
import json
import os
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Generate sample data
def generate_sample_data():
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    data = []
    
    categories = ['Category A', 'Category B', 'Category C']
    regions = ['North', 'South', 'East', 'West']
    
    for date in dates:
        for category in categories:
            for region in regions:
                sales = random.randint(100, 1000)
                profit = sales * random.uniform(0.1, 0.3)
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'category': category,
                    'region': region,
                    'sales': sales,
                    'profit': round(profit, 2)
                })
    
    df = pd.DataFrame(data)
    df.to_csv('sales_data.csv', index=False)
    return df

# Load or generate data
def get_data():
    if not os.path.exists('sales_data.csv'):
        df = generate_sample_data()
    else:
        df = pd.read_csv('sales_data.csv')
        df['date'] = pd.to_datetime(df['date'])
    return df

@app.route('/')
def index():
    df = get_data()
    
    # Get unique values for filters
    categories = df['category'].unique().tolist()
    regions = df['region'].unique().tolist()
    
    return render_template('index.html', 
                         categories=categories,
                         regions=regions)

@app.route('/update_charts', methods=['POST'])
def update_charts():
    df = get_data()
    
    # Get filter values
    selected_category = request.form.get('category', 'all')
    selected_region = request.form.get('region', 'all')
    
    # Apply filters
    if selected_category != 'all':
        df = df[df['category'] == selected_category]
    if selected_region != 'all':
        df = df[df['region'] == selected_region]
    
    # Calculate metrics
    total_sales = df['sales'].sum()
    avg_profit = df['profit'].mean()
    
    # Create charts
    sales_by_category = px.bar(
        df.groupby('category')['sales'].sum().reset_index(),
        x='category',
        y='sales',
        title='Sales by Category'
    )
    
    sales_trend = px.line(
        df.groupby('date')['sales'].sum().reset_index(),
        x='date',
        y='sales',
        title='Sales Trend'
    )
    
    profit_by_region = px.pie(
        df.groupby('region')['profit'].sum().reset_index(),
        values='profit',
        names='region',
        title='Profit by Region'
    )
    
    # Convert charts to JSON
    charts = {
        'sales_by_category': json.loads(sales_by_category.to_json()),
        'sales_trend': json.loads(sales_trend.to_json()),
        'profit_by_region': json.loads(profit_by_region.to_json())
    }
    
    return jsonify({
        'charts': charts,
        'metrics': {
            'total_sales': f"${total_sales:,.2f}",
            'avg_profit': f"${avg_profit:,.2f}"
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
