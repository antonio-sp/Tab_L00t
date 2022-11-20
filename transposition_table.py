import sqlite3


class TranspositionTable():
    def __init__(self,db_file):
        self.db_file = db_file
        create_table_cmd   =   """ CREATE TABLE IF NOT EXISTS TT (
                                        state string not null PRIMARY KEY,
                                        score integer not null,
                                        depth integer not null
                                    ); """
        conn = None
        try:
            # autocommit mode by setting isolation_level to None.
            conn = sqlite3.connect(db_file, isolation_level=None)
            # Set journal mode to WAL.
            conn.execute('pragma journal_mode=wal')
            conn.execute(create_table_cmd)
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def get_conn(self):
        try:
            # autocommit mode by setting isolation_level to None.
            conn = sqlite3.connect(self.db_file, isolation_level=None)
            # Set journal mode to WAL.
            conn.execute('pragma journal_mode=wal')
            return conn
        except sqlite3.Error as e:
            print(e)

    def add(self, depth, state, score):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cmd = '''INSERT OR REPLACE INTO TT(state,score,depth)
                  VALUES(?,?,?)'''
            cur.execute(cmd, (state,score,depth) )
            cur.close()
        except sqlite3.Error as error:
            print("Cannot insert",error)
        finally:
            conn.close()


    def lookup(self, state):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            cur.execute("SELECT * FROM TT WHERE state=? LIMIT 1", 
                    (state,))
            row = cur.fetchone()
            cur.close()
            
            if row is not None :
                #old_state, old_score, old_depth = row
                return row
            else:
                return None

        except sqlite3.Error as error:
            print("Cannot lookup",error)
        finally:
            conn.close()





        
         
        
