# -*- coding: utf-8 -*-
import re
import pandas as pd
import numpy as np
import pymongo
from pymongo import MongoClient
import matplotlib.pyplot as plt

#flag=0 -> 현재, flag=1 -> 업데이트
global flag
#plot num
global n

def barChart(x, y):
    global flag
    global n

    if flag == 0:
        title = "Current total number of docs"
    else:
        title = "Updated total number of docs"

    ax = fig.add_subplot(n)
    n+=1
    ax.bar(x, y)
    ax.set_title(title)
    ax.set_ylabel('count')

    for i, v in enumerate(x):
        ax.text(v, y[i], str(y[i]), fontsize=10, color="black", horizontalalignment='center')

def barhChart(x, y):
    global flag
    global n

    if flag == 0:
        title = "Number of docs by news institutions"
    else:
        title = "Number of docs by paper institutions"

    ax = fig.add_subplot(n)
    n+=1
    ax.barh(x, y)
    ax.set_title(title)
    ax.set_xlabel('institution')
    ax.set_ylabel('count')

def delta_doc_cnt(df):
    '''
    <delta_doc_cnt 함수 description>

    1. before
        1. 마지막 행의 데이터 추출
        2. 이전에 저장된 뉴스 데이터 수 추출
        3. 이전에 저장된 문서 데이터 수 추출
        4. 이전에 저장된 전체 데이터 수 구하기
    2. after
        1. 현재 저장된 뉴스 데이터 수 추출
        2. 현재 저장된 문서 데이터 수 추출
        3. 현재 저장된 전체 데이터 수 구하기
    3. 현재 저장된 뉴스와 문서 데이터 수 그리고 전체 데이터 수 시각화
    4. update (delta)
        1. 업데이트된 전체 데이터 수 구하기
        2. 업데이트된 뉴스 수 구하기
        3. 업데이트된 문서 수 구하기
    5. 업데이트된 뉴스와 문서 데이터 수 그리고 전체 업데이트된 데이터 수 시각화
    '''
    global flag
    global n

    cnt_list = df.iloc[-1]
    print("마지막 행:", cnt_list)
    before_news = cnt_list[0]
    print("news:", before_news)
    before_paper = cnt_list[1]
    print("paper:", before_paper)
    before_total_doc = before_news + before_paper
    print("total:", before_total_doc)

    after_news = db.kubic_news.count_documents({})
    print("현재 저장된 뉴스 총 doc수:", after_news)
    after_paper = db.kubic_paper.count_documents({})
    print("현재 저장된 문서 총 doc수:", after_paper)
    after_total_doc = after_news + after_paper
    print("현재 저장된 전체 doc 수", after_total_doc)
    
    current_x = np.array(['news_doc_cnt', 'paper_doc_cnt', 'total_doc_cnt'])
    current_y = np.array([after_news, after_paper, after_total_doc])
   
    flag=0
    barChart(current_x, current_y)
    
    delta_doc_cnt = after_total_doc - before_total_doc
    print("updated total:", delta_doc_cnt)
    delta_news_cnt = after_news - before_news
    print("updated news:", delta_news_cnt)
    delta_paper_cnt = after_paper - before_paper
    print("updated paper:", delta_paper_cnt)
    
    updated_x = np.array(['updated_news_cnt', 'updated_paper_cnt', 'updated_total_cnt'])
    updated_y = np.array([delta_news_cnt, delta_paper_cnt, delta_doc_cnt])
    
    flag=1
    barChart(updated_x, updated_y)

    return after_news, after_paper, df

def doc_cnt_by_institution():
    '''
    <doc_cnt_by_institution 함수 description>
    
    1. 뉴스 collection에 저장된 distinct한 기관 리스트 추출
    2. 뉴스 기관별 데이터 수 추출
    3. 뉴스 기관별 데이터 수 시각화
    4. 문서 collection에 저장된 distinct한 기관 리스트 추출
    5. 문서 기관별 문서 수 추출
    6. 문서 기관별 데이터 수 시각화
    '''
    global flag
    global n
    
    news_doc_list = []
    news_institutions = db.kubic_news.distinct("published_institution", {})

    for institution in news_institutions:
        doc_cnt = db.kubic_news.count_documents({"published_institution":institution})
        news_doc_list.append(doc_cnt)
        print(institution, doc_cnt)
    
    news_x = np.array(news_institutions)
    news_y = np.array(news_doc_list)
    
    flag=0
    barhChart(news_x, news_y)

    paper_doc_list = []
    paper_institutions = db.kubic_paper.distinct("published_institution", {})

    for institution in paper_institutions:
        doc_cnt = db.kubic_paper.count_documents({"published_institution":institution})
        paper_doc_list.append(doc_cnt)
        print(institution, doc_cnt)

    paper_x = np.array(paper_institutions)
    paper_y = np.array(paper_doc_list)

    flag=1
    barhChart(paper_x, paper_y)

def write_last_cnt(after_news, after_paper, df):
    '''
    <write_last_cnt 함수 description>
    업데이트된 각 카테고리의 데이터 수 csv파일에 쓰기
    '''
    new_row = pd.DataFrame([[after_news, after_paper]], columns = df.columns)
    new_df = pd.concat([df.iloc[:-1], new_row, df.iloc[-1:]], ignore_index=False)
    new_df.to_csv("./newsPaper_docCnt.csv", index=False)
    print("new_df:", new_df)    

if __name__ == '__main__':
    csv_file = '/home/minjoo/mongo_data_cnt/newsPaper_docCnt.csv'
    df = pd.read_csv(csv_file)

    client = MongoClient("mongodb://kubic-test:epp2022!@127.0.0.1")
    db = client.KUBIC

    plt.rc('font', family='NanumGothic')
    plt.rcParams['axes.unicode_minus'] = False

    fig = plt.figure(figsize=(20, 20))
    
    global n
    n = 221
    after_news, after_paper, df = delta_doc_cnt(df)
    doc_cnt_by_institution()
    write_last_cnt(after_news, after_paper, df)
   
    plt.tight_layout()
    plt.show()
    plt.savefig('crawling_aggregation.png')
    
    print("!finish!")


