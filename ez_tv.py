__author__ = 'TanJay'
#This will search for the tv series in todays view
from tkFont import BOLD
from operator import contains
import os
from Tkinter import *
import ttk
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import time
from time import gmtime, strftime
#import libtorrent as lt

#List items created
movie_list = []
magnet = []
added_list = []
down_queue = []

b = 0
i = 1
found = 0
root = Tk()
label = ttk.Label(root)
label.config(text = "Welcome To the eztv Control Panel", font = ("Monaco", 16, BOLD))
label.pack()


def main():
    series = ["Supernatural", "Flash", "Agents of Shield", "Big Bang"]
    url = "http://www.eztv.it"
    ez_site = requests.get(url)
    soup = BeautifulSoup(ez_site.content)
    ass = soup.find_all("td", {"class" : "forum_thread_post"})
    for line in ass:
        a = line.find_all("a")
        for asd in a:
            if " " in asd.text:
                for a in series:
                    if a in asd.text:
                        if not "720p" in asd.text:
                            movie_list.append(asd.text)
                            global down_queue
                            down_queue.append(asd)
    return movie_list
                        
   
#This will extract the magnet link from the URL
def url_mag(mag):
    url_magnet_ht = requests.get("https://eztv.it/%s" %(mag.get("href")))
    soup2 = BeautifulSoup(url_magnet_ht.content)
    find = soup2.find_all("a", {"class" : "magnet"})
    for list in find:
            magnet = list.get("href")
            #print(magnet)
            os.startfile(magnet)
            #mag_down(magnet)
  
#This will Download the torrent using the magnet link  
def mag_down(urlmag):
    ses = lt.session()
    params = { 'save_path': '/home/downloads/'}
    link = urlmag
    handle = lt.add_magnet_uri(ses, link, params)
    
    print("downloading metadata...")
    while (not handle.has_metadata()): time.sleep(1)
    print ("got metadata, starting torrent download...")
    while (handle.status().state != lt.torrent_status.seeding):
        print ('%d %% done' % (handle.status().progress*100))
        time.sleep(1)

# This will keep on checking for the new tv series from 10mins to 10mins                     
def check():
    num = cmp(added_list, main())
    neg = str(-1)
    if neg in str(num):
        print("Updated at %s" %(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
        time.sleep(600)
        check()
    else:
        for den in added_list:
           if main().find(den) != -1:
                print("updating in progress %s" %(den))
                loop_download(den)

                
# When found a episode after main search this will download that
def loop_download(link):
    url = "http://www.eztv.it"
    ez_site = requests.get(url)
    soup = BeautifulSoup(ez_site.content)
    ass = soup.find_all("td", {"class" : "forum_thread_post"})
    for line in ass:
        a = line.find_all("a")
        for asd in a:
            if " " in asd.text:
                    if link in asd.text:
                        if not "720p" in asd.text:
                            added_list.append(asd.text)
                            url_mag(asd)
    


def activity():
    for vs in main():
        added_list.append(vs)
        print(vs)
    for rep in down_queue:
        url_mag(rep)

            
          
activity()
root.mainloop()
check()
