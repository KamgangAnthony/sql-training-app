import duckdb
import pandas as pd
import io



# --------------------------------------------------
# EXERCISES LIST
# --------------------------------------------------


data = {
    "theme": ["cross_joins", "cross_joins"],
    "exercise_name": ["beverages_and_food", "sizes_and_trademarks"],
    "tables": [["beverages", "food_items"], ["size", "trademark"]],
    "last_reviewed": ["1980-01-01", "1970-01-01"],
}

if __name__ == "__main__":
    print("hi")
    con = duckdb.connect("data/exercises_sql_tables.duckdb", read_only=False)

    SQL_QUERY = """
    DROP TABLE IF EXISTS memory_state;
    
    CREATE TABLE memory_state AS
    SELECT * FROM memory_state_df;
    """

    memory_state_df = pd.DataFrame(data)
    con.execute(SQL_QUERY)

    # --------------------------------------------------
    # CROSS JOIN EXERCISES
    # ---------------------------------------------------

    CSV = """
    beverage,price
    orange juice,2.5
    Expresso,2
    Tea,3
    """

    beverages = pd.read_csv(io.StringIO(CSV))
    con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

    CSV2 = """
    food_item,food_price
    cookie juice,2.5
    chocolatine,2
    muffin,3
    """

    food_items = pd.read_csv(io.StringIO(CSV2))
    con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")

    CSV3 = """
    size
    XS
    M
    L
    XL
    """

    size = pd.read_csv(io.StringIO(CSV3))
    con.execute("CREATE TABLE IF NOT EXISTS size AS SELECT * FROM size")

    CSV4 = """
    trademark
    Nike
    Asphalte
    Abercrombie
    Lewis
    """

    trademark = pd.read_csv(io.StringIO(CSV4))
    con.execute("CREATE TABLE IF NOT EXISTS trademark AS SELECT * FROM trademark")

    con.close()
