# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(f"Current Pending Orders!")
st.write(
  """
  Display current unfilled orders!
  """
)

# name_on_order = st.text_input("Name of Smoothie:")
# st.write("The name on your Smoothie will be:", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.orders") \
    .filter(col("ORDER_FILLED") == 0) \
    .collect()

if(my_dataframe):
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')
    if(submitted):
        try:
            og_dataset = session.table("smoothies.public.orders")
            edited_dataset = session.create_dataframe(editable_df)
            og_dataset.merge(edited_dataset
                             , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                             , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                            )
            st.success("Someone clicked the button", icon = "👍")
        except:
            st.write("Something went wrong.")
        
else:
    st.write("There are no pending orders right now.", icon = "👍")
