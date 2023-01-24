import psycopg2


class Database:
    def __init__(self, config: dict, secrets: dict):
        self.connection = psycopg2.connect(
            host=config["dbHost"],
            dbname=config["dbName"],
            port=config["dbPort"],
            user=config["dbUser"],
            password=secrets["DB_PWD"],
        )

    def get_all_data(self, table: str):
        query = "SELECT * FROM %s;"
        with self.connection.cursor() as cur:
            cur.execute(query, (table,))
            return cur.fetchall()
