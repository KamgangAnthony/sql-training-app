# pylint: disable=missing-module-docstring
import io
import streamlit as st
import pandas as pd
import duckdb

con = duckdb.connect("data/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    choix = st.selectbox(
        "Qu'est-ce que vous souhaitez reviser?",
        ("cross_joins", "Group by", "Window functions"),
        index=None,
        placeholder="Select a theme..."
    )

    st.write("Vous avez choisi de reviser: ", choix)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{choix}'").df()
    st.write(exercise)

data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)

# ANSWER_STR = """
# SELECT * from beverages
# CROSS JOIN food_items
# """

# solution_df = duckdb.sql(ANSWER_STR).df()

st.header("enter your code:")
query = st.text_area(label="votre code SQL ici", key="user_input")

# if query:
#     try:
#         result = duckdb.sql(query).df()
#         st.dataframe(result)
#
#         result = result[solution_df.columns]
#         if result.equals(result[solution_df.columns]):
#             print("")
#         else:
#             st.dataframe(result.compare(solution_df))
#
#     except Exception as e:
#         st.text(str(type(e).__name__ + ": " + str(e)))
#
#     else:
#         n_lines_difference = result.shape[0] - solution_df.shape[0]
#         if n_lines_difference != 0:
#             st.write(
#                 f"result has a {n_lines_difference} lines difference with the solution"
#             )
#
# tab2, tab3 = st.tabs(["Tables", "Solution"])
#
# with tab2:
#     st.write("table: beverages")
#     st.dataframe(beverages)
#     st.write("table: food_items")
#     st.dataframe(food_items)
#     st.write("expected:")
#     st.dataframe(solution_df)
#
# with tab3:
#     st.write(ANSWER_STR)
