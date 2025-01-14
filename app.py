import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Настройка страницы
st.set_page_config(
    page_title="Аналитика обращений",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>
    /* Основной заголовок */
    #dashboard-title {
        color: #1f1f1f;
        font-size: 28px;
        font-weight: 600;
        margin-bottom: 24px;
    }

    /* Панель фильтров */
    #time-filters-container {
        background: #ffffff;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 24px;
    }

    /* Кнопки фильтров */
    .filter-button {
        background: #f5f5f5;
        border: none;
        border-radius: 4px;
        color: #333;
        font-size: 14px;
        padding: 8px 16px;
        transition: all 0.3s;
    }
    
    .filter-button:hover {
        background: #2E5BFF;
        color: white;
    }

    /* PDF кнопка */
    .pdf-button-container {
        margin-top: 16px;
    }

    /* Основная метрика */
    #main-metric-container {
        background: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        margin-bottom: 24px;
        position: relative;
        z-index: 2;
    }

    #wait-time-metric {
        font-size: 24px;
        font-weight: 600;
        color: #1f1f1f;
    }

    #wait-time-value {
        font-size: 36px;
        color: #2E5BFF;
    }

    #wait-time-chart {
        height: 200px;
    }

    /* Вторичные метрики */
    #secondary-metrics-container {
        background: rgba(255,255,255,0.95);
        padding: 24px;
        border-radius: 12px;
        margin-top: -12px;
        position: relative;
        z-index: 1;
    }

    .metric-card {
        background: white;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 16px;
    }

    .metric-title {
        font-size: 14px;
        color: #666;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 24px;
        color: #1f1f1f;
        font-weight: 600;
    }

    /* Графики */
    .chart-container {
        background: white;
        padding: 24px;
        border-radius: 8px;
        margin-bottom: 24px;
    }

    .chart-title {
        font-size: 18px;
        color: #1f1f1f;
        margin-bottom: 16px;
    }

    /* Кастомизация Streamlit */
    .st-emotion-cache-18ni7ap {
        padding-top: 0;
    }

    .st-emotion-cache-60r24q {
        background: #fafafa;
    }

    /* Скрытие ненужных элементов */
    .st-emotion-cache-k7vsyb a {
        display: none;
    }
    .st-emotion-cache-3k8syi{
        background:#fff;
    }
    #main-metric-container{
        box-shadow:0 8px 24px rgba(0,0,0,0.0);
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > header{
        z-index:-1;
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi5 > div > div > div > div:nth-child(5)>*{
        border: none;
        background:#ffffff00;
        color: #727272;
    }
    
    /* Удаление границ у кнопок выбора периода */
    .stButton button {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Загрузка данных
@st.cache_data
def load_data():
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    df = pd.DataFrame(data['data'])
    
    # Преобразование строковых дат в datetime
    date_columns = ['Дата и время звонка', 'Время ответа', 'Дата и время решения вопроса']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col])
    
    return df

# Функция фильтрации по времени
def filter_data(df, period):
    now = pd.Timestamp.now()
    if period == 'today':
        return df[df['Дата и время звонка'].dt.date == now.date()]
    elif period == 'week':
        return df[df['Дата и время звонка'] >= (now - pd.Timedelta(days=7))]
    elif period == 'month':
        return df[df['Дата и время звонка'] >= (now - pd.Timedelta(days=30))]
    elif period == 'year':
        return df[df['Дата и время звонка'] >= (now - pd.Timedelta(days=365))]
    return df

