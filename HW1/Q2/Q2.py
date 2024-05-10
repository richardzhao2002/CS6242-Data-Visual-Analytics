########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv
#################################################################################

## Change to False to disable Sample
SHOW = False

############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')
        
        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)",("1","test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())

######################################################################

class HW2_sql():
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
    
        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)
    ######################################################################
    ######################################################################

    # GTusername [0 points]
    def GTusername(self):
        gt_username = "rzhao97"
        return gt_username
    
    # Part a.i Create Tables [2 points]
    def part_ai_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        #connection.execute("CREATE TABLE movies(id integer, title text, score real);")
        
        part_ai_1_sql = "CREATE TABLE movies(id integer, title text, score real);"
        ######################################################################
        
        return self.execute_query(connection, part_ai_1_sql)

    def part_ai_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_2_sql = "CREATE TABLE movie_cast(movie_id integer, cast_id integer, cast_name text, birthday text, popularity real);"
        ######################################################################
        
        return self.execute_query(connection, part_ai_2_sql)
    
    # Part a.ii Import Data [2 points]
    def part_aii_1(self,connection,path):
        ############### CREATE IMPORT CODE BELOW ############################
        with open('data/movies.csv') as file_obj:
             reader_obj = csv.reader(file_obj)
             for row in reader_obj:
                 connection.execute("INSERT INTO movies VALUES (?,?, ?)",(row[0],row[1], row[2]))
        #####################################################################
        
        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
    
    def part_aii_2(self,connection, path):
        ############### CREATE IMPORT CODE BELOW ############################
        with open('data/movie_cast.csv') as file_obj:
             reader_obj = csv.reader(file_obj)
             for row in reader_obj:
                 connection.execute("INSERT INTO movie_cast VALUES (?, ?, ?, ?, ?)",(row[0], row[1], row[2], row[3], row[4]))
        ######################################################################
        
        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part a.iii Vertical Database Partitioning [5 points]
    def part_aiii(self,connection):
        ############### EDIT CREATE TABLE SQL STATEMENT ###################################
        part_aiii_sql = "CREATE TABLE cast_bio(cast_id integer primary key, cast_name text, birthday text, popularity real);"
        ######################################################################
        
        self.execute_query(connection, part_aiii_sql)
        
        ############### CREATE IMPORT CODE BELOW ############################
        query = "INSERT INTO cast_bio (cast_id, cast_name, birthday, popularity) SELECT DISTINCT cast_id, cast_name, birthday, popularity FROM movie_cast"
        part_aiii_insert_sql = query
        ######################################################################
        
        self.execute_query(connection, part_aiii_insert_sql)
        
        sql = "SELECT COUNT(cast_id) FROM cast_bio;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
       

    # Part b Create Indexes [1 points]
    def part_b_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_1_sql = "CREATE INDEX IF NOT EXISTS movie_index ON movies (id)"
        ######################################################################
        return self.execute_query(connection, part_b_1_sql)
    
    def part_b_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_2_sql = "CREATE INDEX IF NOT EXISTS cast_index ON movie_cast (cast_id)"
        ######################################################################
        return self.execute_query(connection, part_b_2_sql)
    
    def part_b_3(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_3_sql = "CREATE INDEX IF NOT EXISTS cast_bio_index ON cast_bio (cast_id)"
        ######################################################################
        return self.execute_query(connection, part_b_3_sql)
    
    # Part c Calculate a Proportion [3 points]
    def part_c(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_c_sql = "SELECT printf('%.2f', COUNT(*) * 100.0 / (SELECT COUNT(*) FROM movies)) FROM movies WHERE score BETWEEN 7 AND 20;"
        ######################################################################
        cursor = connection.execute(part_c_sql)
        return cursor.fetchall()[0][0]

    # Part d Find the Most Prolific Actors [4 points]
    def part_d(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_d_sql = "SELECT cast_name, COUNT(movie_id) AS appearance_count FROM movie_cast WHERE popularity > 10 GROUP BY cast_id, cast_name ORDER BY appearance_count DESC, cast_name LIMIT 5"
        ######################################################################
        cursor = connection.execute(part_d_sql)
        return cursor.fetchall()

    # Part e Find the Highest Scoring Movies With the Least Amount of Cast [4 points]
    def part_e(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_e_sql = "SELECT m.title AS movie_title, printf('%.2f', m.score) AS score, COUNT(mc.cast_id) AS cast_count\
            FROM movies m \
            JOIN movie_cast mc ON m.id = mc.movie_id \
            GROUP BY m.title, score \
            ORDER BY score DESC, COUNT(mc.cast_id) ASC, m.title \
            LIMIT 5"
        part_e_sql = "SELECT m.title AS movie_title, printf('%.2f', m.score) AS score, COUNT(mc.cast_id) AS cast_count\
            FROM movies m \
            INNER JOIN movie_cast mc ON m.id = mc.movie_id \
            GROUP BY m.title \
            ORDER BY m.score DESC, COUNT(mc.cast_id) ASC, m.title \
            LIMIT 5"
        ######################################################################
        cursor = connection.execute(part_e_sql)
        return cursor.fetchall()
    
    # Part f Get High Scoring Actors [4 points]
    def part_f(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_f_sql = "SELECT mc.cast_id AS cast_id, mc.cast_name AS cast_name, \
            printf('%.2f', AVG(m.score)) AS average_score\
            FROM movie_cast mc\
            INNER JOIN movies m ON mc.movie_id = m.id\
            WHERE m.score >= 25\
            GROUP BY mc.cast_id\
            HAVING COUNT(DISTINCT m.id) >= 3\
            ORDER BY AVG(m.score) DESC, mc.cast_name\
            LIMIT 10"
        ######################################################################
        cursor = connection.execute(part_f_sql)
        return cursor.fetchall()

    # Part g Creating Views [6 points]
    def part_g(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_sql = """ CREATE VIEW good_collaboration AS
SELECT t1.cast_id as cast_member_id1, t2.cast_id as cast_member_id2, COUNT(t1.movie_id) as movie_count, AVG(t1.score) as average_movie_score
						   FROM (SELECT cast_id, movie_id, score
								FROM movies a 
								JOIN movie_cast b
								ON a.id = b.movie_id)  as t1
							JOIN (SELECT cast_id, movie_id, score
								FROM movies a 
								JOIN movie_cast b
								ON a.id = b.movie_id) as t2
							ON t1.movie_id = t2.movie_id
								AND t1.cast_id < t2.cast_id
							GROUP BY cast_member_id1, cast_member_id2
							HAVING average_movie_score >= 40
							AND movie_count >= 2;
                        """
        ######################################################################
        return self.execute_query(connection, part_g_sql)
    
    def part_gi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_i_sql = """SELECT cast_member_id1, movie_cast.cast_name, printf('%.2f', AVG(average_movie_score)) AS collaboration_score
                            FROM(
                            SELECT cast_member_id1, cast_member_id2, average_movie_score FROM good_collaboration 
                            UNION 
                                SELECT cast_member_id2, cast_member_id1, average_movie_score FROM good_collaboration) temp
                            JOIN movie_cast
                            on movie_cast.cast_id = temp.cast_member_id1
                            GROUP BY cast_member_id1
                            ORDER BY collaboration_score DESC, cast_name ASC
                            LIMIT 5;"""
        ######################################################################
        cursor = connection.execute(part_g_i_sql)
        return cursor.fetchall()
    
    # Part h FTS [4 points]
    def part_h(self,connection,path):
        ############### EDIT SQL STATEMENT ###################################
        part_h_sql = "CREATE VIRTUAL TABLE movie_overview USING fts3(id integer, overview text);"
        ######################################################################
        connection.execute(part_h_sql)
        ############### CREATE IMPORT CODE BELOW ############################
        with open('./data/movie_overview.csv', encoding = "iso-8859-1") as file1:
            reader = csv.reader(file1)
            for values in reader:
                connection.execute("INSERT INTO movie_overview VALUES (?, ?)", (values[0], values[1]))
                connection.commit()
        ######################################################################
        sql = "SELECT COUNT(id) FROM movie_overview;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
        
    def part_hi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hi_sql = "SELECT count(*) FROM movie_overview WHERE overview MATCH 'fight';"
        ######################################################################
        cursor = connection.execute(part_hi_sql)
        return cursor.fetchall()[0][0]
    
    def part_hii(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hii_sql = "SELECT count(*) FROM movie_overview WHERE overview MATCH 'space NEAR/5 program';"
        ######################################################################
        cursor = connection.execute(part_hii_sql)
        return cursor.fetchall()[0][0]


if __name__ == "__main__":
    
    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
    if SHOW == True:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    db = HW2_sql()
    try:
        conn = db.create_connection("Q2")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except Exception as e:
        print("Error in Table Drops")
        print(e)

    try:
        print('\033[32m' + "part ai 1: " + '\033[m' + str(db.part_ai_1(conn)))
        print('\033[32m' + "part ai 2: " + '\033[m' + str(db.part_ai_2(conn)))
    except Exception as e:
         print("Error in Part a.i")
         print(e)

    try:
        print('\033[32m' + "Row count for Movies Table: " + '\033[m' + str(db.part_aii_1(conn,"data/movies.csv")))
        print('\033[32m' + "Row count for Movie Cast Table: " + '\033[m' + str(db.part_aii_2(conn,"data/movie_cast.csv")))
    except Exception as e:
        print("Error in part a.ii")
        print(e)

    try:
        print('\033[32m' + "Row count for Cast Bio Table: " + '\033[m' + str(db.part_aiii(conn)))
    except Exception as e:
        print("Error in part a.iii")
        print(e)

    try:
        print('\033[32m' + "part b 1: " + '\033[m' + db.part_b_1(conn))
        print('\033[32m' + "part b 2: " + '\033[m' + db.part_b_2(conn))
        print('\033[32m' + "part b 3: " + '\033[m' + db.part_b_3(conn))
    except Exception as e:
        print("Error in part b")
        print(e)

    try:
        print('\033[32m' + "part c: " + '\033[m' + str(db.part_c(conn)))
    except Exception as e:
        print("Error in part c")
        print(e)

    try:
        print('\033[32m' + "part d: " + '\033[m')
        for line in db.part_d(conn):
            print(line[0],line[1])
    except Exception as e:
        print("Error in part d")
        print(e)

    try:
        print('\033[32m' + "part e: " + '\033[m')
        for line in db.part_e(conn):
            print(line[0],line[1],line[2])
    except Exception as e:
        print("Error in part e")
        print(e)

    try:
        print('\033[32m' + "part f: " + '\033[m')
        for line in db.part_f(conn):
            print(line[0],line[1],line[2])
    except Exception as e:
        print("Error in part f")
        print(e)
    
    try:
        print('\033[32m' + "part g: " + '\033[m' + str(db.part_g(conn)))
        print("\033[32mRow count for good_collaboration view:\033[m", conn.execute("select count(*) from good_collaboration").fetchall()[0][0])
        print('\033[32m' + "part g.i: " + '\033[m')
        for line in db.part_gi(conn):
            print(line[0],line[1],line[2])
    except Exception as e:
        print("Error in part g")
        print(e)

    try:   
        print('\033[32m' + "part h: " + '\033[m'+ str(db.part_h(conn,"data/movie_overview.csv")))
        print('\033[32m' + "Count h.i: " + '\033[m' + str(db.part_hi(conn)))
        print('\033[32m' + "Count h.ii: " + '\033[m' + str(db.part_hii(conn)))
    except Exception as e:
        print("Error in part h")
        print(e)

    conn.close()
    #################################################################################
    #################################################################################
  
