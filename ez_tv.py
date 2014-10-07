__author__ = 'TanJay'
#This will search for the tv series in todays view
import os
from Tkinter import *
import ttk
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import time


i = 1
found = 0
root = Tk()
def main():
    series = ["Supernatural", "Black", "Agents of Shield", "Big Bang"]
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
                      print("%s as %s in link" %(asd.text, asd.get("href")))
                    else:
                      time.sleep(1800)
                      main()
                    

main()
