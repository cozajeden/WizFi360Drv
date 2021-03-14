MAX_CONN        = 4
EOL             = b'\r\n'
STATION_MODE    = b'AT_CWMODE_CUR=1'    + EOL
SOFT_AP_MODE    = b'AT_CWMODE_CUR=2'    + EOL
UPDATE_FIRMWARE = b'AT+CIUPDATE'        + EOL
BOTH_MODE       = b'AT_CWMODE_CUR=3'    + EOL
DHCP_EN         = b'AT+CWDHCP_CUR=1,1'  + EOL
DHCP_DA         = b'AT+CWDHCP_CUR=0,0'  + EOL
MUL_CONN_EN     = b'AT+CIPMUX=1'        + EOL
MUL_CONN_DA     = b'AT+CIPMUX=0'        + EOL
STOP_SER        = b'AT+CIPSERVER=0'     + EOL
STATUS          = b'AT+CIPSTA_CUR?'     + EOL
SEARCH          = b'AT+CWLAP'           + EOL
TEST            = b'AT'                 + EOL
ACK             = b'OK'                 + EOL
PREP_SEND_BUFF  = b'AT+CIPSENDBUF='         # Server mode - <client>,<number of bytes> + EOL
SEND_BUFF       = b'AT+CIPSENDEX='          # Server mode - <client>,<number of bytes> + EOL
SET_DATA_LEN    = b'AT+CIPSENDBUF='         # Client mode - <number of bytes> + EOL
SET_MAX_CONN    = b'AT+CIPSERVERMAXCONN='   # <max con (0~4)> + EOL
CONNECT         = b'AT+CWJAP_CUR='          # "SSID","PASS" + EOL
START_SER       = b'AT+CIPSERVER=1,'        # <port> + EOL
PING            = b'AT+PING='               # <IP or www> + EOL
SSID            = b"HUAWEI-B525-2B90"
PASS            = b'"4MDH8DA9F6T"'