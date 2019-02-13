import base64

# Instructions:
# - use your web browser's dev tools to look for a ?pdfemb-serveurl download
# - right click > Copy > Copy Response
# - on the command line, run $ xclip -o > encrypted
# - copy this script to the same folder, and run it using Python
# - you may need to get a new encryption key in the web console: > pdfemb_trans.k

with open("encrypted", "r") as encrypted_file:
    data = base64.b64decode(encrypted_file.read())
key = "ee0110764f6663447dc44caee989a155"

S = range(256)
j = 0
out = []

#KSA Phase
for i in range(256):
    j = (j + S[i] + ord( key[i % len(key)] )) % 256
    S[i] , S[j] = S[j] , S[i]

#PRGA Phase
i = j = 0
for char in data:
    i = ( i + 1 ) % 256
    j = ( j + S[i] ) % 256
    S[i] , S[j] = S[j] , S[i]
    out.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256]))

decrypted_text = ''.join(out)
with open('decrypted.pdf', 'w') as decrypted_file:
    decrypted_file.write(decrypted_text)
