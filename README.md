# Calibre Dump

Find Calibre Servers. Download books from unauthenticated ones.

**Get Hosts that use calibre:**
````shell script
python3 main.py -s <API_KEY>
python3 main.py --use-shodan <API_KEY>
````

**Download books from a authenticationless calibre host:**
````shell script
python3 main.py -c <IP:PORT>
python3 main.py --calibre-host <IP:PORT>
````