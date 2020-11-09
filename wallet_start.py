import subprocess
import json
command  = './derive -g --mnemonic="also victory dry drink donkey bread little wisdom organ magic monster actor" --cols=path,address,privkey,pubkey --format=json'
p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
p_status = p.wait()
print(output)

#for Json format, add --format=json
keys = json.loads(output)
print(keys)
print(keys[0]['address'])