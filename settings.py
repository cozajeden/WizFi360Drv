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
START_SOFT_AP   = b'AT+CWSAP_CUR='          # SoftAP mode - "SSID","PASS",<chl>,<ecn>,<max conn><ssid hidden> + EOL
                                            #   <chl> : channel ID. With range of [0,13]>
                                            #   <ecn> : encryption method:
                                            #       • 0: OPEN
                                            #       • 2: WPA_PSK
                                            #       • 3: WPA2_PSK
                                            #   <max conn> : maximum number of Stations to which WizFi360 SoftAP can be connected; within the range of [1, 4].
                                            #   <ssid hidden>:
                                            #       • 0: SSID is broadcasted. (factory default)
                                            #       • 1: SSID is not broadcasted.