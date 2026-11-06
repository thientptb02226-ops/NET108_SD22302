# -*- coding: utf-8 -*-
import os
import time
import shutil

SRC = r"C:\Net108Khai\Các Bài Lab\Lab1_NET108_AI_Native_Commerce_Updated.docx"
DST = r"C:\Net108Khai\Các Bài Lab\Lab1_NET108_AI_Native_Commerce.docx"

if not os.path.exists(SRC):
    print("Source updated file not found.")
    exit(0)

success = False
for attempt in range(5):
    try:
        shutil.copyfile(SRC, DST)
        os.remove(SRC)
        print(f"Successfully synced updated content to {DST}!")
        success = True
        break
    except PermissionError:
        print(f"Attempt {attempt+1}: File is still locked by Word/WPS. Waiting 1 second...")
        time.sleep(1)

if not success:
    print("Notice: Please close Word/WPS to allow replacing the file, or open Lab1_NET108_AI_Native_Commerce_Updated.docx.")
