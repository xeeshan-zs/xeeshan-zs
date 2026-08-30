import urllib.request
import re
import time
import hashlib

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Referer': 'https://github.com/xeeshan-zs/xeeshan-zs'
}

# Let's map all digits 0-9 on dummy names
digit_hashes = {}
# Digit 0
name = f"dummy_{int(time.time()*1000)}"
# Ping it 10 times to map 1..9, 0
for count in range(1, 11):
    url = f"https://count.getloli.com/get/@{name}?theme=gelbooru"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        svg = resp.read().decode('utf-8', errors='ignore')
        b64_list = re.findall(r'base64,([A-Za-z0-9+/=]+)', svg)
        if count < 10:
            digit_hashes[hashlib.md5(b64_list[-1].encode()).hexdigest()] = str(count)
        else:
            digit_hashes[hashlib.md5(b64_list[0].encode()).hexdigest()] = "1"
            digit_hashes[hashlib.md5(b64_list[1].encode()).hexdigest()] = "0"
    time.sleep(0.5)

print("Mapped digits:", digit_hashes)

def get_current_num():
    url = 'https://count.getloli.com/get/@xeeshan-zs?theme=gelbooru'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        svg = resp.read().decode('utf-8', errors='ignore')
        b64_list = re.findall(r'base64,([A-Za-z0-9+/=]+)', svg)
        num_str = "".join([digit_hashes.get(hashlib.md5(b.encode()).hexdigest(), "?") for b in b64_list])
        return num_str

TARGET = 84
while True:
    current = get_current_num()
    print(f"Current count: {current}")
    try:
        val = int(current)
        if val >= TARGET:
            print(f"Reached target {val}!")
            break
    except:
        pass
    time.sleep(0.5)