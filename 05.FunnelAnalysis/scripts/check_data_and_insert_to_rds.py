from rds_connections import *
import pandas as pd

#######################################################
#    Insert could be speed up by bulk insert          #
#    Code would be much simpler                       #
#    http://stackoverflow.com/questions/29638136/how-to-speed-up-with-bulk-insert-to-ms-server-from-python-with-pyodbc-from-csv
#    Try bulk insert next time                        #
#######################################################

### files to process ###
data_dir = "/projects/DSTakeHomeChallenges/05.FunnelAnalysis/data/"
user_table = data_dir + "user_table.csv"
home_page_table = data_dir + "home_page_table.csv"
search_page_table = data_dir + "search_page_table.csv"
payment_page_table = data_dir + "payment_page_table.csv"
confirmation_table = data_dir + "payment_confirmation_table.csv"

### keep track of all available user ids ###
# _all_user_ids = set()
_all_user_ids = [int(line.strip().split(',')[0]) for line in open(user_table).readlines()[1:]]

### process user table ###
def process_user_table(data_file_name, conn=CONN):
    print "Processing User Table..."
    users = pd.read_csv(data_file_name)
    item_count = 0
    with conn.cursor() as cur:
        cur.execute("create table User ( UserID int NOT NULL, Date date NOT NULL, Device varchar(7) NOT NULL, Sex varchar(6) NOT NULL, PRIMARY KEY (UserID))")
        for idx, row in users.iterrows():
            # check userID
            if row['user_id'] in _all_user_ids:
                sys.exit("Duplicated UserID: %d " %(row['user_id']))
            else:
                _all_user_ids.add(row['user_id'])
            # insert record to RDS MySQL database
            cur.execute('insert into User values ( %d, "%s", "%s", "%s" )' %(row['user_id'], row['date'], row['device'], row['sex']))
            item_count += 1
            if item_count % 10000 == 0:
                print "Inserted %d items to RDS MySQL table User." %(item_count)
        conn.commit()
    print "Inserted %d items to RDS MySQL table User." %(item_count)

### function process homepage, search page, payment page, confirmation page tables ###
def process_page_table(page_type, data_file_name, col_content, conn = CONN):
    print "Processing %s Table..." %(page_type)
    users = pd.read_csv(data_file_name)
    item_count = 0
    with conn.cursor() as cur:
        cur.execute("show tables")
        if page_type in [tab[0] for tab in cur]:
            print "Table '%s' already exists" %(page_type)
        else:
            cur.execute("create table %s ( UserID int NOT NULL, %s boolean NOT NULL, PRIMARY KEY (UserID) )" %(page_type, page_type))
        for idx, row in users.iterrows():
            # check userID
            if row['user_id'] not in _all_user_ids:
                sys.exit("UserID: %d in %s table does not exist in user table." %(row['user_id'], page_type))
            # check column content
            if row['page'] != col_content:
                sys.exit("UserID: %d has different page name: %s " %(row['user_id'], row['page']))
            # insert record to RDS MySQL database
            cur.execute('insert into %s values ( %d , TRUE)' %(page_type, row['user_id']))
            item_count += 1
            if item_count % 10000 == 0:
                print "Inserted %d items to RDS MySQL table %s." %(item_count, page_type)
        conn.commit()
    print "Inserted %d items to RDS MySQL table %s." %(item_count, page_type)

# process_user_table(data_file_name = user_table)
process_page_table(page_type = "HomePage", data_file_name = home_page_table, col_content = "home_page")
process_page_table(page_type = "SearchPage", data_file_name = search_page_table, col_content = "search_page")
process_page_table(page_type = "PaymentPage", data_file_name = payment_page_table, col_content = "payment_page")
process_page_table(page_type = "ConfirmationPage", data_file_name = confirmation_table, col_content = "payment_confirmation_page")


