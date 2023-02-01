import streamlit
import pandas #for reading the s3 bucket file
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Mom's New Healthy Diner")

streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')#set the index of the fruits.txt to fruit name 

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])#pre-populating the 2 fruits to set an example for the customer
fruits_to_show = my_fruit_list.loc[fruits_selected] #we are locating the fruits that have been selected 

# Display the table on the page.
streamlit.dataframe(fruits_to_show)#displaying the selected fruits data 

#this new section is to display the fruitvice response
streamlit.header("Fruityvice Fruit Advice!")
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)#removed watermelon,kiwi
    #streamlit.text(fruityvice_response.json())
    # we take the json and normalize it 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # display it as table
    return fruityvice_normalized
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please enter a fruit to get the information')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()

streamlit.header("The fruit load list contains: ")
#snowflakke related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
        return my_cur.fetchall()

streamlit.header('View Our Fruit List - Add Your Favorites')
#add a button to load the fruit list
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)
    

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
       my_cur.execute("insert into fruit_load_list values('" + new_fruit + "')")
       return "Thanks for adding "+ new_fruit
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add Fruit To List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)



