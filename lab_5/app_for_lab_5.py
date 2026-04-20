import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px


# тут у мене налаштування сторінки щоб було гарно
st.set_page_config(page_title="Floral VHI Explorer", page_icon="🌸", layout="wide")


# тут завантаження данних з лаби 2 
@st.cache_data
def load_and_clean_data(folder_path="data"):

    #це функція з 1.ipynb, адаптована для Streamlit.
    #Завдяки @st.cache_data вона виконується лише один раз, 
    #а не при кожному натисканні кнопок.

    noaa_to_ua = {
        1: 22, 2: 24, 3: 23, 4: 25, 5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21,
        11: 9, 12: 26, 13: 10, 14: 11, 15: 12, 16: 13, 17: 14, 18: 15, 19: 16,
        20: 27, 21: 17, 22: 18, 23: 6, 24: 1, 25: 2, 26: 7, 27: 5
    }
    
    ua_names = {
        1: 'Вінницька', 2: 'Волинська', 3: 'Дніпропетровська', 4: 'Донецька',
        5: 'Житомирська', 6: 'Закарпатська', 7: 'Запорізька', 8: 'Івано-Франківська',
        9: 'Київська', 10: 'Кіровоградська', 11: 'Луганська', 12: 'Львівська',
        13: 'Миколаївська', 14: 'Одеська', 15: 'Полтавська', 16: 'Рівненська',
        17: 'Сумська', 18: 'Тернопільська', 19: 'Харківська', 20: 'Херсонська',
        21: 'Хмельницька', 22: 'Черкаська', 23: 'Чернівецька', 24: 'Чернігівська',
        25: 'Республіка Крим', 26: 'Київ (місто)', 27: 'Севастополь (місто)'
    }
    
    all_df = []
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    
    # перевірка існування папки 
    if not os.path.exists(folder_path):
        st.error(f"Папку '{folder_path}' не знайдено! Необхідно покласти CSV файли в папку data поруч з app.py")
        return pd.DataFrame()

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            filepath = os.path.join(folder_path, filename)
            noaa_id = int(filename.split('_')[2])
            
            # це на випадок якщо завантажився файл для всієї України, тобто ID=0
            if noaa_id == 0: continue 
                
            ua_id = noaa_to_ua[noaa_id]
            df = pd.read_csv(filepath, header=1, names=headers)
            
            if 'empty' in df.columns:
                df = df.drop(columns=['empty'])
                
            df['Year'] = df['Year'].astype(str).str.replace('<tt><pre>', '').str.replace('</pre></tt>', '').str.strip()
            df = df[df['Year'].str.isnumeric()]
            df['Year'] = df['Year'].astype(int)
            df['Week'] = df['Week'].astype(int)
            
            # конвертуємо всі потрібні індекси
            for col in ['VCI', 'TCI', 'VHI']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
            df = df.dropna()
            df = df[df['VHI'] > 0]
            
            df['Area_ID'] = ua_id
            df['Area_Name'] = ua_names[ua_id]
            all_df.append(df)
            
    if not all_df:
        return pd.DataFrame()
        
    return pd.concat(all_df, ignore_index=True)

# завантажуємо дані
df = load_and_clean_data()

if df.empty:
    st.stop() #якщо даних немає то зупиняємось


# тут у нас блок коду зі скиданням фільтрів 
# спочатку встановлюємо початкові значення в session_state, якщо їх ще немає
if 'defaults_set' not in st.session_state:
    st.session_state.index_opt = 'VCI'
    st.session_state.region_opt = 'Вінницька'
    st.session_state.week_opt = (1, 52)
    st.session_state.year_opt = (int(df['Year'].min()), int(df['Year'].max()))
    st.session_state.sort_asc = False
    st.session_state.sort_desc = False
    st.session_state.defaults_set = True

def reset_filters():        #ця штука скидає фільтри до стандартних значень
    st.session_state.index_opt = 'VCI'
    st.session_state.region_opt = 'Вінницька'
    st.session_state.week_opt = (1, 52)
    st.session_state.year_opt = (int(df['Year'].min()), int(df['Year'].max()))
    st.session_state.sort_asc = False
    st.session_state.sort_desc = False


# нарешті частина з інтерфейсом
st.title("🌸 Дослідження NOAA даних")
st.markdown("Візуалізація вегетаційних індексів (VCI, TCI, VHI) по областях України.")

col_filters, col_content = st.columns([1, 3])

