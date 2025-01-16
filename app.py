import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
import pandas as pd
from datetime import datetime, timedelta
import json
import os
from pathlib import Path

# Constants for cache
CACHE_DIR = "cache"
CACHE_FILE = os.path.join(CACHE_DIR, "data_cache.json")
DATA_CACHE_FILE = os.path.join(CACHE_DIR, "response_times.pkl")

# Page Configuration
st.set_page_config(
    page_title="Service Support Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS with new color palette
st.markdown("""
<style>
header{
    z-index:-1 !important;
    height:0 !important;}
/* Main Container */
    .main {
        background-color: #f2f9ff;
        padding: 0.9rem;
    }
#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi5 > div > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div.st-emotion-cache-fplge5.e1f1d6gn3 > div > div > div > div.st-emotion-cache-0.e1f1d6gn0
{background: #fff;
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                box-shadow: rgba(0, 0, 0, 0.12) 0px 1px 3px, rgba(0, 0, 0, 0.24) 0px 1px 2px;
            }
            /* Стили для всех input элементов */
[data-testid*="Input"] input,
[data-testid*="Select"] input {
    background-color: white !important;
}

/* Стили для контейнеров input и select */
[data-testid*="Input"],
[data-testid*="Select"] {
    background-color: white !important;
}

/* Стили для выпадающих списков */
[data-baseweb="popover"],
[data-baseweb="select"] {
    background-color: white !important;
}

/* Стили для календаря */
.DateInput,
.DateInput_input,
.SingleDatePicker,
.SingleDatePickerInput {
    background-color: white !important;
}

/* Стили для multiselect */
[data-baseweb="select"] > div {
    background-color: white !important;
}
.st-emotion-cache-1r4qj8v{
background:#F2F9FE ;}
#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi5 > div > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div.st-emotion-cache-1yycg8b.e1f1d6gn3 > div > div > div > div:nth-child(3) > div > div > div:nth-child(2) > div > div{
box-shadow: rgba(14, 63, 126, 0.04) 0px 0px 0px 1px, rgba(42, 51, 69, 0.04) 0px 1px 1px -0.5px, rgba(42, 51, 70, 0.04) 0px 3px 3px -1.5px, rgba(42, 51, 70, 0.04) 0px 6px 6px -3px, rgba(14, 63, 126, 0.04) 0px 12px 12px -6px, rgba(14, 63, 126, 0.04) 0px 24px 24px -12px;}
#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi5 > div > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div.st-emotion-cache-1yycg8b.e1f1d6gn3 > div > div > div > div:nth-child(3) > div > div > div:nth-child(2) > div{
display:flex;
justify-content:center;}
/* Стили для выпадающего списка */
.stMultiSelect [data-testid="stMultiSelect"] {
    background-color: white !important;
    border-radius: 8px !important;
}
#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi5 > div > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div.st-emotion-cache-1yycg8b.e1f1d6gn3 > div > div > div > div:nth-child(3) > div > div > div:nth-child(2) > div > div{

/* Стили для выбранных элементов в мультиселекте */
.stMultiSelect [data-baseweb="tag"] {
    background-color: #BEDFFC !important;
    border: 1px solid #5A90C4 !important;
    border-radius: 4px !important;
    color: #44361D !important;
}

/* Стили для кнопки удаления в мультиселекте */
.stMultiSelect [data-baseweb="tag"] span[role="button"] {
    color: #44361D !important;
}

/* Стили для опций в выпадающем списке */
.stMultiSelect [role="listbox"] {
    background-color: white !important;
    border: 1px solid #E6C6FA !important;
    border-radius: 8px !important;
}

/* Ховер для опций в выпадающем списке */
.stMultiSelect [role="option"]:hover {
    background-color: #BEDFFC !important;
}

/* Стили для выбранной опции */
.stMultiSelect [aria-selected="true"] {
    background-color: #5A90C4 !important;
    color: white !important;
}

/* Стили для календаря */
[data-testid="stDateInput"] .DateInput_input {
    background-color: white !important;
}

/* Стили для выбранной даты в календаре */
.CalendarDay__selected {
    background-color: #5A90C4 !important;
    border: 1px solid #5A90C4 !important;
}

/* Ховер для дат в календаре */
.CalendarDay:hover {
    background-color: #BEDFFC !important;
    border: 1px solid #5A90C4 !important;
}

/* Стили для диапазона дат */
.CalendarDay__selected_span {
    background-color: #BEDFFC !important;
    border: 1px solid #5A90C4 !important;
    color: #44361D !important;
}

/* Стили для лейблов фильтров */
.stSelectbox label,
[data-testid="stDateInput"] label {
    color: #44361D !important;
    font-weight: 500 !important;
}


#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi5 > div > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div.st-emotion-cache-fplge5.e1f1d6gn3 > div > div > div > div:nth-child(3) > div > button:hover{
color:#14446E;
border:1px solid #14446E;}




#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi5 > div > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div.st-emotion-cache-fplge5.e1f1d6gn3 > div > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div:nth-child(1) > div > div > div > div > div > div > div:hover{
border:1px solid #44361D;}
#\36 5374adc > div > span{
font-size:1.5rem;}
.st-bb{
background-color:#fff;
box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

    #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi5 > div > div > div > div:nth-child(5) > div:nth-child(1) > div > div > div > div:nth-child(1) > div > label > div > div > p{
    font-size:1.5rem
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #44361D;
        font-weight: 600;
    }
    #a7d68e74, #d77b75c6, #62780edb {font-size:1rem;
    text-align:center;
    margin-top:0.6rem;}
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi5 > div > div > div > div.st-emotion-cache-0.e1f1d6gn0 > div > div > div > div.st-emotion-cache-fplge5.e1f1d6gn3 > div{
    }
    /* Metric Cards */
    .metric-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #5A90C4;
    }
    
    .metric-label {
        color: #44361D;
        font-size: 0.875rem;
    }
    
    /* Tables */
    .dataframe {
        width: 100%;
        border: none !important;
    }
    
    .dataframe th {
        background-color: #BEDFFC;
        padding: 0.75rem;
        text-align: left;
        font-weight: 600;
        color: #44361D;
    }
    
    .dataframe td {
        padding: 0.75rem;
        border-bottom: 1px solid #E6C6FA;
    }
    /* Charts */
    .plot-container {
        background-color: white;
        border-radius: 0.5rem;
        padding: 1rem;
        
    }
    .st-b7{
    background-color:#fff;
    }
</style>
""", unsafe_allow_html=True)

def get_connection():
    return psycopg2.connect(
        host="rc1a-p8bp15mmxsfwpbt0.mdb.yandexcloud.net",
        port="6432",
        database="db1",
        user="test_user",
        password="j2M{CnnFq@"
    )

def load_initial_data():
    conn = get_connection()
    try:
        date_query = """
            SELECT
                MIN(TO_TIMESTAMP(created_at)) as min_date,
                MAX(TO_TIMESTAMP(created_at)) as max_date
            FROM test.chat_messages;
        """
        dates = pd.read_sql_query(date_query, conn)
        
        personnel_query = """
            SELECT DISTINCT 
                m.name_mop,
                r.rop_name
            FROM test.managers m
            LEFT JOIN test.rops r ON CAST(m.rop_id AS INTEGER) = r.rop_id
            WHERE m.name_mop IS NOT NULL 
            AND r.rop_name IS NOT NULL
            ORDER BY m.name_mop;
        """
        personnel = pd.read_sql_query(personnel_query, conn)
        
        return (
            dates.iloc[0]['min_date'],
            dates.iloc[0]['max_date'],
            personnel['name_mop'].unique().tolist(),
            personnel['rop_name'].unique().tolist()
        )
    finally:
        conn.close()

def get_response_times(start_date, end_date, selected_managers=None, selected_rops=None):
    conn = get_connection()
    try:
        query = """
            WITH message_blocks AS (
                SELECT 
                    entity_id,
                    created_at,
                    created_by,
                    type,
                    LAG(type) OVER (PARTITION BY entity_id ORDER BY created_at) as prev_type
                FROM test.chat_messages
                WHERE TO_TIMESTAMP(created_at) BETWEEN %s AND %s
            ),
            first_messages AS (
                SELECT *
                FROM message_blocks
                WHERE type != COALESCE(prev_type, 'start')
            ),
            message_pairs AS (
                SELECT
                    m1.entity_id,
                    m1.created_at as client_message_time,
                    m2.created_at as response_time,
                    m2.created_by as responder_id,
                    mg.name_mop,
                    r.rop_name,
                    TO_TIMESTAMP(m2.created_at)::date as response_date,
                    CASE 
                        WHEN TO_TIMESTAMP(m1.created_at)::time >= '00:00:00' AND 
                             TO_TIMESTAMP(m1.created_at)::time < '09:30:00' 
                        THEN 
                            EXTRACT(EPOCH FROM (
                                CASE 
                                    WHEN TO_TIMESTAMP(m2.created_at)::time >= '09:30:00'
                                    THEN TO_TIMESTAMP(m2.created_at) - (TO_TIMESTAMP(m2.created_at)::date + INTERVAL '9 hours 30 minutes')
                                    ELSE INTERVAL '0'
                                END
                            ))/60
                        WHEN TO_TIMESTAMP(m1.created_at)::time >= '00:00:00' AND 
                             TO_TIMESTAMP(m2.created_at)::time < '09:30:00'
                        THEN 0
                        ELSE 
                            EXTRACT(EPOCH FROM (
                                CASE 
                                    WHEN TO_TIMESTAMP(m2.created_at)::time <= '00:00:00'
                                    THEN TO_TIMESTAMP(m1.created_at)::date + INTERVAL '24 hours'
                                    ELSE TO_TIMESTAMP(m2.created_at)
                                END - 
                                CASE 
                                    WHEN TO_TIMESTAMP(m1.created_at)::time < '09:30:00'
                                    THEN TO_TIMESTAMP(m1.created_at)::date + INTERVAL '9 hours 30 minutes'
                                    ELSE TO_TIMESTAMP(m1.created_at)
                                END
                            ))/60
                    END as response_time_minutes
                FROM first_messages m1
                INNER JOIN first_messages m2
                    ON m1.entity_id = m2.entity_id
                    AND m1.type = 'incoming_chat_message'
                    AND m2.type = 'outgoing_chat_message'
                    AND m2.created_at > m1.created_at
                LEFT JOIN test.managers mg ON m2.created_by = mg.mop_id
                LEFT JOIN test.rops r ON CAST(mg.rop_id AS INTEGER) = r.rop_id
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM first_messages m3
                    WHERE m3.entity_id = m1.entity_id
                    AND m3.type = 'outgoing_chat_message'
                    AND m3.created_at > m1.created_at
                    AND m3.created_at < m2.created_at
                )
                {manager_filter}
                {rop_filter}
            )
            SELECT
                name_mop,
                rop_name,
                response_date,
                COUNT(*) as total_responses,
                ROUND(AVG(response_time_minutes)::numeric, 2) as avg_response_minutes,
                ROUND(MIN(response_time_minutes)::numeric, 2) as min_response_minutes,
                ROUND(MAX(response_time_minutes)::numeric, 2) as max_response_minutes,
                ROUND((SUM(CASE WHEN response_time_minutes <= 15 THEN 1 ELSE 0 END) * 100.0 / COUNT(*))::numeric, 2) as sla_percentage,
                SUM(CASE WHEN response_time_minutes <= 5 THEN 1 ELSE 0 END) as responses_under_5min,
                SUM(CASE WHEN response_time_minutes > 5 AND response_time_minutes <= 15 THEN 1 ELSE 0 END) as responses_5_15min,
                SUM(CASE WHEN response_time_minutes > 15 THEN 1 ELSE 0 END) as responses_over_15min
            FROM message_pairs
            WHERE name_mop IS NOT NULL
            AND rop_name IS NOT NULL
            GROUP BY name_mop, rop_name, response_date
            ORDER BY response_date, name_mop;
        """
        
        params = [start_date, end_date]
        manager_filter = ""
        rop_filter = ""
        
        if selected_managers:
            manager_filter = "AND mg.name_mop = ANY(%s)"
            params.append(selected_managers)
        
        if selected_rops:
            rop_filter = "AND r.rop_name = ANY(%s)"
            params.append(selected_rops)
        
        query = query.format(
            manager_filter=manager_filter,
            rop_filter=rop_filter
        )
        
        return pd.read_sql_query(query, conn, params=params)
    finally:
        conn.close()
def create_performance_chart(operator_stats):
    fig = go.Figure()
    
    # Add SLA percentage bars
    fig.add_trace(go.Bar(
        name='SLA %',
        x=operator_stats['Оператор'],
        y=operator_stats['SLA %'],
        marker_color='#5A90C4',
        text=operator_stats['SLA %'].apply(lambda x: f'{x:.1f}%'),
        textposition='auto',
        offsetgroup=1
    ))
    
    # Add total responses bars
    normalized_responses = operator_stats['Обращения'] / operator_stats['Обращения'].max() * 100
    fig.add_trace(go.Bar(
        name='Количество обращений',
        x=operator_stats['Оператор'],
        y=normalized_responses,
        marker_color='#BFA577',
        text=operator_stats['Обращения'].apply(lambda x: f'{x:,}'),
        textposition='auto',
        offsetgroup=2
    ))
    
    fig.update_layout(
        barmode='group',
        plot_bgcolor='#efefef',
        paper_bgcolor='white',
        margin=dict(l=0, r=0, t=20, b=0),
        yaxis=dict(
            title='Показатели эффективности',
            showgrid=True,
            gridcolor='#C3C3C3'
        ),
        xaxis=dict(
            title='',
            showgrid=False,
            tickangle=45  # Наклон подписей для лучшей читаемости
        ),
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig



def main():
    # Load initial data
    min_date, max_date, all_managers, all_rops = load_initial_data()
    
    # Remove padding
    st.markdown("""
        <style>
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 0rem;
                padding-right: 0rem;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Create two main columns: 60% for title, 40% for filters
    col_title, col_filters = st.columns([0.6, 0.4])
    
    with col_title:
        # st.title("")
        st.markdown("### Анализ эффективности работы сервиса поддержки")
    
    
        # Create three equal columns for filters
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            dates = st.date_input(
                "Период",
                value=(min_date.date(), max_date.date()),
                min_value=min_date.date(),
                max_value=max_date.date()
            )
        
        with filter_col2:
            selected_managers = st.multiselect(
                "Менеджеры",
                ["All"] + all_managers,
                default=["All"]
            )
            if "All" in selected_managers:
                selected_managers = all_managers
        
        with filter_col3:
            selected_rops = st.multiselect(
                "Супервайзеры",
                ["All"] + all_rops,
                default=["All"]
            )
            if "All" in selected_rops:
                selected_rops = all_rops
        
        # Get data for PDF
        if len(dates) == 2:
            start_date, end_date = dates
        else:
            start_date = end_date = dates[0]
            
        df = get_response_times(
            start_date,
            end_date,
            selected_managers if selected_managers else None,
            selected_rops if selected_rops else None
        )
        
        if not df.empty:
            # PDF download button on a new line
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="PDF отчет",
                data=csv_data,
                file_name=f'service_support_report_{start_date}_{end_date}.pdf',
                mime='application/pdf'
            )
    
        if df.empty:
            st.warning("Нет данных для выбранных фильтров")
            return
        
        # Create container for visualizations
        operator_stats = df.groupby('name_mop').agg({
            'total_responses': 'sum',
            'avg_response_minutes': 'mean',
            'sla_percentage': 'mean'
        }).reset_index()
        
        operator_stats.columns = ['Оператор', 'Обращения', 'Среднее время (мин)', 'SLA %']
        
        # Performance Chart
        cont0 = st.container()
        with cont0:
            # cont3.markdown("<div class='metrics-container'>", unsafe_allow_html=True)
            cont0.markdown("<div >Показатели эффективности операторов</div>", unsafe_allow_html=True)
            
            fig = create_performance_chart(operator_stats)
            cont0.plotly_chart(fig, use_container_width=True)
            
        
    with col_filters:
        # Определяем общий стиль для всех контейнеров
        st.markdown(
            """
            <style>
            #root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-z5fcl4.ea3mdgi5 > div > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div.st-emotion-cache-1yycg8b.e1f1d6gn3 > div > div > div >div:not(:first-child) {
                background: #fff;
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                box-shadow: rgba(0, 0, 0, 0.12) 0px 1px 3px, rgba(0, 0, 0, 0.24) 0px 1px 2px;
            }
            .metric-value {
                text-align: center;
                color: #5A90C4;
                font-size: 1.8rem;
                font-weight: bold;
                margin: 0.5rem 0;
            }
            .metric-title {
                color: #6A6A6A;
                text-align: center;
                font-size: 1.2rem;
                margin-bottom: 1rem;
            }
            .metric-label {
                text-align: right;
                color: #6A6A6A;
            }
            .metric-number {
                text-align: left;
                color: #5A90C4;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    
        # 1. Контейнер для среднего времени ответа
        cont1 = st.container()
        with cont1:
            cont1.markdown("<div class='metric-title'>Среднее время ответа</div>", unsafe_allow_html=True)
            
            avg_response = df['avg_response_minutes'].mean()
            avg_sla = df['sla_percentage'].mean()
            total_responses = df['total_responses'].sum()
            
            cont1.markdown(f"<div class='metric-value'>{avg_response:.1f} мин</div>", unsafe_allow_html=True)
            
            col1, col2 = cont1.columns(2)
            with col1:
                st.markdown("<div class='metric-label'>SLA</div>", unsafe_allow_html=True)
                st.markdown("<div class='metric-label'>Всего обращений</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='metric-number'>{avg_sla:.1f}%</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='metric-number'>{total_responses:,}</div>", unsafe_allow_html=True)
            
        # 2. Контейнер для статистики операторов
        cont2 = st.container()
        with cont2:
            # cont2.markdown("<div class='metrics-container'>", unsafe_allow_html=True)
            cont2.markdown("<div class='metric-title'>Статистика</div>", unsafe_allow_html=True)
            cont2.dataframe(
                operator_stats,
                hide_index=True,
                column_config={
                    "Оператор": st.column_config.TextColumn("Оператор"),
                    "Обращения": st.column_config.NumberColumn("Обращения", format="%d"),
                    "Среднее время (мин)": st.column_config.NumberColumn("Среднее время (мин)", format="%.1f"),
                    "SLA %": st.column_config.NumberColumn("SLA %", format="%.1f%%")
                },
                height=150
            )
            # cont2.markdown("</div>", unsafe_allow_html=True)
    
        # 3. Контейнер для распределения времени ответа
        cont3 = st.container()
        with cont3:
            # cont3.markdown("<div class='metrics-container'>", unsafe_allow_html=True)
            cont3.markdown("<div class='metric-title'>Распределение времени ответа</div>", unsafe_allow_html=True)
            
            response_distribution = pd.DataFrame({
                'Время ответа': ['До 5 минут', '5-15 минут', 'Более 15 минут'],
                'Количество': [
                    df['responses_under_5min'].sum(),
                    df['responses_5_15min'].sum(),
                    df['responses_over_15min'].sum()
                ]
            })
            
            fig_dist = px.pie(
                response_distribution,
                values='Количество',
                names='Время ответа',
                color_discrete_sequence=['#5A90C4', '#E6C6FA', '#ECCE98'],
                height=250
            )
            fig_dist.update_layout(margin=dict(t=0, b=0))
            cont3.plotly_chart(fig_dist, use_container_width=True)
            # cont3.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
