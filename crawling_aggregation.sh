#!/bin/sh
export PATH=/home/minjoo/bin/miniconda3/envs/py37/bin:$PATH

cd /home/minjoo/mongo_data_cnt
python crawling_aggregation.py

uuencode crawling_aggregation.png crawling_aggregation.png | mail -s "Crawling Aggregation" minjooshin@handong.ac.kr
