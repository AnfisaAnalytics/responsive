# app.py
from flask import Flask, render_template
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

app = Flask(__name__)

def generate_sales_data():
    # Генерируем данные за последние 30 дней
    dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(30)]
    data = {
        'date': dates,
        'sales': np.random.normal(1000, 200, 30).astype(int),  # Продажи
        'visitors': np.random.normal(500, 100, 30).astype(int),  # Посетители
        'conversion': np.random.uniform(1, 5, 30).round(2)  # Конверсия
    }
    return pd.DataFrame(data)

def analyze_data(df):
    analysis = {
        'total_sales': int(df['sales'].sum()),
        'avg_daily_sales': int(df['sales'].mean()),
        'total_visitors': int(df['visitors'].sum()),
        'avg_conversion': float(df['conversion'].mean().round(2)),
        'best_day': df.loc[df['sales'].idxmax(), 'date'],
        'worst_day': df.loc[df['sales'].idxmin(), 'date']
    }
    return analysis

@app.route('/')
def index():
    # Генерируем и анализируем данные
    df = generate_sales_data()
    analysis = analyze_data(df)
    
    # Подготавливаем данные для графиков
    chart_data = {
        'dates': df['date'].tolist(),
        'sales': df['sales'].tolist(),
        'visitors': df['visitors'].tolist(),
        'conversion': df['conversion'].tolist()
    }
    
    # Сохраняем данные в файл
    df.to_csv('static/data.txt', index=False)
    
    return render_template('index.html', 
                         analysis=analysis, 
                         chart_data=json.dumps(chart_data))

if __name__ == '__main__':
    app.run(debug=True)
