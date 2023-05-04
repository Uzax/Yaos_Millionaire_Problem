import random 
#from RSA_enc import RSA_ENC

#------- alice

class HE:
    rsa = None
    send_array = []

    # def __init__(self) :
    #     #self.rsa = RSA_ENC()


    def get_public (self):
        return 1 
        #return self.rsa.PublicKey


    
    def Sender(self, X):
        binX = bin(X)[2:]

        R0 = []
        R1 = []
        arr = [] 
        for i in binX:
            if i == '1' :
                R1.append(1)
                R0.append(random.randint(2,100))
                # R1.append(self.rsa.encrypt(1))
                # R0.append(self.rsa.encrypt(random.randint(2,100)))
            else:
                # R0.append(self.rsa.encrypt(1))
                # R1.append(self.rsa.encrypt(random.randint(2,100)))
                 R0.append(1)
                 R1.append(random.randint(2,100))
            
        R0.reverse()
        R1.reverse()

        
            
        arr.append(R0)
        arr.append(R1)

        print(arr)
        self.send_array = arr 
        #return arr 

    #print(arr)


    #------bob --------

    def reciver(self,Y ,sender_arr , publicsender = None):

        binY = bin(Y)[2:]

        while (len(binY) < len(sender_arr[0])):
            binY = '0' + binY


        S0 = []

        for i in range(1, len(binY)+1):
            if binY[0:i][-1] == '0' :
                S0.append(binY[0:i-1] + '1')

        arr2 = []

        for i in S0 :
            C = len(sender_arr[0]) -1
            tmp = []
            for j in i :
                tmp.append(sender_arr[int(j)][C])
                C-=1
            arr2.append(tmp)

        if len(arr2) < len(sender_arr[0]):
            #tmp = self.rsa.encrypt(random.randint(2,100), publicsender)
            tmp = random.randint(2,100)
            arr2.append([tmp]) #E
        

        return arr2



    #------- back to alice 


    def results (self ,array):
       
     
        for i in array :
            result = 1
            for j in i :
                #N = self.rsa.decrypt(j)
                result*= int(j) 

                if result > 1 :
                    break
            
            if result == 1 :
                return 1
        
        return 0



alice = HE() #
bob = HE() #

alice.Sender(7)
res = bob.reciver(5 , alice.send_array)
print(res)
print(alice.results(res))