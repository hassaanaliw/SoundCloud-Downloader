import urllib

import re,requests,json,sys

useragent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5"
html = {"User-Agent": useragent, "Content-Type": "application/json", "Accept-Encoding": "gzip"}
client_id='40ae937e42ea2d4d4a04b1e22bb5d371'

def main(url):

    valid = r'^(?:https?://)?(?:www\.)?soundcloud\.com/([\w\d-]+)/([\w\d-]+)'


    matches = re.match(valid, url)
    if matches is None:
        print "Invalid URL"

        sys.exit()


    accountname = matches.group(1)

    song =matches.group(2)

    simple_title = accountname + u'-' + song
    url = 'http://soundcloud.com/%s/%s' % (accountname, song)
    print(url)
    next = 'http://api.soundcloud.com/resolve.json?url=' + url + '&client_id=%s' % client_id
    
    info_json = requests.get(next, headers=html).text

    info = json.loads(info_json)
    video_id = info['id']
    final = "https://api.sndcdn.com/i1/tracks/%s/streams?client_id=%s"%(video_id,client_id)
    print(final)
    next_json = requests.get(final,headers=html).text
    nextdata = json.loads(next_json)
    try:
     dl_link = nextdata["http_mp3_128_url"]
    except KeyError:
        print("Sorry. A stream only(rtmp) link was returned. This song cannot be downloaded. ")
        raw_input("Enter to exit:")
        sys.exit(1)



    ##########DOWNLOAD############
    dl_link = nextdata["http_mp3_128_url"]
    download(dl_link,song,".mp3")

def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize:  # near the end
            sys.stderr.write("\n")
    else:  # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))

def download(url, filename, extension):
     print("Downloading  "+filename+extension)
     urllib.urlretrieve(url,filename+extension,reporthook)





if __name__ == "__main__":
    main(raw_input("Please Enter A Valid Soundcloud Link: "))
