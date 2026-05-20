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

    def get_all_tables(self, schema='public'):
        '''
        ดึงรายชื่อตารางทั้งหมดใน schema ที่ระบุ (ค่าเริ่มต้น: public)
        '''
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = %s AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """, (schema,))
            return [row[0] for row in cur.fetchall()]

    def get_table_schema(self, table_name, schema='public'):
        '''
        ดึงโครงสร้างตาราง (column name, type, nullable, default)
        '''
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = %s AND table_schema = %s
                ORDER BY ordinal_position
            """, (table_name, schema))
            return cur.fetchall()

    def get_all_tables_schema(self, schema='public'):
        '''
        ดึงโครงสร้างของทุกตารางใน schema ที่ระบุ
        '''
        tables = self.get_all_tables(schema)
        all_schema = {}
        for table in tables:
            all_schema[table] = self.get_table_schema(table, schema)
        return all_schema

if __name__ == "__main__":
    db = POSTGRESQL()
    all_schema = db.get_all_tables_schema()
    for table, schema in all_schema.items():
        print(f"Table: {table}")
        for col in schema:
            print(col)



#     db = POSTGRESQL()
#     users = db.get_user()
#     for row in users:
#         user_name = row[1]
#         db_password_blob = row[2]
#         password_str = db_password_blob.tobytes().decode('utf-8')
#         print(f"{user_name}: {password_str}")