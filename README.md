# 네이버 금융 주가 크롤러

네이버 금융 사이트에서 주식 정보를 크롤링하는 Python 스크립트입니다.

## 🚀 기능

- 실시간 주가 정보 조회
- 전일 대비 변동률 및 변동금액
- 거래량, 시가총액 정보
- PER, PBR 투자지표
- 52주 최고/최저가
- 여러 종목 일괄 조회

## 📋 요구사항

```bash
pip install requests beautifulsoup4 lxml
```

## 🔧 사용법

### 1. 기본 사용법 (단일 종목)

```python
from naver_stock_crawler_v2 import NaverStockCrawler

# 크롤러 인스턴스 생성
crawler = NaverStockCrawler()

# 삼성전자(005930) 정보 조회
stock_info = crawler.get_stock_info('005930')
crawler.print_stock_info(stock_info)
```

### 2. 간단한 주가만 조회

```python
# 현재가만 빠르게 조회
price = crawler.get_simple_stock_price('005930')
print(f"삼성전자 현재가: {price}원")
```

### 3. 여러 종목 일괄 조회

```python
stocks = {
    '005930': '삼성전자',
    '000660': 'SK하이닉스', 
    '035420': 'NAVER',
    '005380': '현대차',
    '051910': 'LG화학'
}

for code, name in stocks.items():
    price = crawler.get_simple_stock_price(code)
    print(f"{name}({code}): {price}원")
```

## 📊 출력 예시

```
==================================================
📈 삼성전자 (005930)
==================================================
현재가:    60,200원
전일대비:  400 (상승)
등락률:    +0.67%
거래량:    59,800
시가총액:  61,100억원
PER:       11.66
PBR:       1.02
52주최고:  60,200원
52주최저:  49,900원
조회시간:  2025-07-01 19:54:33
URL:       https://finance.naver.com/item/main.naver?code=005930
==================================================
```

## 🏃‍♂️ 실행 방법

```bash
# 기본 실행 (삼성전자 및 여러 종목 조회)
python3 naver_stock_crawler_v2.py

# 또는 직접 실행
python3 -c "
from naver_stock_crawler_v2 import NaverStockCrawler
crawler = NaverStockCrawler()
info = crawler.get_stock_info('005930')
crawler.print_stock_info(info)
"
```

## 📝 주요 종목 코드

| 종목명 | 코드 |
|--------|------|
| 삼성전자 | 005930 |
| SK하이닉스 | 000660 |
| NAVER | 035420 |
| 현대차 | 005380 |
| LG화학 | 051910 |
| 카카오 | 035720 |
| 셀트리온 | 068270 |
| 포스코홀딩스 | 005490 |

## ⚠️ 주의사항

1. **서버 부하 방지**: 연속적인 요청 시 `time.sleep()`을 사용하여 간격을 두세요.
2. **네트워크 상태**: 인터넷 연결 상태를 확인하세요.
3. **사이트 구조 변경**: 네이버 금융 사이트 구조가 변경되면 셀렉터 수정이 필요할 수 있습니다.
4. **사용 제한**: 과도한 크롤링은 IP 차단의 위험이 있습니다.

## 🛠️ 커스터마이징

### User-Agent 변경
```python
crawler = NaverStockCrawler()
crawler.headers['User-Agent'] = 'Your Custom User Agent'
```

### 타임아웃 설정
```python
response = requests.get(url, headers=self.headers, timeout=10)
```

## 🔍 문제 해결

### 1. 데이터가 "N/A"로 표시되는 경우
- 네이버 금융 사이트 구조 변경 가능성
- 해당 종목의 데이터 제공 여부 확인

### 2. 네트워크 오류 발생 시
- 인터넷 연결 상태 확인
- 방화벽 또는 프록시 설정 확인

### 3. 패키지 설치 오류
```bash
# 가상환경 사용 권장
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 🤝 기여하기

버그 리포트나 기능 개선 제안은 언제든지 환영합니다!

---

**면책조항**: 이 도구는 교육 목적으로 제작되었습니다. 투자 결정은 본인의 책임하에 이루어져야 합니다.