def main():
    left_col, right_col = st.columns([1, 2])
    
    with left_col:
        # Заголовок и подзаголовок
        st.markdown('''
            <h1 id="dashboard-title">Панель анализа работы сервиса поддержки</h1>
            <p class="dashboard-subtitle">Интерактивный отчет о работе сервиса поддержки</p>
        ''', unsafe_allow_html=True)
        
        # Фильтры времени
        st.markdown('<div id="time-filters-container">', unsafe_allow_html=True)
        cols = st.columns(4)  # Создаем 4 колонки для кнопок
        
        with cols[0]:
            if st.button('Сегодня', key='today-filter', help='Показать данные за сегодня'):
                st.session_state.period = 'today'
        with cols[1]:
            if st.button('Неделя', key='week-filter', help='Показать данные за неделю'):
                st.session_state.period = 'week'
        with cols[2]:
            if st.button('Месяц', key='month-filter', help='Показать данные за месяц'):
                st.session_state.period = 'month'
        with cols[3]:
            if st.button('Год', key='year-filter', help='Показать данные за год'):
                st.session_state.period = 'year'
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Кнопка PDF
        st.markdown('<div class="pdf-button-container">', unsafe_allow_html=True)
        if st.button('📥 Скачать PDF отчёт', key='download-pdf'):
            pass
        st.markdown('</div>', unsafe_allow_html=True)

    # Загрузка и фильтрация данных
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("Файл data.json не найден!")
        return
    
    if 'period' not in st.session_state:
        st.session_state.period = 'all'
    filtered_df = filter_data(df, st.session_state.period)
    
    # Расчет метрик
    wait_times = (filtered_df['Время ответа'] - filtered_df['Дата и время звонка']).dt.total_seconds() / 60
    avg_wait_time = wait_times.mean()
    
    
    with right_col:
        # Основная метрика и график
        st.markdown('<div id="main-metric-container">', unsafe_allow_html=True)
        metric_cols = st.columns(2)  # Создаем 2 колонки для метрики и графика
        
        with metric_cols[0]:
            st.markdown(f'''
                <div id="wait-time-metric">
                    <div class="metric-title">Среднее время ожидания</div>
                    <div id="wait-time-value">{avg_wait_time:.1f} мин</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with metric_cols[1]:
            daily_wait_times = filtered_df.groupby(filtered_df['Дата и время звонка'].dt.date).agg({
                'Время ответа': lambda x: (x - filtered_df.loc[x.index, 'Дата и время звонка']).mean().total_seconds() / 60
            }).reset_index()
            
            fig_wait = px.line(daily_wait_times, 
                              x='Дата и время звонка', 
                              y='Время ответа',
                              title='')
            fig_wait.update_traces(line_color='#2E5BFF')
            fig_wait.update_layout(
                showlegend=False,
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_wait, use_container_width=True, key='wait-time-chart')
        st.markdown('</div>', unsafe_allow_html=True)

    # Создаем две колонки с соотношением 60/40 для тепловой карты и сводной таблицы
    heatmap_col, summary_col = st.columns([0.6, 0.4])
    
    with heatmap_col:
        st.markdown('''
            <div class="chart-container">
                <div class="chart-title">Объем обращений по времени суток и дням недели</div>
            </div>
        ''', unsafe_allow_html=True)
        
        # Подготовка данных для тепловой карты
        filtered_df['hour'] = filtered_df['Дата и время звонка'].dt.hour
        filtered_df['day_of_week'] = filtered_df['Дата и время звонка'].dt.day_name()
        
        heatmap_data = filtered_df.groupby(['day_of_week', 'hour']).size().unstack()
        
        # Правильный порядок дней недели
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data.reindex(day_order)
        
        # Создание тепловой карты
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='Blues'
        ))
        
        fig_heatmap.update_layout(
            xaxis_title='Час дня',
            yaxis_title='День недели',
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with summary_col:
        st.markdown('''
            <div class="chart-container">
                <div class="chart-title">Сводная статистика</div>
            </div>
        ''', unsafe_allow_html=True)
        
        # Подготовка данных для сводной таблицы
        summary_data = {
            'Метрика': [
                '% типовых запросов',
                'Среднее время ожидания',
                'Количество операторов в смену',
                'Доступность поддержки',
                'Стоимость обработки запроса'
            ],
            'Значение': [
                f"{(len(filtered_df[filtered_df['Тема звонка'] == 'Типовой']) / len(filtered_df) * 100):.1f}%",
                f"{avg_wait_time:.1f} мин",
                "5",  # Пример значения
                "95%",  # Пример значения
                "₽250"  # Пример значения
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        st.table(summary_df.set_index('Метрика'))


if __name__ == "__main__":
    main()