# Ransomware
A ransomware malware developed for educational purposes. The main ransomware file is executed at the victim's end as a result of which a TCP reverse shell is created between the attacker and the victim.
Apart from this, all the documents in the client's system (.txt for this project) get encrypted and the encryption key gets sent to the attacker via the TCP connection.The key is deleted from the victim's system.
The victim can only restore his/her files when he/she has the decryption key which the attacker would give when a certain ransom is paid.
**This ransomware has a unique signature and can't be detected by Windows OS. Use it at your own risk.**