import streamlit as st
import src.jira_config as config
from jira import JIRA
import pandas as pd
import streamlit_shadcn_ui as ui

######################################## Retrieve data from Jira ########################################
def calculate_time(start_date, end_date):
    weekmask = 'Mon Tue Wed Thu Fri'
    holidays = ['2022-01-01', '2022-01-17']
    return len(pd.bdate_range(start_date,
                              end_date,
                              freq='C',
                              weekmask=weekmask,
                              holidays=holidays))

def retrieve_jira_data_by_jql(jql, story_points_df, cost_dev_per_day, percentage_dev_time, percentage_review_time):
    try:
        with st.spinner('Retrieving data from Jira...'):
            # Jira server configuration
            jira = JIRA(options={'server': config.jira['server']}, basic_auth=(config.jira['email'], config.jira['api_token']))

            # Define the columns of the DataFrame including the two extra columns
            columns = ['Issue Key', 'Description', 'Story Points', 'Estimated Dev Days', 'Estimated Cost', 'Actual Dev Days', 'Actual Cost']

            issue_history = {}
            issues = jira.search_issues(jql, maxResults=0)
            all_fields = jira.fields()
            name_map = {jira.field['name']: jira.field['id'] for jira.field in all_fields}
            total_dev_days = 0
            list_of_worklog = pd.DataFrame(columns=columns)
            for issue in issues:

                issue_development_time = 0
                issue_estimated_time = 0
                story_points = 0

                issue_jql = jira.issue(issue.key, expand='changelog')  # pass one issue at the time
                changelog = issue_jql.changelog
                start_dev_date, end_dev_date = "", ""
                start_review_date, end_review_date = "", ""
                development_time = 0
                if getattr(issue.fields, name_map["Story Points"]) is None:
                    story_points = 0
                else:
                    story_points = int(getattr(issue.fields, name_map["Story Points"]))

                estimated_time_from_story_points = int(story_points_df.loc[story_points_df['Story Points'] == str(story_points), 'Development Days'].values[0])
                for history in reversed(changelog.histories):
                    for item in reversed(history.items):
                        if item.field == "status":
                            issue_history = {
                                'created': history.created,
                                'fromString': item.fromString,
                                'toString': item.toString
                            }

                            # calculate development time
                            if item.toString == "In Development":
                                start_dev_date = history.created
                            if item.fromString == "In Development":
                                end_dev_date = history.created
                            if start_dev_date != "" and end_dev_date != "":
                                development_time = development_time + (calculate_time(start_dev_date, end_dev_date) / 100) * percentage_dev_time
                                start_dev_date = ""
                                end_dev_date = ""

                            # calculate review time
                            if item.toString == "In Review":
                                start_review_date = history.created
                            if item.fromString == "In Review":
                                end_review_date = history.created
                            if start_review_date != "" and end_review_date != "":
                                review_time = round((calculate_time(start_review_date, end_review_date) / 100) * percentage_review_time)
                                development_time = development_time + review_time
                                start_review_date = ""
                                end_review_date = ""

                # Calculate the cost for estimated time and actual development time
                estimated_cost = estimated_time_from_story_points * cost_dev_per_day
                actual_cost = development_time * cost_dev_per_day

                # Collect data for the current issue including the cost columns
                issue_data = {
                    'Issue Key': issue.key,
                    'Description': issue.fields.summary,
                    'Story Points': story_points,
                    'Estimated Dev Days': estimated_time_from_story_points,
                    'Estimated Cost': f'{int(estimated_cost):,}',
                    'Actual Dev Days': development_time,
                    'Actual Cost': f'{int(actual_cost):,}',
                }

                # Create a temporary DataFrame and concatenate it with the main DataFrame
                temp_df = pd.DataFrame(columns=columns)
                temp_df = pd.DataFrame(issue_data, index=[0])
                list_of_worklog = pd.concat([list_of_worklog, temp_df], ignore_index=True)

    except Exception as e:
        st.error("Error retrieving data from Jira. Please check your Jira configuration and your JQL.")
        st.stop()
    return list_of_worklog

