# :bar_chart: Automated crawl aggregation system

## Introduction
크롤링 집계 자동화 시스템은 백엔드에서 매일 수집한 뉴스와 문서 데이터를 기관별로 분리하여 집계한다. 이 집계된 데이터는 시각화된 이미지 파일로 생성되며, 해당 파일은 사용자가 이메일을 통해 받을 수 있도록 자동으로 전송된다.

## How It Work
1. 데이터 집계
   - crawling_aggregation.py 스크립트는 MongoDB에 저장된 뉴스 및 문서 데이터를 조회하여 현재 데이터 수와 각 기관별 데이터 수를 집계한다. 
3. CSV 파일 사용
   - 집계된 데이터는 newsPaper_docCnt.csv 파일에 저장되며, 이 파일은 이전 및 현재 집계된 데이터의 기록을 보관한다.
   - 스크립트 실행 시, CSV 파일에서 마지막으로 기록된 데이터 수를 읽어와 이전 데이터 수와 비교한다. 이를 통해 새로 크롤링된 데이터의 양을 계산한다.
4. 데이터 시각화
   - 집계된 데이터는 bar chart를 사용하여 시각화된다. 이 차트들은 현재 데이터 수, 각 기관별 데이터 수, 그리고 업데이트된 데이터 수를 보여준다.
5. 이메일 전송
   - 시각화된 차트를 포함한 이미지 파일은 crawling_aggregation.sh 쉘 스크립트를 통해 이메일로 전송된다.
6. 자동화 실행
   - 다음과 같은 crontab 설정을 통해 crawling_aggregation.sh 스크립트는 매일 자동으로 실행된다. 실행 결과는 로그 파일 crawling_aggregation.log에 기록된다.
   ```shell
    00 1 * * * /home/minjoo/mongo_data_cnt/crawling_aggregation.sh >> /home/minjoo/mongo_data_cnt/crawling_aggregation.log 2>&1
    ```
## Dependency
- MongoDB
- Python 3.7
- pandas, numpy, matplotlib, pymongo

## Result
![crawling_aggregation](https://github.com/MinjooShin/Automated-crawl-aggregation-system/assets/74174008/3d1a807e-6b1e-4f0a-9594-3ace529ddf02)

크롤링 집계 자동화 시스템은 집계 결과를 네 개의 그래프를 통해 시각화한다.
- 현재 총 데이터 수: 첫 번째 그래프는 현재 데이터베이스에 저장된 news와 paper 데이터의 수, 그리고 이 둘을 합친 총 데이터의 수를 막대 차트로 보여준다. 이를 통해 관리자는 각 카테고리의 현재 데이터 크기를 한눈에 파악할 수 있다.
- 업데이트된 총 데이터 수: 두 번째 그래프는 최근 크롤링으로 인한 데이터 증가량을 막대 차트로 보여준다. 새로운 news와 paper 데이터의 증가 수, 그리고 업데이트된 총 데이터의 수를 각각 비교할 수 있다.
- 뉴스 기관별 데이터 수: 세 번째 그래프는 horizontal bar chart를 사용하여 각 news 기관별로 저장된 데이터의 수를 나타낸다. 각 바는 특정 뉴스 기관에서 발행한 데이터의 양을 나타내며, 이를 통해 어떤 기관이 데이터베이스 내에서 가장 많은 뉴스를 제공하고 있는지 알 수 있다.
- 문서 기관별 데이터 수: 마지막 그래프는 paper 기관별로 저장된 데이터의 수를 horizontal bar chart로 보여준다. 각 바는 특정 문서 기관에서 발행한 데이터의 양을 나타내며, 이를 통해 어떤 기관이 데이터베이스에서 가장 많은 문서를 제공하고 있는지 쉽게 파악할 수 있다.

## Technology of Use
- Python: 데이터 집계 및 시각화
- MongoDB: 뉴스 및 문서 데이터 저장
- matplotlib: 데이터 시각화
- pandas: 데이터 분석 및 CSV 파일 처리
- crontab: 스크립트 자동 실행 스케줄링
