import json, time, socket, random, datetime, asyncio, select

#What this thing should be able to do
#1. Export thermostat's current status to a given client
#Notes: The thermostat's status should be updated regardless of any client connection. Log its status 
#at a given frequency in the console of this script. Find a way to get around the synchronous behavior 
#of python. 
#2. Receive a command from that client that can change the thermostat's status

async def main():
    main = Main()
    await_sock_conn = asyncio.create_task(main.await_sock_conn())
    populate_reg = asyncio.create_task(main.populate_reg())
    await await_sock_conn
    await populate_reg

class Main():
    def __init__(self):
        self.register = Register(json.dumps({"temp": random.randint(80,89), 
            "timestamp": str(datetime.datetime.now())})) #Instantiate the thermostat Register. 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        addrinfo = socket.getaddrinfo("0.0.0.0", 5000)
        addr = addrinfo[0][-1]
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(addr) #Bind to local addr
        self.sock.listen(5) #Listen on localhost
        print("Listening on",addr)
    async def populate_reg(self):
        while True: 
            print("populate_reg",str(datetime.datetime.now()))
            try:
                self.client[0].send(str.encode(json.dumps(self.register.get_value())))
            except: 
                print("No valid client connection. Reconnecting..")
                client_socket, address = self.sock.accept()    
                print("Connection from", address)
            print(self.register.get_value())
            self.register.set_value({"temp": random.randint(80,89), "timestamp": str(datetime.datetime.now())})
            await asyncio.sleep(10)
    async def await_sock_conn(self):
        print("Awaiting client connection:", str(datetime.datetime.now()))
        client_socket, address = self.sock.accept()    
        print("Connection from", address)
        await asyncio.sleep(0)
        # while True:
        #     self.client = self.sock.accept() #Wait for client connection
        #     await asyncio.sleep(10)

class Register():
    def __init__(self, value):
        self.value = value
        self.history = []
        self.history.append(value)

    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value
        self.history.append(value)

    def register_history(self):
        return self.history
        
asyncio.run(main())


