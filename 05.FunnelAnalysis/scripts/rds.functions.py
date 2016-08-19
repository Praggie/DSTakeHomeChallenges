import sys
import logging
import rds_config
import pymysql

### rds settings ###
_rds_host  = "dschallenges.c3hzg9suelby.us-west-1.rds.amazonaws.com"
_name = rds_config.db_username
_password = rds_config.db_password
_db_name = rds_config.db_name
_port = 3306

### set up logging ###
logging.basicConfig()
_logger = logging.getLogger()
_logger.setLevel(logging.INFO)

### try connecting to server ###
server_address = (_rds_host, _port)
try:
    _conn = pymysql.connect(_rds_host, user=_name, passwd=_password, db=_db_name, connect_timeout=5)
except:
    _logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()
_logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

### functions ###
def create_table(table_name, table_content, primary_key):
    ######
    # This function create a table in mysql RDS instance
    # table_content - [(colname, coltype, T/F null)]
    ######

    with _conn.cursor() as cur:
        sql_argv = "create table "
        sql_argv += table_name + " "                                                            # table name
        sql_argv += "( "
        sql_argv += ", ".join([e[0] + ' ' + e[1] + ' ' + e[2] for e in table_content])          # columns name+type
        sql_argv += ", PRIMARY KEY (" + primary_key + ")"                                       # primary key
        sql_argv += ")"
        cur.execute(sql_argv)
        _conn.commit()

def bulk_insert(table_name, dat, cols = None):
    ######
    # This function insert data to mysql RDS instance
    ######

    item_count = 0
    with conn.cursor() as cur:
        cur.execute("create table User ( UserID int NOT NULL, Date date NOT NULL, Device varchar(7) NOT NULL, Sex varchar(6) NOT NULL, PRIMARY KEY (UserID))")  
        conn.commit()
        cur.execute("select * from Employee3")
        for row in cur:
            item_count += 1
            logger.info(row)
            #print(row)
    

    return "Added %d items from RDS MySQL table" %(item_count)
