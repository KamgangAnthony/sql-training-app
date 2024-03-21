# pylint: disable=missing-module-docstring
import io
import streamlit as st
import pandas as pd
import duckdb

CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""

beverages = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""

with st.sidebar:
    option = st.selectbox(
        "Qu'est-ce que vous souhaitez reviser?",
        ("Joins", "Views", "Aggregate functions"),
    )

    st.write("Vous avez choisi de reviser: ", option)

data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)

food_items = pd.read_csv(io.StringIO(CSV2))

ANSWER_STR = """
SELECT * from beverages
CROSS JOIN food_items
"""

solution_df = duckdb.sql(ANSWER_STR).df()

st.header("enter your code:")
query = st.text_area(label="votre code SQL ici", key="user_input")

if query:
    try:
        result = duckdb.sql(query).df()
        st.dataframe(result)

        result = result[solution_df.columns]
        if result.equals(result[solution_df.columns]):
            print("")
        else:
            st.dataframe(result.compare(solution_df))

    except Exception as e:
        st.text(str(type(e).__name__ + ": " + str(e)))

    else:
        n_lines_difference = result.shape[0] - solution_df.shape[0]
        if n_lines_difference != 0:
            st.write(
                f"result has a {n_lines_difference} lines difference with the solution"
            )


tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected:")
    st.dataframe(solution_df)

with tab3:
    st.write(ANSWER_STR)
