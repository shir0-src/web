import requests
import os
import re
import sys
import time
from bs4 import BeautifulSoup

def name_image(i):
    integer = i
    i = str(i)
    name = ""
    if integer < 10:
        name = "0"*3 + i
    elif integer >= 10 and integer < 100:
        name = "0"*2 + i
    elif integer >= 100 and integer <1000:
        name = "0"*1 + i
    elif integer >= 1000:
        name = i
    else:
        print ("[-] Error. over 10000 images or something wrong, please fix name_image() function.")
        exit(0)
    return name


def get_images(url, condition):
    r = requests.get(url)
    soup = BeautifulSoup(r.text.encode(r.encoding), 'html.parser')
    title = re.sub(r'[\\/:*?"<>|]+','',soup.title.string)
    #imgs = soup.find_all("img", src=re.compile(condition))
    imgs = soup.find_all("img", {'src':re.compile(condition)})
    
    # print("r:{0}".format(r))
    # print("soup:{0} ".format(len(soup)))
    # print("imgs:{0}".format(len(imgs)))
    print('{0} images hit.'.format(len(imgs)))

    download = input('start download?[y/n]:')
    if download == "y":
        i = 1
        if not os.path.exists("./images"):
            os.mkdir("./images")
        os.mkdir("./images/{0}".format(title))
        for img in imgs:
            filename = "./images/{0}/{1}.jpg".format(title, name_image(i))
            with open(filename, 'wb') as f: 
                print(img['src'])
                r = requests.get(img['src'])
                f.write(r.content)
            time.sleep(5)
            i = i + 1
        print("Done")
    elif download == "n":
        print('Alright, exiting...')
    else:
        print('Unhandle option. exiting...')
    r.close()
    for img in imgs:
        soup.img.clear()
    exit(0)

def main():
    if len(sys.argv) < 2:
        print("usage:./get_images.py [URL] [condition(Regular Expression)]")
        exit(0)
    url = sys.argv[1]
    condition = sys.argv[2]
    get_images(url, condition)

if __name__ == '__main__':
    main()

