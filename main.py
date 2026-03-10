import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as st_go

st.set_page_config(page_title="Streamlit Dashboard", layout="wide")

st.title("Интерактивный дашборд для визуализации данных")

# Загрузка файла
uploaded_file = st.file_uploader("Загрузите Excel или CSV файл", type=['csv', 'xlsx'])

if uploaded_file:
    # Определение формата и чтение
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Предпросмотр данных")
    edited_df = st.data_editor(df)

    # Настройки графиков в боковой панели
    st.sidebar.header("Настройки графика")
    columns = df.columns.tolist()

    x_axis = st.sidebar.selectbox("Выберите ось X", columns)
    y_axes = st.sidebar.multiselect("Выберите колонки для оси Y", [c for c in columns if c != x_axis])

    if y_axes:
        # Создаем фигуру через graph_objects для поддержки нескольких осей
        fig = st_go.Figure()

        for i, col in enumerate(y_axes):
            # Добавляем линию для каждой колонки
            fig.add_trace(st_go.Scatter(
                x=df[x_axis],
                y=df[col],
                name=col,
                yaxis=f"y{i + 1}" if i > 0 else "y"
            ))

        # Настройка макета для отображения нескольких осей
        layout_kwargs = {
            "title": f"Линейный график: {', '.join(y_axes)}",
            "xaxis": {"title": x_axis},
            "yaxis": {"title": y_axes[0]}
        }

        # Динамически добавляем дополнительные оси Y
        for i in range(1, len(y_axes)):
            layout_kwargs[f"yaxis{i + 1}"] = {
                "title": y_axes[i],
                "overlaying": "y",
                "side": "right",
                "anchor": "free",
                "autoshift": True
            }

        fig.update_layout(**layout_kwargs)

        st.plotly_chart(fig, use_container_width=True)
        if st.button("Сохранить график в HTML"):
            filename = f"chart_{x_axis}_{y_axes}.html"
            fig.write_html(filename)
            st.success(f"Файл сохранен как {filename} в папке с проектом")
    else:
        st.info("Выберите хотя бы одну колонку для оси Y в боковой панели.")
else:
    st.info("Ожидание загрузки файла...")