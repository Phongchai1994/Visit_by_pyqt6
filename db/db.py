import psycopg2 ,os ,hashlib
from dotenv import load_dotenv

load_dotenv(load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')))

print('SQLITE_DB',os.getenv("SQLITE_DB"))
print('PG_HOST',os.getenv("PG_HOST"))
print('PG_PORT',os.getenv("PG_PORT"))
print('PG_NAME',os.getenv("PG_NAME"))
print('PG_USER',os.getenv("PG_USER"))
print('PG_PASS',os.getenv("PG_PASS"))

class POSTGRESQL():
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT"),
            dbname=os.getenv("PG_NAME"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASS")
        )
        self.conn.autocommit = True

    def get_user(self):
        '''
        ดึงข้อมูล user password
        '''
        with self.conn.cursor() as cur:
            cur.execute('SELECT * FROM users')
            return cur.fetchall()

# if __name__ == "__main__":
#     db = POSTGRESQL()
#     users = db.get_user()
#     for row in users:
#         user_name = row[1]
#         db_password_blob = row[2]
#         password_str = db_password_blob.tobytes().decode('utf-8')
#         print(f"{user_name}: {password_str}")