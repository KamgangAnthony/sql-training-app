# pylint: disable=missing-module-docstring
import io
import streamlit as st
import pandas as pd
import duckdb

con = duckdb.connect("data/exercises_sql_tables.duckdb", read_only=False)

st.header("enter your code:")
query = st.text_area(label="votre code SQL ici", key="user_input")

with st.sidebar:
    choix = st.selectbox(
        "Qu'est-ce que vous souhaitez reviser?",
        ("cross_joins", "Group by", "Window functions"),
        index=None,
        placeholder="Select a theme...",
    )

    st.write("Vous avez choisi de reviser: ", choix)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{choix}'").df().sort_values("last_reviewed").reset_index(drop=True)
    st.write(exercise)

    if choix:
        exercise_name = exercise.loc[0, "exercise_name"]
        with open(f"answers/{exercise_name}.sql", "r") as f:
            answer = f.read()

        solution_df = con.execute(answer).df()

# data = {"a": [1, 2, 3], "b": [4, 5, 6]}
# df = pd.DataFrame(data)

# if query:
#     try:
#         exercise2 = con.execute(f"{query}").df()
#         st.dataframe(exercise2)
#
#     except Exception as e:
#         st.text(str(type(e).__name__ + ": " + str(e)))

# else:
#     vari = 0
#     while not query:
#         if vari == 0:
#             st.write("Enter a query bro")
#             vari += 1

if query:
    result = None
    try:
        result = con.execute(f"{query}").df()
        st.dataframe(result)

        result = result[solution_df.columns]

        if result.equals(result[solution_df.columns]):
            print("")
        else:
            st.dataframe(result.compare(solution_df))
            st.write("used compare")

    except KeyError as e:
        st.text(str(type(e).__name__ + ": " + str(e)))

    if result is not None:
        n_lines_difference = result.shape[0] - solution_df.shape[0]
        if n_lines_difference != 0:
            st.write(
                f"result has a {n_lines_difference} lines difference with the solution"
            )

tab2, tab3 = st.tabs(["Tables", "Solution"])

# if not choix:
#     vari2 = 0
#     while not choix:
#         if vari2 == 0:
#             st.write("Pick an exercise bro")
#             vari2 += 1


with tab2:
    if choix:
        exercise_tables = exercise.loc[0, "tables"]
        for table in exercise_tables:
            st.write(f"table: {table}")
            df_table = con.execute(f"SELECT * FROM {table}").df()
            st.dataframe(df_table)

    if not choix:
        vari2 = 0
        while not choix:
            if vari2 == 0:
                st.write("Pick an exercise bro")
                vari2 += 1

with tab3:
    if choix:
        st.write(answer)

    if not choix:
        vari3 = 0
        while not choix:
            if vari3 == 0:
                st.write("Pick an exercise bro")
                vari3 += 1

# ANSWER_STR = """
# SELECT * from beverages
# CROSS JOIN food_items
# """

# solution_df = duckdb.sql(ANSWER_STR).df()
