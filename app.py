import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import mysql.connector
import  pandas as pd


load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def connect_to_database():
    return mysql.connector.connect(
        host='localhost',
        user=username,
        password=password,
        database=database_name
    )

def execute_query(connection, query, database, fetch_data=True):
    try:
        # connection = connect_to_database()
        if connection.is_connected():
            cursor = connection.cursor()
            print(query)
            cursor.execute(f"USE {database};")
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows is not None:
                connection.commit()

            return rows

            # else:
            #     cursor.execute(f'''SELECT * FROM {table_name}''')
            #     rows = cursor.fetchall()
            #     return rows
    except mysql.connector.Error as e:
        st.error(f"Error executing SQL Query: {e}")
        connection.rollback()
    # finally:
    #     if connection.is_connected():
    #         cursor.close()
    #         connection.close()



def get_table_data(connection, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        table_data = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        return table_data, column_names
    except mysql.connector.Error as e:
        st.error(f"Error: {e}")
        return [], []


def get_tables_in_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        return table_names
    except mysql.connector.Error as e:
        st.error(f"Error: {e}")
        return []




st.set_page_config(page_title="SQL Query Generator App",layout="wide",page_icon=":robot:")
st.markdown(
        """
            <div style=text-align:center;>
                <h2>SQL Query Generator 🛢️🤖 </h2>
                <p style=color:grey;>This tool can retrieve data from SQL Database using natural language queries</p>
            </div>
        """,
        unsafe_allow_html=True
)
api_key_llm = st.sidebar.text_input("#### Enter your API key", type="password")
if api_key_llm:
    model = genai.GenerativeModel("gemini-pro")
    genai.configure(api_key=api_key_llm)
    database_name = st.sidebar.text_input("Enter the name of the database")
    table_name = st.sidebar.text_input("Enter the name of the table")
    username = st.sidebar.text_input("Enter your username")
    password = st.sidebar.text_input("Enter your password",type="password")
    column_names = []
    try:
        connection = connect_to_database()
        if connection.is_connected():
            tables = get_tables_in_database(connection)
            for table in tables:
                st.subheader(f"Table: {table}")
                table_data, column_names = get_table_data(connection, table)
                df = pd.DataFrame(table_data, columns=column_names)
                st.dataframe(df)
            cursor = connection.cursor()
                # cursor.execute(f'''SELECT * FROM {table_name}''')
                # rows = cursor.fetchall()
                # column_names = [i[0] for i in cursor.description]
                # df = pd.DataFrame(rows, columns=column_names)
                # st.dataframe(df, height=400)
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table:", e)

    st.write('')

    if database_name and username and password:
        text_input = st.text_area("##### Enter your Query (For data from multiple tables, specify both the table names, 'ON' and 'WHERE' conditions)")
        submit = st.button("Retrieve data from SQL")
        if submit:
            with st.spinner("Executing SQL Query..."):
                template = f"""
                        Create a SQL query snippet using the below text for the table with database name and table name as {database_name}.{table_name} and columns {column_names}:
                            ```
                                {text_input}
                            ```
                            I just want a SQL Query.
                        """
                formatted_template = template.format(text_input=text_input)
                response = model.generate_content(formatted_template)
                sql_query = response.text
                sql_query = sql_query.strip().lstrip("```sql").rstrip("```")
                rows = execute_query(connection,sql_query,database_name)

                explanation = f"""
                                        Explain this sql Query:
                                        ```
                                            {sql_query}
                                        ```
                                        Please provide with simplest of explanation of the snippet.
                                    """
                explanation_formatted = explanation.format(sql_query=sql_query)
                explain_output = model.generate_content(explanation_formatted)
                explain_response = explain_output.text

                with st.container():
                    st.success("SQL Query generated successfully ! ")
                    st.code(sql_query, language='sql')
                    st.write(" ")
                    st.write(" ")
                    st.success("Output of this SQL Query")
                    # st.markdown(output_response)
                    if rows:
                        st.dataframe(rows)
                    else:
                        st.info("Data updated successfully !!!")
                        if connection.is_connected():
                            cursor.execute(f'''SELECT * FROM {table_name}''')
                            rows = cursor.fetchall()
                            st.dataframe(rows)

                    st.write(" ")
                    st.write(" ")
                    st.success("Explanation of this SQL Query")
                    st.markdown(explain_response)
else:

    st.error("API key is required to use this application !!!!")