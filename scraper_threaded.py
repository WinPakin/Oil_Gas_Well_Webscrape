from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import util
import json
import sys
import time
import threading
import math
# Author: Pakin Wirojwatanakul

# Log status
logging.basicConfig(level=logging.INFO)

# Scraper Thread Class
class Scrape_Thread (threading.Thread):
   def __init__(self, name, start_idx, end_idx):
      threading.Thread.__init__(self)
      self.name = name
      self.start_idx = start_idx
      self.end_idx = end_idx
   def run(self):
      # does the actual scraping with util.scrape
      util.scrape(self.name, self.start_idx, self.end_idx)


# partition the total number of requests into quartiles.
start = int(sys.argv[1])
end = int(sys.argv[2])
interval = end - start
q1 = start + math.floor(interval / 4)
q2 = start + math.floor(interval / 2)
q3 = start + math.floor(interval * (3 / 4))

# Create new threads.
# Assigns a quater of the work to each thread.
thread_1 = Scrape_Thread("Thread 1", start, q1)
thread_2 = Scrape_Thread("Thread 2", q1, q2)
thread_3 = Scrape_Thread("Thread 3", q2, q3)
thread_4 = Scrape_Thread("Thread 4", q3, end)

# Start new threads.
thread_1.start()
thread_2.start()
thread_3.start()
thread_4.start()
