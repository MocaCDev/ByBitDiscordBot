import mysql.connector
import yaml
import sys

class DB:

    def __init__(self):
        self.database = None
        self.table_name = None
        self.column_names = []

        with open('database_connection.yaml', 'r') as db_conn:
            connection_data = yaml.safe_load(db_conn)

            try:
                self.database = mysql.connector.connect(
                    host=connection_data['host'],
                    user=connection_data['user'],
                    passwd=connection_data['pswd']
                )
            except Exception as e:
                print(f'{str(e)}\n\tIf this persist, please do not hesitate to contact Fire🔥Kurama🃏.')
                sys.exit(1)

            db_conn.close()

        self.cursor = self.database.cursor()

        with open('table_layout.yaml', 'r') as t_layout:
            layout = yaml.safe_load(t_layout)
            self.table_name = layout["table_name"]

            column_info = []
            
            for column_name, datatype in layout['columns'].items():
                self.column_names.append(column_name)
                column_info.append(f'{column_name} {datatype}')

            column_info = ','.join(column_info)
            
            try:
                # Create the database, if it does not exist.
                self.cursor.execute(f'CREATE DATABASE IF NOT EXISTS {layout["database_name"]}')

                # Make sure we are actively using the database.
                self.cursor.execute(f'USE {layout["database_name"]}')

                # Create the table in accordance to the data in `table_layout.yaml`
                self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name}({column_info});')

                t_layout.close()
            except Exception as e:
                print(f'{str(e)}\n\tIf this persist, please do not hesitate to contact Fire🔥Kurama🃏.')
                sys.exit(1)
    
    # If more, or less, data is needed (more or less columns exist), this will need to be updated by the owner.
    def add_user(self, user_id: int, account_type: str, public_key: str, private_key: str):
        CN = ','.join(self.column_names)

        # `balance` will be, by default, zero.
        # The user will have to run `!set_default_cash_amount` if they want to explicitly tell the server the starting balance.
        try:
            self.cursor.execute(f'INSERT INTO {self.table_name}({CN}) VALUES ({user_id}, "{account_type}", "{public_key}", "{private_key}", 0)')
            self.database.commit()

            return True # All went well.
        except:
            return False # Oh no, an error happend :c

    def remove_user(self, user_id: int):
        try:
            self.cursor.execute(f'DELETE FROM {self.table_name} WHERE user_id={user_id}')
            self.database.commit()
            
            return True # All went well.
        except:
            return False # Oh no, an error happened :c

    def get_users_balance(self, user_id: int):
        try:
            self.cursor.execute(f'SELECT (balance) FROM {self.table_name} WHERE user_id={user_id}')
            user_balance = self.cursor.fetchall()[0][0]

            return user_balance
        except:
            return None

    def set_users_balance(self, user_id: int, balance: float):
        if balance == -1:
            return False
        
        try:
            self.cursor.execute(f'INSERT INTO {self.table_name}(balance) VALUES ({balance}) WHERE user_id={user_id}')
            self.database.commit()
            
            return True
        except Exception as e:
            return False

    def get_user_account_type(self, user_id: int):
        try:
            self.cursor.execute(f'SELECT (account_type) FROM {self.table_name} WHERE user_id={user_id}')
            users_account_type = self.cursor.fetchall()[0][0]

            return users_account_type
        except:
            return None

    def get_user_public_key(self, user_id: int):
        try:
            self.cursor.execute(f'SELECT (public) FROM {self.table_name} WHERE user_id={user_id}')
            user_public_key = self.cursor.fetchall()[0][0]

            return user_public_key
        except:
            return None

    def get_user_private_key(self, user_id: int):
        try:
            self.cursor.execute(f'SELECT (private) FROM {self.table_name} WHERE user_id={user_id}')
            user_private_key = self.cursor.fetchall()[0][0]

            return user_private_key
        except:
            return None

    def get_all_users(self):
        try:
            self.cursor.execute(f'SELECT * FROM {self.table_name}')
            all_users = self.cursor.fetchall()
            user_data = []

            if len(all_users) == 0:
                return []

            for i in all_users:
                user_data.append({
                    'user_id': i[0],
                    'account_type': i[1],
                    'private_key': i[2],
                    'public_key': i[3],
                    'wallet_balance': i[4]
                })
            
            return user_data
        except:
            return None
    
    def close_db(self): self.database.close()
