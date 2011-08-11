import md5
import os


def encrypt_md5(s):
    return md5.new(s).hexdigest().upper()

if __name__ == '__main__':
    os.chdir('browser/resources/captchas')
    files = os.listdir('.')
    index = 1
    
    for file in files:
        if file.endswith('.metadata'):
            value = open(file).readlines()[1].split('=')[1]
            meta = open(file, 'w+').write(value)