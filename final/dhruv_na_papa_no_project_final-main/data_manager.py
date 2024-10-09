import sqlite3 as sql

class data_manager:

    def __init__(self) -> None:
        conn = sql.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data (
                id VARCHAR(100) NOT NULL,
                "no" INTEGER PRIMARY KEY,  
                date DATE NOT NULL,
                name VARCHAR(255) NOT NULL,
                box INTEGER NOT NULL,
                dozen INTEGER,
                total_items INTEGER,
                weight DECIMAL(10, 2),
                total_weight DECIMAL(10, 2),
                price DECIMAL(5, 2),
                total_price DECIMAL(10, 5),
                flag INTEGER
            );
        ''')

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS company (
                    "no" INTEGER PRIMARY KEY,
                    company_name VARCAR(50) NOT NULL
                );
        ''')
        conn.commit()
        conn.close()


    def calculatePaisaUsingTotalItem(cursor,date : int ,name : str , box : int,dazon : int , total_item : int , option_input : int, company : str):
        total_paisa = int(total_item) * int(option_input)
        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen, total_items, price, total_price,flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
            ''', (company,date, name, box, dazon , total_item, option_input, total_paisa,1))
        
    def calculatePaisausingDozenTotalItem(cursor,date : int ,name : str , box : int,dazon : int , option_input : int, company : str):
        total_item = (dazon * 12)
        total_paisa = (total_item * float(option_input))
        
        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen,total_items, price, total_price,flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
            ''', (company,date, name, box, dazon ,total_item, option_input, total_paisa,1))
        
    def calculatePaisaUsingDozen(cursor,date : int ,name : str , box : int,dazon : int , option_input : int, company : str):
        total_paisa = int(dazon) * float(option_input)
        total_item =  int(dazon) * 12
        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen,total_items, price, total_price,flag)
            VALUES (?, ?, ?, ?, ?, ?,? , ?,?)
            ''', (company,date, name, box, dazon,total_item , option_input, total_paisa,0))
        
    def calculateWieghtUsingDozenToTotalItem(cursor,date : int ,name : str , box : int,dazon : int , option_input : int, company : str):
        total_item = (int(dazon) * 12)
        total_weight = (total_item * float(option_input))

        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen, total_items, weight, total_weight,flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
            ''', (company ,date, name, box, dazon , total_item, option_input, total_weight,1))
        
    def calculateBothUsingDozenTOTotalItem(cursor,date : int ,name : str , box : int,dazon : int  , option_input : int , both : int, company : str):
        total_item = (dazon * 12)
        total_paisa = (total_item * float(option_input))
        total_wieght = (total_item * float(both))
        cursor.execute('''
        INSERT INTO data (id, date, name, box, dozen,total_items,weight,total_weight, price, total_price,flag)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?,?,?,?)
        ''', (company,date, name, box, dazon ,total_item,both,total_wieght, option_input, total_paisa,1))

    def calculateBothUsingTotalitem(cursor,date : int ,name : str , box : int,dazon : int ,total_item : int, option_input : int,both : int, company : str):
        total_paisa = int(total_item) * float(option_input)
        total_weight = (int(total_item) * float(both))
        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen, total_items,weight,total_weight, price, total_price,flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
            ''', (company,date, name, box, dazon , total_item,both,total_weight, option_input, total_paisa,1))
    
    def calculateBothUsingdozen(cursor,date : int ,name : str , box : int,dazon : int , option_input : int,both : int, company : str):
        total_paisa = int(dazon) * float(option_input)
        total_item = int(dazon) * 12
        total_weight = (int(total_item) * float(both))
        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen,total_items,weight,total_weight, price, total_price,flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?,?, ?,?)
            ''', (company,date, name, box, dazon,total_item ,both,total_weight, option_input, total_paisa,0))
        

        
    def add_data(self,date : int ,name : str , box : int , total_item : int , option_input : int, option : str, count : str,both : str, company : str):
        conn = sql.connect('data.db')
        cursor = conn.cursor()
        try:
            box = int(box)
            option_input = float(option_input)
        except ValueError:
            total_item = None 
        
        dazon = box * 6

        if both == "":
            if option == "paisa":
                if count == "on":
                    self.calculatePaisaUsingDozen(cursor,date, name, box, dazon , option_input,company)
                if count == "":
                    if total_item == "":
                        self.calculatePaisausingDozenTotalItem(cursor,date, name, box, dazon , option_input,company)
                    else:
                        self.calculatePaisaUsingTotalItem(cursor,date, name, box, dazon ,total_item, option_input,company)
            else:
                self.calculateWieghtUsingDozenToTotalItem(cursor,date, name, box, dazon , option_input,company)
        else:
            if count == "on":
                    self.calculateBothUsingdozen(cursor,date, name, box, dazon , option_input,both,company)
            else:
                if total_item == "":
                    self.calculateBothUsingDozenTOTotalItem(cursor,date, name, box, dazon , option_input,both,company)
                else:
                    self.calculateBothUsingTotalitem(cursor,date, name, box, dazon,total_item , option_input,both,company)
                    
        
        conn.commit()
        conn.close()

    def get_data():
        conn = sql.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM company;")
        data = cursor.fetchall()
        conn.close()
        return data
    
    def get_company_data(selection,company):
        conn = sql.connect('data.db')
        curson = conn.cursor()
        if selection == "weight":
            query = "SELECT date, name, box, dozen, total_items, weight, total_weight,flag FROM data WHERE id = ?"
        else:
            query = "SELECT date, name, box, dozen, total_items, price, total_price,flag FROM data WHERE id = ?"

        data = conn.execute(query, (company,)).fetchall()
        conn.close()
        print(data)
        return data

    
