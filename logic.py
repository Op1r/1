import sqlite3
from config import DATABASE

skills = [ (_,) for _ in (['Python', 'SQL', 'API'])]
statuses = [ (_,) for _ in (['На этапе проектирования', 'В процессе разработки', 'Разработан. Готов к использованию.', 'Обновлен', 'Завершен. Не поддерживается'])]


class DB_Manager:
    def __init__(self, database):
        self.database = database # имя базы данных
        
    def create_tables(self):
        con = sqlite3.connect(self.database)
        with con:
            con.execute("""CREATE TABLE projects (
                            project_id INTEGER PRIMARY KEY,
                            user_id INTEGER,
                            project_name TEXT NOT NULL,
                            description TEXT,
                            url TEXT,
                            status_id INTEGER,
                            FOREIGN KEY(status_id) REFERENCES status(status_id))""")
            con.execute("""CREATE TABLE status(
                        status_id INTEGER PRIMARY KEY,
                        status_name TEXT)""")
            con.execute("""CREATE TABLE skill(
                        skill_id INTEGER PRIMARY KEY,
                        skill_name TEXT)""")
            con.execute("""CREATE TABLE project_skills(
                        skill_id INTEGER,
                        project_id INTEGER,
                        FOREIGN KEY (skill_id) REFERENCES skill(skill_id),
                        FOREIGN KEY (project_id) REFERENCES projects(project_id))""")
            con.commit()

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
    
    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
        
    def insert_project(self, data): # data = [(user_id, project_name, description, url, status=us_id)]
        sql ='INSERT INTO projects VALUES(?, ?, ?, ?, ?)'
        self.__executemany(sql, data)
        

    def insert_skill(self, user_id, project_name, skill):
        id = self.get_project_info(user_id, project_name)[0][0]
        skill_id = self.__select_data('SELECT id FROM skills WHERE skill_name = ?', (skill,))
        data = [(id, skill_id)]
        sql = 'INSERT INTO project_skill VALUES(?, ?)'
        self.__executemany(sql, data)



    def get_statuses(self):
        # Задание 2. Получи все статус_имена из таблицы
        pass

    def get_status_id(self, status_name):
        sql = 'SELECT status_id FROM status WHERE status_name = ?'
        res = self.__select_data(sql, (status_name,))
        if res: return res[0][0]
        else: return None

    def get_projects(self, user_id):
        return self.__select_data(sql='SELECT * FROM projects WHERE user_id = ?', data = (user_id,))
    
    def get_skill(self):
        return self.__select_data(sql='SELECT * FROM skill')
    
    def get_project_info(self, user_id, project_name):
        sql = """
        SELECT project_name, description, url, status_name FROM  (
        SELECT * FROM projects 
        JOIN status ON
        status.status_id = projects.status_id)
        WHERE project_name=? AND user_id=?
        """
        return self.__select_data(sql=sql, data = (project_name, user_id))[0]

    def default_insert(self):
        sql = 'INSERT INTO skill (skill_name) values(?)'
        data = skills
        self.__executemany(sql, data)
        sql = 'INSERT INTO status (status_name) values(?)'
        data = statuses
        self.__executemany(sql, data) 


    def update_projects(self, param, data):
        self.__executemany(f"UPDATE projects SET {param} = ? WHERE project_name = ? AND user_id = ?", [data]) 


    def delete_project(self, user_id, project_id):
        #Задание 3. Реализуй удаление проекта по заданным параметрам.
        pass


if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    
    data = [
        (1111, 'Бот - администратор  Тг - бот, который будет отвечать за чат','', 1)
    ]
    #manager.insert_project(data)
 