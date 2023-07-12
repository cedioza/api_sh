import mysql.connector
import os


class MysqlConnection(object): 
    """ Class connection mysql """
    
    def __init__(self, host, user, password, database):
        self.connector = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connector.cursor()
        
    def select(self, query, params):
        self.cursor.execute(query, params)
    
    def insert(self, query, params):
        if type(params) == list:
            if len(params) > 1:
                self.cursor.executemany(query, params)
            else:
                self.cursor.execute(query, params[0])
            self.connector.commit()
        
    def query(self, function:str, query:str, params:tuple):
        try:
            _execute = getattr(self, function)
            _execute(query, params)
        except mysql.connector.Error as err:
            print("Something mysql wrong: {}".format(err))
            self.connector.rollback()
        
    def close_connection(self):
        self.cursor.close()
        self.connector.close()