from src.config import get_db_connection
from src.utils import common_ideology


def main(seconds_between: int):
    db = get_db_connection()

    df = common_ideology(db=db, seconds_between=seconds_between)
    print(df.head())
    df.to_csv(f"data/df_ideology_connections_s{seconds_between}.csv")


if __name__ == "__main__":
    main(60)