with col_filters:
    st.header("🌷 Фільтри")
    
    # хочу зазначити що усі віджети прив'язані до session_state через параметр key
    selected_index = st.selectbox("Оберіть індекс:", ['VCI', 'TCI', 'VHI'], key='index_opt')
    
    # тут ми сортуємо назви областей за алфавітом для зручності
    regions_list = sorted(df['Area_Name'].unique())
    selected_region = st.selectbox("Оберіть область:", regions_list, key='region_opt')
    
    selected_weeks = st.slider("Інтервал тижнів:", min_value=1, max_value=52, key='week_opt')
    selected_years = st.slider("Інтервал років:", 
                               min_value=int(df['Year'].min()), 
                               max_value=int(df['Year'].max()), 
                               key='year_opt')
    
    st.markdown("---")
    st.markdown("**Сортування таблиці**")
    sort_asc = st.checkbox("За зростанням", key='sort_asc')
    sort_desc = st.checkbox("За спаданням", key='sort_desc')
    
    st.markdown("---")
    st.button("Скинути всі фільтри 🌿", on_click=reset_filters)


# ця частина відповідає за фільтрацію та сортування даних 
# якщо детальніше то ми фільтруємо весь датасет за роками та тижнями
mask_time = (
    (df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1]) &
    (df['Week'] >= selected_weeks[0]) & (df['Week'] <= selected_weeks[1])
)
time_filtered_df = df[mask_time].copy()

# тут ми виділяємо дані конкретно для обраної області
region_df = time_filtered_df[time_filtered_df['Area_Name'] == selected_region].copy()

# а це логіка сортування таблиці (з перевіркою конфлікту)
if sort_asc and sort_desc:
    st.warning(" Увага: Обрано обидва види сортування! Таблицю залишено в оригінальному хронологічному порядку. Вимкніть один із чекбоксів.")
elif sort_asc:
    region_df = region_df.sort_values(by=selected_index, ascending=True)
elif sort_desc:
    region_df = region_df.sort_values(by=selected_index, ascending=False)


# ця частина коду відповізає за вкладки з результатами (сама таблиця та графіки )
with col_content:
    tab1, tab2, tab3 = st.tabs(["📋 Відфільтровані дані", "🌺 Часовий ряд (Графік)", "🌼 Порівняння областей"])
    
    with tab1:

        #перша вкладка
        st.subheader(f"Дані для області: {selected_region}")
        display_columns = ['Year', 'Week', 'Area_Name', 'VCI', 'TCI', 'VHI']
        st.dataframe(region_df[display_columns], use_container_width=True)

    with tab2:
        st.subheader(f"Динаміка {selected_index} ({selected_years[0]}-{selected_years[1]} рр.)")
        
        # примітка: для другої вкладки  дані обов'язково мають бути відсортовані за часом, 
        # тому беремо невідсортований `time_filtered_df` для цієї області
        plot_df = time_filtered_df[time_filtered_df['Area_Name'] == selected_region].copy()
        
        # тут ми створюємо зручну вісь X у форматі рік-тиждень
        plot_df['Time'] = plot_df['Year'].astype(str) + "-W" + plot_df['Week'].astype(str).str.zfill(2)
        
        fig1 = px.line(plot_df, x='Time', y=selected_index, 
                       color_discrete_sequence=['#d88fae'],
                       title=f'Зміни {selected_index} для {selected_region}')
        
        fig1.update_layout(xaxis_title="Час (Рік-Тиждень)", yaxis_title=f"Значення {selected_index}")
        # це перестраховка якщо точок дуже багато, ховаємо підписи на осі X, щоб не було мішанини
        if len(plot_df) > 100:
             fig1.update_xaxes(showticklabels=False)
             
        st.plotly_chart(fig1, use_container_width=True)

    with tab3:
        st.subheader(f"Порівняння {selected_index} за вказаний період")
        
        # це у нас третя вкладка з порівнянням: спочатку рахуємо середнє значення обраного індексу для кожної області за обраний час
        comp_df = time_filtered_df.groupby('Area_Name')[selected_index].mean().reset_index()
        comp_df = comp_df.sort_values(by=selected_index)
        
        # підсвічуємо обрану область яскравим кольором, а інші - блідим щоб було зручно помітити
        comp_df['Color'] = np.where(comp_df['Area_Name'] == selected_region, '#c07094', '#e6d3db')
        
        fig2 = px.bar(comp_df, x='Area_Name', y=selected_index, 
                      color='Color', color_discrete_map="identity",
                      title=f'Середнє значення {selected_index} по Україні ({selected_years[0]}-{selected_years[1]})')
        
        fig2.update_layout(xaxis_title="Область", yaxis_title=f"Середній {selected_index}")
        st.plotly_chart(fig2, use_container_width=True)