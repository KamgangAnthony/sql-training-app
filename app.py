# pylint: disable=missing-module-docstring
import io
import logging
import os
import streamlit as st
import pandas as pd
import duckdb
import init_db

con = duckdb.connect("data/exercises_sql_tables.duckdb", read_only=False)

if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

st.header("enter your code:")
query = st.text_area(label="votre code SQL ici", key="user_input")

with st.sidebar:
    choix = st.selectbox(
        "Qu'est-ce que vous souhaitez reviser?",
        # ["cross_joins"],
        set(init_db.data["theme"]),
        index=None,
        placeholder="Select a theme...",
    )

    st.write("Vous avez choisi de reviser: ", choix)
    print(choix)
    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{choix}'").df().sort_values(
        "last_reviewed").reset_index(drop=True)
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

tables_tab, solutions_tab = st.tabs(["Tables", "Solution"])


# if not user_choice:
#     vari2 = 0
#     while not user_choice:
#         if vari2 == 0:
#             st.write("Pick an exercise bro")
#             vari2 += 1

def get_user_choice_of_exercise_display_exercises(user_choice: str) -> None:
    """
    Get the choice of exercise from the user and display the available exercises
    :param user_choice: a string containing the choice of exercise from the user
    :return: None
    """

    if user_choice:
        exercise_tables = exercise.loc[0, "tables"]
        for table in exercise_tables:
            st.write(f"table: {table}")
            df_table = con.execute(f"SELECT * FROM {table}").df()
            st.dataframe(df_table)
    if not user_choice:
        vari2 = 0
        while not user_choice:
            if vari2 == 0:
                st.write("Pick an exercise bro")
                vari2 += 1


with tables_tab:
    get_user_choice_of_exercise_display_exercises(choix)


def display_solution_of_exercise(user_choice: str) -> None:
    if user_choice:
        st.write(answer)
    if not user_choice:
        vari3 = 0
        while not user_choice:
            if vari3 == 0:
                st.write("Pick an exercise bro")
                vari3 += 1


with solutions_tab:
    display_solution_of_exercise(choix)

# ANSWER_STR = """
# SELECT * from beverages
# CROSS JOIN food_items
# """

# solution_df = duckdb.sql(ANSWER_STR).df()
