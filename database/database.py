from sqlalchemy import create_engine
import pandas as pd


""" 
*Database*
 """
#original Data
sql_engine = create_engine('sqlite:///test.db', echo=False)
connection = sql_engine.raw_connection()
working_df = pd.read_csv("../static/csv/STUD - Sheet1.csv")
working_df.to_sql('data', connection,index=False, if_exists='replace')

#attendance data
working_df = pd.read_csv("../static/csv/attendance.csv")
working_df.to_sql('attendance', connection,index=False, if_exists='replace')

#personal details
working_df = pd.read_csv("../static/csv/personal_details.csv")
working_df.to_sql('personal_details', connection,index=False, if_exists='replace')

#semester details
working_df = pd.read_csv("../static/csv/semester_details.csv")
working_df.to_sql('semester_details', connection,index=False, if_exists='replace')

#domain performance 
working_df = pd.read_csv('../static/csv/Domain_performance.csv')
working_df.to_sql("domain_details", connection,index=False,if_exists='replace')

#CS 
working_df = pd.read_csv('../static/csv/CS.csv')
working_df.to_sql("CS", connection,index=False,if_exists='replace')

#EC
working_df = pd.read_csv('../static/csv/EC.csv')
working_df.to_sql("EC", connection,index=False,if_exists='replace')

#IT
working_df = pd.read_csv('../static/csv/IT.csv')
working_df.to_sql("IT", connection,index=False,if_exists='replace')

#HS
working_df = pd.read_csv('../static/csv/HS.csv')
working_df.to_sql("HS", connection,index=False,if_exists='replace')

#MA
working_df = pd.read_csv('../static/csv/MA.csv')
working_df.to_sql("MA", connection,index=False,if_exists='replace')

