# Dragon-E
## What is it?
Dragon-E is a simple but powerful library to encode messages. It relies on the end-user having the decryption key.
## What does it look like?
Encoded messages will look something like this:
`154:221:169:238:253:184:108:204:179:230:206:254:185:220:241:251:179:135:226:169:116:183:139:180:240:245:178:192:254:170:236:195:237:189:148:168:241:166:218:242:86:200:197:139:189:250:243:106:188:232:168:238:189:236:174:150`
In this case, the original message was `Dragon Encryption is a lightweight, easy to use package.` and was encoded using the passkey `AV3ry57r0nGp4Ssw0Rd!?`.
## What makes it so amazing?
1. Unlike some other encryption methods, the encoded message's length is not dependent on the passkey's length. This makes it more difficult to guess the passcode.
2. Every part of the passkey is important, meaning that you can't solve it all at once.
3. The longer the message and passkey, the more difficult it is to decode.
## How can I download it?
`pip install dragon-e`

# EXAMPLE
## Encrypting
```py
import dragon_e as de

important_info = de.encrypt("Don't share this info with anybody!", "V3ry57r0ngS3cuR17yK3Y")
with open('secret_file.dragon', 'w') as f:
    f.write(important_info)
```
## Decrypting
```py
import dragon_e as de
f = open('secret_file.dragon', 'r')
super_secret = f.read()
f.close()
decrypted = de.decrypt(super_secret, "V3ry57r0ngS3cuR17yK3Y")
print("Decoded information: "+decrypted)
```