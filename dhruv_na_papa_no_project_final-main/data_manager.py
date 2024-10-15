import sqlite3 as sql

class DataManager:
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
                company_name VARCHAR(50) NOT NULL
            );
        ''')
        conn.commit()
        conn.close()

    def calculatePaisaUsingTotalItem(self, cursor, date: str, name: str, box: int, dazon: int, total_item: int, option_input: float, company: str):
        total_paisa = total_item * option_input
        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen, total_items, price, total_price, flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (company, date, name, box, dazon, total_item, option_input, total_paisa, 1))

    def calculatePaisausingDozenTotalItem(self, cursor, date: str, name: str, box: int, dazon: int, option_input: float, company: str):
        total_item = dazon * 12
        total_paisa = total_item * option_input
        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen, total_items, price, total_price, flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (company, date, name, box, dazon, total_item, option_input, total_paisa, 1))

    def calculatePaisaUsingDozen(self, cursor, date: str, name: str, box: int, dazon: int, option_input: float, company: str):
        total_paisa = dazon * option_input
        total_item = dazon * 12
        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen, total_items, price, total_price, flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (company, date, name, box, dazon, total_item, option_input, total_paisa, 0))

    def calculateWeightUsingDozenToTotalItem(self, cursor, date: str, name: str, box: int, dazon: int, option_input: float, company: str):
        total_item = dazon * 12
        total_weight = total_item * option_input
        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen, total_items, weight, total_weight, flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (company, date, name, box, dazon, total_item, option_input, total_weight, 1))

    def calculateBothUsingDozenToTotalItem(self, cursor, date: str, name: str, box: int, dazon: int, option_input: float, both: float, company: str):
        total_item = dazon * 12
        total_paisa = total_item * option_input
        total_weight = total_item * both
        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen, total_items, weight, total_weight, price, total_price, flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (company, date, name, box, dazon, total_item, both, total_weight, option_input, total_paisa, 1))

    def calculateBothUsingTotalItem(self, cursor, date: str, name: str, box: int, dazon: int, total_item: int, option_input: float, both: float, company: str):
        total_paisa = total_item * option_input
        total_weight = total_item * both
        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen, total_items, weight, total_weight, price, total_price, flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (company, date, name, box, dazon, total_item, both, total_weight, option_input, total_paisa, 1))

    def calculateBothUsingDozen(self, cursor, date: str, name: str, box: int, dazon: int, option_input: float, both: float, company: str):
        total_paisa = dazon * option_input
        total_item = dazon * 12
        total_weight = total_item * both
        cursor.execute('''
            INSERT INTO data (id, date, name, box, dozen, total_items, weight, total_weight, price, total_price, flag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (company, date, name, box, dazon, total_item, both, total_weight, option_input, total_paisa, 0))

    def add_data(self, date: str, name: str, box: int, total_item: int, option_input: float, option: str, count: str, both: str, company: str):
        conn = sql.connect('data.db')
        cursor = conn.cursor()
        try:
            box = int(box)
            option_input = float(option_input)
            both = float(both) if both else None  # Convert `both` if provided
            total_item = int(total_item) if total_item else 0  # Default to 0 if not provided
        except ValueError as e:
            print(f"Error: {e}")
            return

        dazon = box * 6

        if not both:
            if option == "paisa":
                if count == "on":
                    self.calculatePaisaUsingDozen(cursor, date, name, box, dazon, option_input, company)
                elif not total_item:
                    self.calculatePaisausingDozenTotalItem(cursor, date, name, box, dazon, option_input, company)
                else:
                    self.calculatePaisaUsingTotalItem(cursor, date, name, box, dazon, total_item, option_input, company)
            else:
                self.calculateWeightUsingDozenToTotalItem(cursor, date, name, box, dazon, option_input, company)
        else:
            if count == "on":
                self.calculateBothUsingDozen(cursor, date, name, box, dazon, option_input, both, company)
            elif not total_item:
                self.calculateBothUsingDozenToTotalItem(cursor, date, name, box, dazon, option_input, both, company)
            else:
                self.calculateBothUsingTotalItem(cursor, date, name, box, dazon, total_item, option_input, both, company)

        conn.commit()
        conn.close()

    def get_company_data(self, selection: str, company: str):
        conn = sql.connect('data.db')
        cursor = conn.cursor()

        if selection not in ('paisa', 'weight'):
            raise ValueError("Invalid selection type")

        # Fetch data based on selection and company
        if selection == 'paisa':
            cursor.execute("SELECT no, date, name, box, dozen, total_items, price, total_price, flag FROM data WHERE id = ?", (company,))
        elif selection == 'weight':
            cursor.execute("SELECT no, date, name, box, dozen, total_items, weight, total_weight, flag FROM data WHERE id = ?", (company,))

        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_data(self):
        conn = sql.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT no, company_name FROM company")
        rows = cursor.fetchall()
        conn.close()
        return rows
