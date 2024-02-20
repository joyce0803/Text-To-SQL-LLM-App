## Text-To-SQL App
The Text-To-SQL is an application that allows users to retrieve data from SQL databases using natural language queries. It is powered by LLMS model, which understands and generates SQL queries based on user input.
These queries are further used to display the required data.

### Features
- Language Queries: Users can input their queries in plain English, and the application will generate the corresponding SQL query.

- SQL Query Execution: The application executes the generated SQL query against the specified SQL database and retrieves the results.

- Interactive Interface: Users interact with the application through a user-friendly web interface built using Streamlit.

### Getting Started

Prerequisites
Python 3.9 and above
Streamlit
LLM
MySQL or other SQL database server

### Installation

Clone the repository:

bash
Copy code
git clone https://github.com/your-username/sql-query-generator-app.git
Install the required Python dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the gemini-pro model and obtain the necessary API key from Google.

Configure the application to use the gemini-pro model and specify the database connection details in the .env file.

Usage
Run the application:

bash
Copy code
streamlit run app.py
Access the application through your web browser at the specified URL.

Enter your natural language query in the provided text area and click the "Retrieve data from SQL" button.

The application will generate the corresponding SQL query, execute it against the database, and display the results.
