Multi threaded downloader in Python 2.7 using concurrent.futures

__Single thread__
```
rkadam@rkadam-vbox:~/github/pydwnldr/src$ time wget http://ubuntu.mirrors.tds.net/pub/releases/15.10/ubuntu-15.10-desktop-amd64.iso
--2016-01-28 15:47:20--  http://ubuntu.mirrors.tds.net/pub/releases/15.10/ubuntu-15.10-desktop-amd64.iso
Resolving ubuntu.mirrors.tds.net (ubuntu.mirrors.tds.net)... 64.50.236.222
Connecting to ubuntu.mirrors.tds.net (ubuntu.mirrors.tds.net)|64.50.236.222|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1178386432 (1.1G) [application/octet-stream]
Saving to: ‘ubuntu-15.10-desktop-amd64.iso’

ubuntu-15.10-desktop-amd64.iso            100%[======================================================================================>]   1.10G   844KB/s   in 22m 49ss

2016-01-28 16:10:09 (840 KB/s) - ‘ubuntu-15.10-desktop-amd64.iso’ saved [1178386432/1178386432]


real    22m49.513s
user    0m0.180s
sys     0m29.884s
```
__4 Threads__
```
(pydwnldr)rkadam@rkadam-vbox:~/github/pydwnldr/src$ time python dwnldr.py http://ubuntu.mirrors.tds.net/pub/releases/15.10/ubuntu-15.10-desktop-amd64.iso
Downloading ubuntu-15.10-desktop-amd64.iso 1178386432 bytes

real    5m53.696s
user    0m0.764s
sys     0m32.244s
```
__8 Threads__
```
(pydwnldr)rkadam@rkadam-vbox:~/github/pydwnldr/src$ time python dwnldr.py http://ubuntu.mirrors.tds.net/pub/releases/15.10/ubuntu-15.10-desktop-amd64.iso
Downloading ubuntu-15.10-desktop-amd64.iso 1178386432 bytes

real    3m2.407s
user    0m1.040s
sys     0m36.796s
```
