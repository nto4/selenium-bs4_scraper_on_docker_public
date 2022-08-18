# -*- coding:utf-8 -*-
# encoding:utf-8
import os
import subprocess
import logging
import time

say = 0
from apscheduler.schedulers.background import BlockingScheduler  # BackgroundScheduler
logging.basicConfig(handlers=[logging.FileHandler(filename="./schedule_check.log",
                                                 encoding='utf-8', mode='a+')],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%F %A %T",
                    level=logging.INFO)



# main.py
def nftevening_main_scraper():
    proc = subprocess.Popen(['python', '/app/code/main.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    contex = proc.communicate()[0]
    print(contex)
    p_status = proc.wait()
    logging.info("nftevening main scraper worked")
    print("nftevening main scraper worked")




def nftevening_today_scraper():
    proc = subprocess.Popen(['python', '/app/code/today.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    contex = proc.communicate()[0]
    print(contex)
    p_status = proc.wait()
    logging.info("nftevening today scraper worked")
    print("nftevening today scraper worked")





def nftevening_past_scraper():
    proc = subprocess.Popen(['python', '/app/code/past.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    contex = proc.communicate()[0]
    print(contex)
    p_status = proc.wait()
    logging.info("nftevening past scraper worked")
    print("nftevening past scraper worked")

nftevening_today_scraper()
time.sleep(180)
nftevening_main_scraper()
time.sleep(180)
nftevening_past_scraper()




sched = BlockingScheduler(daemon=True)
sched.add_job(nftevening_today_scraper,'cron', hour=22, minute='35')
sched.add_job(nftevening_main_scraper,'cron', hour=22, minute='55')
sched.add_job(nftevening_past_scraper,'cron', hour=23, minute='45')




#sched.add_job(sensor,'interval',seconds=1)
sched.start()