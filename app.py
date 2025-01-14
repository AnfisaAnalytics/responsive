import streamlit as st
import plotly.express as px
import psycopg2
import pandas as pd

# Настройка стилей и темы
st.set_page_config(
    page_title="Анализ времени ответа менеджеров",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Пользовательские CSS стили
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stMetric:hover {
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    .st-emotion-cache-1629p8f h1 {
        color: #1f77b4;
        text-align: center;
        padding-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        margin-bottom: 2rem;
    }
    .st-emotion-cache-10trblm {
        color: #2c3e50;
        margin-top: 2rem;
    }
    div[data-testid="stDataFrame"] {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

def connect_to_db():
    try:
        conn = psycopg2.connect(
        host="rc1a-p8bp15mmxsfwpbt0.mdb.yandexcloud.net",
        port="6432",
        database="db1",
        user="test_user",
        password="j2M{CnnFq@"
        )
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

def get_response_times():
    """Выполнить запрос для получения времени ответа"""
    query = """
    WITH ranked_messages AS (
    SELECT
    m.message_id,
    m.type,
    m.entity_id,
    m.created_by,
    m.created_at,
    mg.name_mop,
    LAG(m.type) OVER (PARTITION BY m.entity_id ORDER BY m.created_at) as prev_type,
    LAG(m.created_at) OVER (PARTITION BY m.entity_id ORDER BY m.created_at) as prev_created_at
    FROM test.chat_messages m
    LEFT JOIN test.managers mg ON m.created_by = mg.mop_id
    ORDER BY m.entity_id, m.created_at
    ),
    response_times AS (
    SELECT
    rm.,
    CASE
    WHEN rm.type = 'outgoing_chat_message'
    AND rm.prev_type = 'incoming_chat_message' THEN
    CASE
    -- Если предыдущее сообщение было в нерабочее время (00:00-09:30)
    WHEN TO_TIMESTAMP(rm.prev_created_at)::time < TIME '09:30:00'
    AND TO_TIMESTAMP(rm.created_at)::time >= TIME '09:30:00' THEN
    EXTRACT(EPOCH FROM (
    TO_TIMESTAMP(rm.created_at) -
    TO_TIMESTAMP(rm.prev_created_at)::date + INTERVAL '9 hours 30 minutes'
    ))
    -- Если текущий ответ после рабочего времени
    WHEN TO_TIMESTAMP(rm.created_at)::time > TIME '00:00:00' THEN
    EXTRACT(EPOCH FROM (
    TO_TIMESTAMP(rm.created_at) -
    TO_TIMESTAMP(rm.prev_created_at)
    ))
    ELSE NULL
    END
    ELSE NULL
    END as response_time_seconds
    FROM ranked_messages rm
    )
    SELECT
    name_mop,
    COUNT() as total_responses,
    ROUND(AVG(response_time_seconds)/60, 2) as avg_response_time_minutes,
    ROUND(MIN(response_time_seconds)/60, 2) as min_response_time_minutes,
    ROUND(MAX(response_time_seconds)/60, 2) as max_response_time_minutes
    FROM response_times
    WHERE response_time_seconds IS NOT NULL
    AND name_mop IS NOT NULL
    GROUP BY name_mop
    ORDER BY avg_response_time_minutes;
    """

try:
    conn = connect_to_db()
    if conn:
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    return None
except Exception as e:
    print(f"Ошибка выполнения запроса: {e}")
    return None

st.set_page_config(page_title="Анализ времени ответа менеджеров", layout="wide")

st.title("Анализ времени ответа службы поддержки")

# Добавляем описание
st.markdown("""
    <div style='background-color: #e8f4f9; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem;'>
        <h4 style='color: #1f77b4;'>О дашборде</h4>
        <p>Этот дашборд показывает анализ эффективности работы операторов службы поддержки, 
        включая время ответа и количество обработанных обращений.</p>
    </div>
""", unsafe_allow_html=True)

# Получение данных
df = get_response_times()

if df is not None:
    # Основные метрики с улучшенным стилем
    st.markdown("<h3 style='text-align: center; color: #2c3e50;'>Ключевые показатели</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👥 Всего менеджеров", len(df))
    with col2:
        st.metric("⏱️ Среднее время ответа (мин)", f"{df['avg_response_time_minutes'].mean():.2f}")
    with col3:
        st.metric("📝 Всего обращений", f"{df['total_responses'].sum():,}")

    # Графики с улучшенным стилем
    st.markdown("<h3 style='text-align: center; color: #2c3e50; margin-top: 2rem;'>Визуализация данных</h3>", 
                unsafe_allow_html=True)
    
    # График среднего времени ответа
    fig1 = px.bar(
        df,
        x='name_mop',
        y='avg_response_time_minutes',
        title='Среднее время ответа по менеджерам',
        labels={
            'name_mop': 'Менеджер', 
            'avg_response_time_minutes': 'Среднее время ответа (минуты)'
        },
        color='avg_response_time_minutes',
        color_continuous_scale='RdYlBu_r'
    )
    fig1.update_layout(
        plot_bgcolor='white',
        xaxis_tickangle=-45,
        hoverlabel=dict(bgcolor="white"),
        margin=dict(t=50, l=0, r=0, b=0)
    )
    st.plotly_chart(fig1, use_container_width=True)

    # График количества ответов
    fig2 = px.bar(
        df,
        x='name_mop',
        y='total_responses',
        title='Количество обработанных обращений по менеджерам',
        labels={
            'name_mop': 'Менеджер', 
            'total_responses': 'Количество обращений'
        },
        color='total_responses',
        color_continuous_scale='Viridis'
    )
    fig2.update_layout(
        plot_bgcolor='white',
        xaxis_tickangle=-45,
        hoverlabel=dict(bgcolor="white"),
        margin=dict(t=50, l=0, r=0, b=0)
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Детальная таблица данных
    st.markdown("<h3 style='text-align: center; color: #2c3e50;'>Детальная статистика по менеджерам</h3>", 
                unsafe_allow_html=True)
    
    styled_df = df.rename(columns={
        'name_mop': 'Менеджер',
        'total_responses': 'Всего обращений',
        'avg_response_time_minutes': 'Среднее время ответа (мин)',
        'min_response_time_minutes': 'Минимальное время ответа (мин)',
        'max_response_time_minutes': 'Максимальное время ответа (мин)'
    })
    
    st.dataframe(
        styled_df,
        hide_index=True,
        column_config={
            "Всего обращений": st.column_config.NumberColumn(format="%d"),
            "Среднее время ответа (мин)": st.column_config.NumberColumn(format="%.2f"),
            "Минимальное время ответа (мин)": st.column_config.NumberColumn(format="%.2f"),
            "Максимальное время ответа (мин)": st.column_config.NumberColumn(format="%.2f")
        }
    )
else:
    st.error("Не удалось получить данные из базы данных. Пожалуйста, проверьте подключение.")