# dataframe_collection = retrieve_jira_data_by_jql('issuekey in (PS-485)')
# print(dataframe_collection)

def main():

    story_points_df = pd.DataFrame(list({'0': '0', '1': '1', '2': '2', '3': '5', '5': '10', '8': '15', '13': '20'}.items()), columns=['Story Points', 'Development Days'])
    cost_dev_per_day = 980
    percentage_dev_time = 100
    percentage_review_time = 70

    ######################################## Sidebar ########################################
    with st.sidebar:

        # toggle for cost
        cost_toggle = st.toggle('Cost configuration', value=False)
        if cost_toggle:
            cost_dev_per_day = st.number_input("Development cost per dev day", value=980)

        # toggle for story points
        change_story_points_toggle = st.toggle('Customized Story Points', value=False)
        if change_story_points_toggle:
            story_points_df = st.data_editor(
                story_points_df,
                column_config={
                    "story_points": "Story Points",
                    "dev_days": st.column_config.NumberColumn(
                        "Development Days",
                        step=1,
                        format="%d",
                    ),
                },
                hide_index=True,
            )

        # toggle for charts
        show_chart = st.toggle('Show Charts', value=False)

        column_toggle = st.toggle('Column configuration', value=False)
        if column_toggle:
            percentage_dev_time = st.slider("Development time considered %", min_value=1, max_value=100, value=100)
            percentage_review_time = st.slider("Review time considered %", min_value=1, max_value=100, value=70)

    ######################################## Project Cost Page ########################################

    st.title("Project Cost")
    jql = ""
    epic_number = ""
    jql = st.text_input('JQL Query', placeholder='parent in (PS-485, PS-486)')

    if jql or epic_number:
        listOfWorklog = retrieve_jira_data_by_jql(jql, story_points_df, cost_dev_per_day, percentage_dev_time, percentage_review_time)


        ######################################## Metrics Dataframe ########################################

        ui.table(data=listOfWorklog, maxHeight=300)


        ######################################## Total Cards ########################################
        
        total_estimated_dev_day = 0
        total_estimated_cost = 0
        total_actual_dev_days = 0
        total_actual_cost = 0

        for index, row in listOfWorklog.iterrows():
            total_estimated_dev_day = total_estimated_dev_day + int(row['Estimated Dev Days'])
            total_estimated_cost = total_estimated_cost + int(row['Estimated Cost'].replace(',', ''))
            total_actual_dev_days = total_actual_dev_days + int(row['Actual Dev Days'])
            total_actual_cost = total_actual_cost + int(row['Actual Cost'].replace(',', ''))


        cols = st.columns(4)
        with cols[0]:
            ui.metric_card(title="Total Estimated", content=str(total_estimated_dev_day) + " dev days", description="based on story points", key="card1")
        with cols[1]:
            ui.metric_card(title="Estimated Cost", content="$" + f'{int(total_estimated_cost):,}', description="based on $" + str(cost_dev_per_day) + " per dev day", key="card2")
        with cols[2]:
            ui.metric_card(title="Total Actual", content=str(total_actual_dev_days) + " dev days", description="based on story points", key="card3")
        with cols[3]:
            ui.metric_card(title="Total Actual Cost", content="$" + f'{int(total_actual_cost):,}', description="based on $" + str(cost_dev_per_day) + " per dev day", key="card4")        

        ######################################## Charts ########################################
        if show_chart:
            st.bar_chart(listOfWorklog, x="Issue Key", y=["Estimated Dev Days", "Actual Dev Days"], color=["#FF0000", "#0000FF"])

        st.caption("* Dev day definition based on the columns 'In Progress' and 'Review'" + " - now its configured as " + str(percentage_dev_time) + "% for development and " + str(percentage_review_time) + "% for review columns")

#########################################################################################

# source venv/bin/activate
# streamlit run Estimated_vs_Actual_Time.py --server.port 8081
# https://mnzel.medium.com/how-to-activate-python-venv-on-a-mac-a8fa1c3cb511
