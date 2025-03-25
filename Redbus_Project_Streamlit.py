import streamlit as st
import pandas as pd
import mysql.connector
import time
from datetime import timedelta 
mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 password="root",)
mycursor = mydb.cursor(buffered=True)

st.sidebar.title("MAIN MENU")
home = st.sidebar.button("home", type="primary")
route = st.sidebar.button("Select bus route")
if home:
    st.title("Redbus Data Filtering")
    st.write("An interactive application to filter Redbus data.")    
else:
    data = "SELECT Route_Name FROM redbus.bus_details"
    data_route_column = pd.read_sql(data, mydb)
    
# Extract unique route names
    route_name = data_route_column["Route_Name"].unique().tolist()      
    Select_route_name = st.selectbox("Select route", ["All"] + route_name)
    if Select_route_name != "All":
        filtered_route_name = f"Route_name LIKE '%{Select_route_name}%'"
    else:
        filtered_route_name = " 1 + 1"
    Select_Rating = st.selectbox("bus rating", ("All",1,2,3,4,5) )
    # col1, col2, col3= st.columns(3)

    # # Add selectboxes to the columns
    # with col1:
    #     option1 = st.selectbox('Select an option for Column 1', ['Option 1', 'Option 2', 'Option 3'])
    # with col2:
    #     option2 = st.selectbox('Select an option for Column 2', ['Option A', 'Option B', 'Option C'])
    # with col3:
    #     option3 = st.selectbox('Select an option for Column 3', ['Option A', 'Option B', 'Option C'])
    
    
    #Seat_Type = st.selectbox("Select Seat Type", ("All","AC","Non AC") )
    # Filtering bus rate
    rate_min, rate_max = 0, 5
    if Select_Rating == "All":
        rate_min, rate_max = 0 , 5
    elif Select_Rating == 5:
        rate_min, rate_max = 5 , 5
    elif Select_Rating == 4:
        rate_min, rate_max = 4.0, 4.9
    elif Select_Rating == 3:
        rate_min, rate_max = 3.0, 3.9
    elif Select_Rating == 2:
        rate_min, rate_max = 2.0, 2.9
    elif Select_Rating == 1:
        rate_min, rate_max = 0, 1.9
    
    # Filtering bus type
    bus_type = st.selectbox("Select bus type", ["All","A/C", "NON A/C"])
    if bus_type == "A/C":
        bus_type_option = "bustype LIKE '%A/C%' OR bustype LIKE '%AC Seater%' AND bustype NOT LIKE '%non%'"
    elif bus_type == "NON A/C":
        bus_type_option = "bustype LIKE '%NON A/C%' OR bustype LIKE '%NON-AC%' OR bustype LIKE '% NON AC%'"
    elif bus_type == "All":
        bus_type_option = "(bustype LIKE '%NON A/C%' OR bustype LIKE '%NON-AC%' OR bustype LIKE '% NON AC%' OR bustype LIKE '%A/C%' OR bustype LIKE '%AC%')"
    # Filtering bus fare
    bus_fare = st.selectbox("Price range", ["All","Below 500", "500 to 1000", "Above 1000"])
    if bus_fare == "Below 500":
        fare_condition = "price < 500"
    elif bus_fare == "500 to 1000":
        fare_condition = "price BETWEEN 500 AND 1000"
    elif bus_fare == "Above 1000":
        fare_condition = "price > 1000"
    elif bus_fare == "All":
        fare_condition = "price > 0"

       

    # Execute Query busname, Bustype, Departing_time, Reaching_time, Duration,rating ,Price, seats_available
    sqlquery = f"""SELECT * FROM redbus.bus_details WHERE rating BETWEEN {rate_min} AND {rate_max} 
    AND {bus_type_option} 
    AND {fare_condition} 
    AND {filtered_route_name}"""
    mycursor.execute(sqlquery)
    data = mycursor.fetchall()
    columns = [col[0] for col in mycursor.description]  # Extract column names
    df = pd.DataFrame(data, columns=columns)
    st.dataframe(df)

# Close connection at the end
mycursor.close()
mydb.close()