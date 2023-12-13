import streamlit as st
import streamlit_shadcn_ui as ui
import datetime

def main():
    
    st.title('Capacity calculator')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        

        tab_selected = ui.tabs(options=['Sprint Capacity', 'Period/Quarter Capacity'], default_value='Sprint Capacity', key="capacity_tab")

        if tab_selected == 'Sprint Capacity':
            total_working_days = st.number_input('Total working day in a normal sprint', min_value=1, max_value=50, value=10, step=1)
            total_contributors = st.number_input('Total number of contributors on team', min_value=1, max_value=10, value=5, step=1)
            average_velocity = st.number_input('Average story point velocity for last 3 sprints', min_value=1, max_value=100, value=25, step=1)
            total_holidays = st.number_input('Total number of holidays during the sprint', min_value=0, max_value=50, value=0, step=1)
            total_days_off = st.number_input('Total days off for all contributors', min_value=0, max_value=50, value=0, step=1)
            
            total_days = total_contributors * total_working_days
            total_day_minus_vancacy = total_days - total_days_off - (total_holidays * total_contributors)            

            percentage_of_possible_work = (total_day_minus_vancacy / total_days) * 100 

            sprint_capacity = (int(percentage_of_possible_work) * average_velocity) / 100

            ui.metric_card(title="Capacity", content=str(int(sprint_capacity)) + " story points", key="card1")


        elif tab_selected == 'Period/Quarter Capacity':

            # Get the current date
            today = datetime.datetime.now()

            # Calculate the start date of the next quarter
            next_quarter_month = ((today.month - 1) // 3 + 1) * 3 + 1
            next_quarter_year = today.year

            if next_quarter_month > 12:
                next_quarter_month -= 12
                next_quarter_year += 1

            next_quarter_start = datetime.date(next_quarter_year, next_quarter_month, 1)

            # Calculate the end date of the next quarter
            next_quarter_end = (next_quarter_start + datetime.timedelta(days=89)).replace(day=31)

            # Define the date input widget with default values
            d = st.date_input(
                "Select a period to calculate capacity",
                (next_quarter_start, next_quarter_end),
                next_quarter_start,
                next_quarter_end,
                format="MM/DD/YYYY",
            )

            # Calculate the number of working days in the selected period
            working_days = 0
            current_date = next_quarter_start
            while current_date <= next_quarter_end:
                if current_date.weekday() < 5:  # Weekdays (Monday to Friday)
                    working_days += 1
                current_date += datetime.timedelta(days=1)

            total_contributors = st.number_input('Total number of contributors on team', min_value=1, max_value=50, value=5, step=1)
            total_holidays = st.number_input('Total number of holidays during this period', min_value=0, max_value=300, value=0, step=1)
            total_days_off = st.number_input('Total days off for all contributors', min_value=0, max_value=300, value=0, step=1)

            period_capacity = (working_days - total_holidays) * total_contributors - total_days_off
            ui.metric_card(title="Capacity", content=str(int(period_capacity)) + " development days", key="card2")





    