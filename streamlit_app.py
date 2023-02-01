import streamlit
import pandas #for reading the s3 bucket file
import requests

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
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)#removed watermelon,kiwi
#streamlit.text(fruityvice_response.json())

# we take the json and normalize it 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# display it as table
streamlit.dataframe(fruityvice_normalized)

import snowflake.connecteor

