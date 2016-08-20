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
    CONN = pymysql.connect(_rds_host, user=_name, passwd=_password, db=_db_name, connect_timeout=5)
except:
    _logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()
_logger.info("SUCCESS: Connection to RDS mysql instance succeeded")


