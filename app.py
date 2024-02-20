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
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def execute_query(query):
    try:
        connection = connect_to_database()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    except mysql.connector.Error as e:
        st.error(f"Error executing SQL Query: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


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
table_name = st.text_input("Enter the name of the table")
column_names=[]
try:
    connection = connect_to_database()
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute(f'''SELECT * FROM {table_name}''')
        rows = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        df = pd.DataFrame(rows,columns=column_names)
        st.dataframe(df, height=400)
except mysql.connector.Error as e:
    print("Error reading data from MySQL table:", e)
finally:
    cursor.close()
    connection.close()
    print("MySQL connection is closed")



def main():

    st.write('')

    if table_name is not None and column_names is not None:
        text_input = st.text_area("##### Enter your Query")
        submit = st.button("Retrieve data from SQL")
        if submit:
            with st.spinner("Executing SQL Query..."):
                template = f"""
                    Create a SQL query snippet using the below text for the table with table name {table_name} and columns {column_names}:
                    ```
                        {text_input}
                    ```
                    I just want a SQL Query.
                """
                formatted_template = template.format(text_input=text_input)
                response = model.generate_content(formatted_template)
                sql_query = response.text
                sql_query = sql_query.strip().lstrip("```sql").rstrip("```")
                rows = execute_query(sql_query)

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
                    st.code(sql_query,language='sql')
                    st.write(" ")
                    st.write(" ")
                    st.success("Output of this SQL Query")
                    # st.markdown(output_response)
                    if rows:
                        st.dataframe(rows)
                    else:
                        st.info("No data retrieved from the database")
                    st.write(" ")
                    st.write(" ")
                    st.success("Explanation of this SQL Query")
                    st.markdown(explain_response)
main()