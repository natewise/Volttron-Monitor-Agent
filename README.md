# Volttron Monitor Agent
#### For information about Volttron and their platform, visit their [Read the Docs](https://volttron.readthedocs.io/en/develop/index.html).   

Description: The Volttron platform acts as a high-level interface to hardware. This agent runs a SSL-wrapped server socket that gets Volttron data out to an external client. _client_2.py_ is the mock client that connects to the Monitor Agent, and _sock_cli_js.js_ is it's JavaScript analog. _sock_client.py_, _sock_server_py.py_, and _sock_server_ssl.py_ are seperate from the Volttron implementation. They are the socket logic that the agent and the client use to communicate, placed in its own file.  

https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15
#this has a link to a few other dependcied towards the top of the file

client_2.py is the client script for the thermostat.py API/Register
