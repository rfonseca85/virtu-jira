import streamlit as st
import streamlit_shadcn_ui as ui
import datetime
import matplotlib.pyplot as plt
from src.components.capacity_card import capacity_card
import calendar

# Função para Sprint Capacity

def sprint_capacity():
    st.title('Sprint Capacity')
    st.markdown('''<span style="color:#4F8BF9;font-size:1.2rem;">Calcule a capacidade do seu time para o próximo sprint de forma visual e rápida.</span>''', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        total_working_days = st.number_input('Dias úteis no sprint', min_value=1, max_value=50, value=10, step=1)
        total_contributors = st.number_input('Membros do time', min_value=1, max_value=10, value=5, step=1)
        average_velocity = st.number_input('Velocidade média (últimos 3 sprints)', min_value=1, max_value=100, value=25, step=1)
        total_holidays = st.number_input('Feriados no sprint', min_value=0, max_value=50, value=0, step=1)
        total_days_off = st.number_input('Dias de folga (soma do time)', min_value=0, max_value=50, value=0, step=1)
    
    with col2:
        # Cálculos
        total_days = total_contributors * total_working_days
        total_day_minus_vacancy = total_days - total_days_off - (total_holidays * total_contributors)
        percentage_of_possible_work = (total_day_minus_vacancy / total_days) * 100
        sprint_capacity_value = (int(percentage_of_possible_work) * average_velocity) / 100
        # Cards visuais
        capacity_card(
            title="Capacidade do Sprint",
            value=int(sprint_capacity_value),
            unit="story points",
            icon="🚀",
            color="#4F8BF9",
            description=f"{int(percentage_of_possible_work)}% da capacidade total possível"
        )
        capacity_card(
            title="Dias totais disponíveis",
            value=total_day_minus_vacancy,
            unit="dias",
            icon="📅",
            color="#43B97F",
            description=f"{total_days} dias - {total_days_off} folgas - {total_holidays * total_contributors} feriados"
        )
        # Gráfico de pizza
        fig, ax = plt.subplots(figsize=(4, 4))
        labels = ['Dias de trabalho', 'Feriados', 'Folgas']
        values = [total_days - (total_holidays * total_contributors) - total_days_off, total_holidays * total_contributors, total_days_off]
        colors = ['#4F8BF9', '#F9C846', '#F96D6D']
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'fontsize': 12})
        ax.axis('equal')
        st.pyplot(fig)
        st.caption('Distribuição dos dias do sprint')

# Função para Period/Quarter Capacity

def period_capacity():
    st.title('Period/Quarter Capacity')
    st.markdown('''<span style="color:#4F8BF9;font-size:1.2rem;">Calcule a capacidade do time para qualquer período ou trimestre.</span>''', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        # Período padrão: próximo trimestre
        today = datetime.datetime.now()
        next_quarter_month = ((today.month - 1) // 3 + 1) * 3 + 1
        next_quarter_year = today.year
        if next_quarter_month > 12:
            next_quarter_month -= 12
            next_quarter_year += 1
        next_quarter_start = datetime.date(next_quarter_year, next_quarter_month, 1)
        # Corrige: pega o último dia do trimestre
        end_month = next_quarter_month + 2 if next_quarter_month + 2 <= 12 else (next_quarter_month + 2) % 12
        end_year = next_quarter_year if next_quarter_month + 2 <= 12 else next_quarter_year + 1
        last_day = calendar.monthrange(end_year, end_month)[1]
        next_quarter_end = datetime.date(end_year, end_month, last_day)
        period = st.date_input(
            "Selecione o período para calcular a capacidade",
            (next_quarter_start, next_quarter_end),
            next_quarter_start,
            next_quarter_end,
            format="MM/DD/YYYY",
        )
        # Garante que period é uma tupla de datas
        if isinstance(period, tuple) and len(period) == 2:
            start_date, end_date = period
        else:
            start_date = end_date = next_quarter_start
        total_contributors = st.number_input('Membros do time', min_value=1, max_value=50, value=5, step=1)
        total_holidays = st.number_input('Feriados no período', min_value=0, max_value=300, value=0, step=1)
        total_days_off = st.number_input('Dias de folga (soma do time)', min_value=0, max_value=300, value=0, step=1)
    with col2:
        # Calcula dias úteis no período
        working_days = 0
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() < 5:
                working_days += 1
            current_date += datetime.timedelta(days=1)
        total_days = working_days * total_contributors
        total_day_minus_vacancy = total_days - total_days_off - (total_holidays * total_contributors)
        percentage_of_possible_work = (total_day_minus_vacancy / total_days) * 100 if total_days > 0 else 0
        # Cards visuais
        capacity_card(
            title="Capacidade do Período",
            value=int(total_day_minus_vacancy),
            unit="dias de desenvolvimento",
            icon="📈",
            color="#4F8BF9",
            description=f"{int(percentage_of_possible_work)}% da capacidade total possível"
        )
        capacity_card(
            title="Dias totais disponíveis",
            value=total_day_minus_vacancy,
            unit="dias",
            icon="📅",
            color="#43B97F",
            description=f"{total_days} dias - {total_days_off} folgas - {total_holidays * total_contributors} feriados"
        )
        # Gráfico de pizza
        fig, ax = plt.subplots(figsize=(4, 4))
        labels = ['Dias de trabalho', 'Feriados', 'Folgas']
        values = [total_days - (total_holidays * total_contributors) - total_days_off, total_holidays * total_contributors, total_days_off]
        colors = ['#4F8BF9', '#F9C846', '#F96D6D']
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'fontsize': 12})
        ax.axis('equal')
        st.pyplot(fig)
        st.caption('Distribuição dos dias do período')

# Mantém main vazio ou apenas para compatibilidade

def main():
    pass

    