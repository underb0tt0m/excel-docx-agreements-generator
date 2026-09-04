import json
import psycopg2

class DatabaseClient:
    def __init__(self, config):
        self.config = config
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(
            host=self.config.db['host'],
            port=self.config.db['port'],
            dbname=self.config.db['db_name'],
            user=self.config.db['user'],
            password=self.config.db['password']
        )
        self.connection.autocommit = True
        return self

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.connection and not self.connection.closed:
            self.connection.close()

    def get_input_archive(self, job_id):
        with self.connection.cursor() as cur:
            cur.execute("SELECT archive FROM input_archives WHERE job_id = %s;", (job_id,))
            row = cur.fetchone()
            if row is None:
                raise ValueError(f"Input archive for job {job_id} not found")
            return row[0]

    def save_generation_result(self, job_id, zip_bytes, exceptions, generated_count):
        errors_list = []
        fatal_error = None
        for file_name, file_errors in exceptions.items():
            for err in file_errors:
                err_obj = {"message": str(err)}
                if hasattr(err, 'code'):
                    err_obj["code"] = err.code
                if hasattr(err, 'grpc_code'):
                    err_obj["grpc_code"] = err.grpc_code
                errors_list.append(err_obj)
                if fatal_error is None:
                    fatal_error = str(err)

        with self.connection.cursor() as cur:
            cur.execute("""
                INSERT INTO archives (job_id, archive, gen_count, gen_errors, fatal_gen_error)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (job_id) DO UPDATE
                SET archive = EXCLUDED.archive,
                    gen_count = EXCLUDED.gen_count,
                    gen_errors = EXCLUDED.gen_errors,
                    fatal_gen_error = EXCLUDED.fatal_gen_error,
                    updated_at = NOW();
            """, (job_id, zip_bytes, generated_count, json.dumps(errors_list), fatal_error))
            self.connection.commit()

    def update_job_status(self, job_id, status):
        with self.connection.cursor() as cur:
            cur.execute("UPDATE jobs SET status = %s, updated_at = NOW() WHERE id = %s;", (status, job_id))
            self.connection.commit()

    def save_fatal_error(self, job_id, error_message):
        with self.connection.cursor() as cur:
            cur.execute("""
                INSERT INTO archives (job_id, fatal_gen_error, gen_errors)
                VALUES (%s, %s, %s)
                ON CONFLICT (job_id) DO UPDATE
                SET fatal_gen_error = EXCLUDED.fatal_gen_error,
                    gen_errors = EXCLUDED.gen_errors,
                    updated_at = NOW();
            """, (job_id, error_message, json.dumps([{"message": error_message}])))
            self.connection.commit()