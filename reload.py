import streamlit as st
import os
import threading
import time
wait_second = 10
def threadFunc():
   time.sleep(wait_second)
   
def reload(page):
    th = threading.Thread(target=threadFunc)
    th.start()
    os.system(r"streamlit run " + page + ".py")
    th.join()