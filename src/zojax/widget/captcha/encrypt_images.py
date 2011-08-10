import md5
import os


def encrypt_md5(s):
    return md5.new(s).hexdigest().upper()

os.chdir('skins/captchas')
files = os.listdir('.')
index = 1

for file in files:
    fname = file[:-5]
    hash = md5.new(fname).hexdigest().upper()
    new_fname = str(index) + '.jpg'
    metaname = new_fname + '.metadata'
    meta = open(metaname, 'w')
    meta.write('[default]\n')
    meta.write('title=' + hash)
    meta.close()
    os.rename(file, new_fname)
    index += 1
