import sqlite3


class Database:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def get_all_regions(self):
        self.cursor.execute("SELECT * FROM regions")
        regions = dict_fetchall(self.cursor)
        return regions

    def get_countries_by_region(self, region_id):
        self.cursor.execute("SELECT * FROM countries WHERE region_id = ?", (region_id,))
        countries = dict_fetchall(self.cursor)
        return countries

    def get_all_jobs(self):
        self.cursor.execute("SELECT * FROM jobs")
        jobs = dict_fetchall(self.cursor)
        return jobs

    def get_employees_by_job(self,job_id):
        self.cursor.execute("SELECT * FROM employees WHERE job_id = ?",(job_id,))
        employees = dict_fetchall(self.cursor)
        return employees

    def get_all_locations(self,country_id):
        self.cursor.execute("SELECT * FROM locations WHERE country_id = ?",(country_id,))
        locations = dict_fetchall(self.cursor)
        print(locations)
        return locations

    def get_location_by_id(self, location_id):
        self.cursor.execute("SELECT * FROM locations WHERE location_id = ?", (location_id,))
        row = self.cursor.fetchone()
        if not row:
            return None
        columns = [i[0] for i in self.cursor.description]
        return dict(zip(columns, row))



def dict_fetchall(cursor):
    columns = [i[0] for i in cursor.description]
    print(columns)
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
