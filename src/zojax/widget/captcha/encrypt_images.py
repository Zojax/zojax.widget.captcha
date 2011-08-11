import md5
import os


def encrypt_md5(s):
    return md5.new(s).hexdigest().upper()

if __name__ == '__main__':
    os.chdir('browser/resources/captchas')
    files = os.listdir('.')
    index = 1
    
    for file in files:
        fname = file[:-5]
        hash = md5.new(fname).hexdigest().upper()
        new_fname = str(index) + '.jpg'
        metaname = new_fname + '.metadata'
        meta = open(metaname, 'w')
        meta.write(hash)
        meta.close()
        os.rename(file, new_fname)
        index += 1
