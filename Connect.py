import socket
import threading
import time
import json
from millonere import HE

# --- functions ---
class ssocket :
    HE = None
    money = 0 

    def __init__(self , money): 
        self.HE = HE()
        self.money = money



    def handle_client(self ,conn, addr): 
        print("[thread] starting")

        # recv message
        message = conn.recv(1024)
        message = message.decode()

        if message == 'Ready' : # if message from bob is ready then start to calculate the array [ alice array check slide 21 - L12 ]
            if len(self.HE.send_array) == 0 :
                self.HE.Sender(self.money)
            
            dict = {"Key" : "Here RSA key." , "array" : self.HE.send_array}
            data = json.dumps(dict) 
            data = data.encode()
            conn.send(data) # send array 
        
        message = conn.recv(4096) # wait for the response array from bob 
        message = message.decode()
        # while len(message) == 0 :
        #     message = conn.recv(4096)
        #     message = message.decode()
        
        data = json.loads(message) 
        array = data['array']

        result = self.HE.results(array) # calculate bob array and check if alice is greater than bob or not  
        result = str(result)

        conn.send(result.encode()) # We don't need this , but it's to tell bob if he is the winner or not 

        conn.close()

            

    
    # --- main ---
    def Server(self , port) : # Handling connections 
        host = '127.0.0.1'
        port = int(port)

        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
        s.bind((host, port))
        s.listen(1)

        all_threads = []

        try:
            while True:
                print("Waiting for client")
                conn, addr = s.accept()
            
                print("Client:", addr)
                
                t = threading.Thread(target=self.handle_client, args=(conn, addr))
                t.start()
            
                all_threads.append(t)
        except KeyboardInterrupt:
            print("Stopped by Ctrl+C")
        finally:
            if s:
                s.close()
            for t in all_threads:
                t.join()



    def send(self  , port): # Bob in slide L12 - 21 
        host = '127.0.0.1'
        port = int(port)

        s = socket.socket()
        s.connect((host, port))

        print("Connected to the server")


        # Tell him Ur ready to recive the array [ array from alice , check slide 21 L12 ]
        message = 'Ready'.encode()
        s.send(message)

        #wait for Json [ array ]
        message = s.recv(4096)
        message = message.decode()
        data = json.loads(message)
        key = data['Key']
        rec_array = data['array']


        # calculate the recived array then return {E(r) ...... } check slide 21 
        arr = self.HE.reciver(self.money , rec_array , self.HE.get_public())

        data = json.dumps({"array" : arr})
        data = data.encode()
        s.send(data) # send arr to alice 
        
        # wait for the result 
        message = s.recv(1024) 
        message = message.decode()

        if message == '1':
            print('You Lost')
        elif message == '0':
            print('You Won')
        else :
            print('IDK')
        
        s.close
        return 





    def check(ip , port): # check if the alive or not. 
        try : 
            s = socket.socket()
            s.connect((ip, int(port)))
            s.close() ##
            return True
        
        except ConnectionRefusedError:
            # print("Connection Refused Error")
            return False
        except : 
            # print("Another ERROR !")
            return False




# Connect 

S = ssocket(100000)
ser = threading.Thread(target=S.Server , args = (5000 , ))
ser.start()


B = ssocket(10293)

time.sleep(3) 

AA = B.send(5000)
