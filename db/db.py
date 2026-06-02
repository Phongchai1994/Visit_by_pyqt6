import psycopg2
import os
import hashlib
import traceback
import inspect
from dotenv import load_dotenv
from psycopg2 import Binary

load_dotenv(load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')))

def log_db_exceptions(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            self.log_error(
                function_name=f"{os.path.basename(__file__)}::{self.__class__.__name__}::{func.__name__}",
                error_message=f"Error in {func.__name__}::: {e}",
                extra_info=traceback.format_exc()
            )
            print(f"Error in {func.__name__}: {e}")
            return False
    return wrapper

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
        # self.create_tables_if_not_exist()

    @log_db_exceptions
    def create_tables_if_not_exist(self):
        commands = [
            """
            CREATE TABLE IF NOT EXISTS public.relative_fingerprints (
                id serial PRIMARY KEY,
                relative_id bigint NOT NULL,
                finger_name text NOT NULL,
                fingerprint bytea NOT NULL,
                is_active boolean DEFAULT true,
                created_at timestamp DEFAULT CURRENT_TIMESTAMP,
                updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT relative_fingerprints_relative_id_fkey
                    FOREIGN KEY (relative_id)
                    REFERENCES public.relatives(relative_id)
                    ON DELETE RESTRICT,
                CONSTRAINT relative_fingerprints_unique
                    UNIQUE (relative_id, finger_name)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS public.prisoners (
                prisoner_id bigint PRIMARY KEY,
                sex text NOT NULL,
                f_name text NOT NULL,
                l_name text NOT NULL,
                lawsuit text NOT NULL,
                level text NOT NULL,
                dan text NOT NULL,
                type text,
                status text,
                disciplinary text,
                "timestamp" timestamp DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS public.relatives (
                relative_id bigint PRIMARY KEY,
                title text NOT NULL,
                f_name text NOT NULL,
                l_name text NOT NULL,
                address text NOT NULL,
                tel text NOT NULL,
                is_active boolean DEFAULT true,
                "timestamp" timestamp DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS public.check_ (
                id serial PRIMARY KEY,
                key text
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS public.holidays (
                id serial PRIMARY KEY,
                date text NOT NULL UNIQUE,
                name text NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS public.log_error (
                log_id serial PRIMARY KEY,
                time_stamp timestamp DEFAULT CURRENT_TIMESTAMP,
                function_name text,
                error_message text,
                extra_info text
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS public.log_realtime (
                id serial PRIMARY KEY,
                "timestamp" timestamp DEFAULT CURRENT_TIMESTAMP,
                prisoner_id bigint,
                relative_id bigint,
                result text,
                detail text,
                device text,
                channel integer,
                visit_date text,
                time_visit text
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS public.users (
                id serial PRIMARY KEY,
                username text UNIQUE,
                password bytea,
                user_type text,
                fullname text
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS public.relations (
                id serial PRIMARY KEY,
                prisoner_id bigint NOT NULL,
                relative_id bigint NOT NULL,
                relation text NOT NULL,
                is_active boolean DEFAULT true,
                "timestamp" timestamp DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT relations_prisoner_id_fkey FOREIGN KEY (prisoner_id) REFERENCES public.prisoners(prisoner_id) ON DELETE RESTRICT,
                CONSTRAINT relations_relative_id_fkey FOREIGN KEY (relative_id) REFERENCES public.relatives(relative_id) ON DELETE RESTRICT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS public.visit_history (
                id serial PRIMARY KEY,
                "timestamp" timestamp DEFAULT CURRENT_TIMESTAMP,
                visit_date text NOT NULL,
                time_visit text NOT NULL,
                prisoner_id bigint NOT NULL,
                relative_id_1 bigint,
                relative_id_2 bigint,
                relative_id_3 bigint,
                relative_id_4 bigint,
                relative_id_5 bigint,
                channel integer,
                "desc" text,
                CONSTRAINT visit_history_prisoner_id_fkey FOREIGN KEY (prisoner_id) REFERENCES public.prisoners(prisoner_id) ON DELETE RESTRICT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS public.visit_spacial (
                visit_id serial PRIMARY KEY,
                time_stamp timestamp DEFAULT CURRENT_TIMESTAMP,
                date_visit text NOT NULL,
                time_visit text NOT NULL,
                prisoner_id bigint NOT NULL,
                relative_id_1 bigint,
                relative_id_2 bigint,
                relative_id_3 bigint,
                relative_id_4 bigint,
                relative_id_5 bigint,
                channel integer,
                CONSTRAINT visit_spacial_prisoner_id_fkey FOREIGN KEY (prisoner_id) REFERENCES public.prisoners(prisoner_id) ON DELETE RESTRICT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS public.visits (
                visit_id serial PRIMARY KEY,
                time_stamp timestamp DEFAULT CURRENT_TIMESTAMP,
                date_visit text NOT NULL,
                time_visit text NOT NULL,
                prisoner_id bigint NOT NULL,
                relative_id_1 bigint,
                relative_id_2 bigint,
                relative_id_3 bigint,
                relative_id_4 bigint,
                relative_id_5 bigint,
                channel integer,
                visit_status text DEFAULT 'pending',
                CONSTRAINT visits_prisoner_id_fkey FOREIGN KEY (prisoner_id) REFERENCES public.prisoners(prisoner_id) ON DELETE RESTRICT
            )
            """
        ]
                
        alter_commands = [
            'ALTER TABLE IF EXISTS public.relations ADD COLUMN IF NOT EXISTS "user_insert" text',
            'ALTER TABLE IF EXISTS public.relatives ADD COLUMN IF NOT EXISTS "user_insert" text'
        ]
        with self.conn.cursor() as cur:
            for command in commands:
                cur.execute(command)
            for command in alter_commands:
                cur.execute(command)
        print("Tables created or already exist.")

    @log_db_exceptions
    def get_all_prisoners_list(self):
        '''
        ดึงข้อมูลผู้ต้องขังใน DB
        '''
        with self.conn.cursor() as cur:
            cur.execute('SELECT * FROM prisoners')
            rows = cur.fetchall()
            return rows

    @log_db_exceptions
    def get_all_relatives_list(self):
        '''
        ดึงข้อมูลญาติ ใน db'''
        with self.conn.cursor() as cur: 
            cur.execute(
                """
                SELECT
                    r.relative_id,
                    r.title,
                    r.f_name,
                    r.l_name,
                    r.address,
                    r.tel,
                    EXISTS(
                        SELECT 1
                        FROM relative_fingerprints rf
                        WHERE rf.relative_id = r.relative_id
                        AND rf.is_active = TRUE
                    ) AS has_fingerprint,
                    r.is_active,
                    r.timestamp
                FROM relatives r
                """
            )
            rows = cur.fetchall()
            return rows

    @log_db_exceptions
    def insert_and_update_prisoner(self, prisoner_id, sex, f_name, l_name, lawsuit, level, dan, type_, status, disciplinary = None):
        """
        เพิ่มข้อมูลผู้ต้องขัง ถ้ามีอยู่แล้วให้ update
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO prisoners(
                    prisoner_id, sex, f_name, l_name, lawsuit, level, dan, type, status, disciplinary
                )VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s ,%s)
                ON CONFLICT (prisoner_id) DO UPDATE SET
                    sex = EXCLUDED.sex,
                    f_name = EXCLUDED.f_name,
                    l_name = EXCLUDED.l_name,
                    lawsuit = EXCLUDED.lawsuit,
                    level = EXCLUDED.level,
                    dan = EXCLUDED.dan,
                    type = EXCLUDED.type,
                    status = EXCLUDED.status,
                    disciplinary = EXCLUDED.disciplinary,
                    "timestamp" = CURRENT_TIMESTAMP

                """,(prisoner_id, sex, f_name, l_name, lawsuit, level, dan, type_, status, disciplinary)
            )
        return True

    @log_db_exceptions
    def check_db_login(self, username, password):
        '''
        ดึงข้อมูล username password
        '''
        with self.conn.cursor() as cur:
            cur.execute("SELECT password, user_type, fullname FROM users WHERE username=%s", (username,))
            row = cur.fetchone()
            if row:
                db_password = row[0].tobytes()
                input_hash = hashlib.sha256(password.encode()).digest()
                if db_password == input_hash:
                    return True, row[1], row[2]
            return False, None, None

    @log_db_exceptions
    def get_relatives(self, prisoner_id):
        '''
        ดึงข้อมูลญาติ จาก id ผู้ต้องขัง
        '''
        with self.conn.cursor() as cur:
            cur.execute(
                '''
                SELECT rel.relative_id, rel.title, rel.f_name, rel.l_name, rel.tel, r.relation
                FROM relatives rel
                JOIN relations r ON rel.relative_id = r.relative_id
                WHERE r.prisoner_id = %s AND rel.is_active = TRUE AND r.is_active = TRUE
                ''',
                (prisoner_id,)
            )
            return cur.fetchall()

    @log_db_exceptions
    def get_prisoners_from_relative_id(self, relative_id):
        '''
        ดึงข้อมูลผู้ต้องขัง จาก id ญาติ'''
        with self.conn.cursor() as cur:
            cur.execute(
                '''
                SELECT p.prisoner_id, p.f_name, p.l_name, p.level, p.dan, p.status, p.disciplinary, r.relation
                FROM prisoners p
                JOIN relations r ON p.prisoner_id = r.prisoner_id
                WHERE r.relative_id = %s
                ''',(relative_id,)
            )

    @log_db_exceptions
    def insert_or_update_relative_and_relation(self,relative_id, prisoner_id, title, f_name, l_name, address, tel, relation, user_insert = None):
        '''
        เพิ่มข้อมูลญาติไปยัง db และความสัมพันธ์ไปยัง db\n
        ต้องการ relative_id, prisoner_id, title, f_name, l_name, address, tel, relation, user_insert = None
        
        '''
        with self.conn.cursor() as cur:
            cur.execute(
                '''
                INSERT INTO relatives (relative_id, title, f_name, l_name, address, tel, is_active, user_insert)
                VALUES (%s, %s, %s, %s, %s, %s, TRUE, %s)
                ON CONFLICT (relative_id) DO UPDATE SET
                    title = EXCLUDED.title,
                    f_name = EXCLUDED.f_name,
                    l_name = EXCLUDED.l_name,
                    address = EXCLUDED.address,
                    tel = EXCLUDED.tel,
                    is_active = EXCLUDED.is_active,
                    user_insert = EXCLUDED.user_insert,
                    "timestamp" = CURRENT_TIMESTAMP
                RETURNING relative_id
                ''',
                (relative_id, title, f_name, l_name, address, tel, user_insert)
            )
            rel_id = cur.fetchone()[0]

            # เพิ่มข้อมูลไปยัง reltions
            cur.execute(
                '''
                INSERT INTO relations (prisoner_id, relative_id, relation, is_active, user_insert)
                VALUES (%s, %s, %s, TRUE, %s)
                ON CONFLICT (prisoner_id, relative_id) 
                DO UPDATE SET
                    relation = EXCLUDED.relation,
                    is_active = TRUE,
                    "timestamp" = CURRENT_TIMESTAMP,
                    user_insert = EXCLUDED.user_insert
                ''',
                (prisoner_id, rel_id, relation, user_insert)
            )
            print('บันทึกสำเร็จ')
        return True

    @log_db_exceptions
    def get_relative_data(self, relative_id):
        '''
        ดึงข้อมูลญาติ จาก id ของญาติเอง เอาแค่ id,title,f_name,l_name,address,tel
        '''
        with self.conn.cursor() as cur:
            cur.execute(
                '''
                SELECT relative_id, title, f_name, l_name, address, tel
                FROM relatives
                WHERE relative_id = %s
                ''',
                (relative_id,)
            )
            return cur.fetchone()

    @log_db_exceptions
    def updete_relation(self, prisoner_id, relative_id, is_active:bool):
        '''
        แก้ไขข้อมูลความสัมพันธ์ ต้องการ relative_id, prisoner_id, is_active'''
        with self.conn.cursor() as cur:
            print(prisoner_id, relative_id, is_active)
            cur.execute(
                '''
                UPDATE relations
                SET 
                    is_active = %s, 
                    "timestamp" = CURRENT_TIMESTAMP
                WHERE prisoner_id = %s AND relative_id = %s
                ''',(is_active, prisoner_id, relative_id)
            )
            return True

    @log_db_exceptions
    def upsert_relative_fingerprint(self, relative_id, finger_name, fingerprint_bytes, is_active = True):
        with self.conn.cursor() as cur:
            cur.execute(
                '''
                INSERT INTO relative_fingerprints(
                    relative_id, finger_name, fingerprint, is_active, created_at
                ) 
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (relative_id, finger_name) DO UPDATE SET
                    fingerprint = EXCLUDED.fingerprint,
                    is_active = EXCLUDED.is_active,
                    updated_at = CURRENT_TIMESTAMP
                ''',
                (relative_id, finger_name, Binary(fingerprint_bytes), is_active)
            )
            return True

    def log_error(self, function_name, error_message, extra_info=None):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO log_error (function_name, error_message, extra_info)
                    VALUES (%s, %s, %s)
                    """,
                    (function_name, str(error_message), extra_info)
                )
        except Exception as log_e:
            print(f"Error logging to log_error: {log_e}")

# if __name__ == "__main__":
#     db = POSTGRESQL()
#     i,x = db.check_db_login('admin','066986')
#     print(i,x)
#     # for rel in result:
#     #     print('คนที่')
#     #     print(rel)