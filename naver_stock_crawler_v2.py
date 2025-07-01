import requests
from bs4 import BeautifulSoup
import re
import time

class NaverStockCrawler:
    def __init__(self):
        self.base_url = "https://finance.naver.com/item/main.naver?code="
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def get_stock_info(self, stock_code):
        """
        네이버 금융에서 주식 정보를 가져오는 함수
        
        Args:
            stock_code (str): 주식 종목 코드 (예: '005930')
        
        Returns:
            dict: 주식 정보 딕셔너리
        """
        try:
            url = self.base_url + stock_code
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 회사명 가져오기
            company_name_element = soup.select_one('.wrap_company h2 a')
            if not company_name_element:
                company_name_element = soup.select_one('h2 a')
            company_name = company_name_element.text.strip() if company_name_element else "N/A"
            
            # 현재 주가 가져오기 - 여러 셀렉터 시도
            current_price = "N/A"
            price_selectors = [
                '.no_today .blind',
                '.today .blind',
                '#_nowVal',
                '.no_today strong',
                '.rate_info .no_today em'
            ]
            
            for selector in price_selectors:
                price_element = soup.select_one(selector)
                if price_element:
                    current_price = price_element.text.strip()
                    break
            
            # 전일 대비 가격 변동 가져오기
            change_price = "N/A"
            change_selectors = [
                '.no_exday .blind',
                '.change .blind',
                '#_diff',
                '.no_exday strong'
            ]
            
            for selector in change_selectors:
                change_element = soup.select_one(selector)
                if change_element:
                    change_price = change_element.text.strip()
                    break
            
            # 등락률 가져오기
            change_rate = "N/A"
            rate_selectors = [
                '.no_exday em',
                '.change em',
                '#_rate'
            ]
            
            for selector in rate_selectors:
                rate_element = soup.select_one(selector)
                if rate_element:
                    change_rate = rate_element.text.strip()
                    break
            
            # 거래량 가져오기
            volume = "N/A"
            volume_selectors = [
                'table.no_info tr:nth-child(1) td:nth-child(4) em',
                'table tr:contains("거래량") em',
                '#_quant'
            ]
            
            for selector in volume_selectors:
                volume_element = soup.select_one(selector)
                if volume_element:
                    volume = volume_element.text.strip()
                    break
            
            # 시가총액 가져오기
            market_cap = "N/A"
            cap_selectors = [
                'table.no_info tr:nth-child(3) td:nth-child(2) em',
                'table tr:contains("시가총액") em'
            ]
            
            for selector in cap_selectors:
                cap_element = soup.select_one(selector)
                if cap_element:
                    market_cap = cap_element.text.strip()
                    break
            
            # PER 가져오기
            per_element = soup.select_one('#_per')
            per = per_element.text.strip() if per_element else "N/A"
            
            # PBR 가져오기
            pbr_element = soup.select_one('#_pbr')
            pbr = pbr_element.text.strip() if pbr_element else "N/A"
            
            # 52주 최고/최저가 가져오기
            high_52w = "N/A"
            low_52w = "N/A"
            
            high_selectors = [
                'table.no_info tr:nth-child(4) td:nth-child(2) em',
                'table tr:contains("52주") em:first-child'
            ]
            
            for selector in high_selectors:
                high_element = soup.select_one(selector)
                if high_element:
                    high_52w = high_element.text.strip()
                    break
            
            low_selectors = [
                'table.no_info tr:nth-child(4) td:nth-child(4) em',
                'table tr:contains("52주") em:last-child'
            ]
            
            for selector in low_selectors:
                low_element = soup.select_one(selector)
                if low_element:
                    low_52w = low_element.text.strip()
                    break
            
            return {
                '종목코드': stock_code,
                '회사명': company_name,
                '현재가': current_price,
                '전일대비': change_price,
                '등락률': change_rate,
                '거래량': volume,
                '시가총액': market_cap,
                'PER': per,
                'PBR': pbr,
                '52주최고': high_52w,
                '52주최저': low_52w,
                '조회시간': time.strftime('%Y-%m-%d %H:%M:%S'),
                'URL': url
            }
            
        except requests.exceptions.RequestException as e:
            print(f"네트워크 오류 발생: {e}")
            return None
        except Exception as e:
            print(f"데이터 파싱 오류 발생: {e}")
            return None
    
    def print_stock_info(self, stock_info):
        """주식 정보를 보기 좋게 출력하는 함수"""
        if stock_info is None:
            print("주식 정보를 가져올 수 없습니다.")
            return
        
        print("=" * 50)
        print(f"📈 {stock_info['회사명']} ({stock_info['종목코드']})")
        print("=" * 50)
        print(f"현재가:    {stock_info['현재가']}원")
        print(f"전일대비:  {stock_info['전일대비']} ({stock_info['등락률']})")
        print(f"거래량:    {stock_info['거래량']}")
        print(f"시가총액:  {stock_info['시가총액']}")
        print(f"PER:       {stock_info['PER']}")
        print(f"PBR:       {stock_info['PBR']}")
        print(f"52주최고:  {stock_info['52주최고']}원")
        print(f"52주최저:  {stock_info['52주최저']}원")
        print(f"조회시간:  {stock_info['조회시간']}")
        print(f"URL:       {stock_info['URL']}")
        print("=" * 50)

    def get_simple_stock_price(self, stock_code):
        """간단하게 현재 주가만 가져오는 함수"""
        try:
            url = self.base_url + stock_code
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 현재 주가 가져오기
            price_selectors = [
                '.no_today .blind',
                '.today .blind',
                '#_nowVal',
                '.no_today strong'
            ]
            
            for selector in price_selectors:
                price_element = soup.select_one(selector)
                if price_element:
                    return price_element.text.strip()
            
            return "N/A"
            
        except Exception as e:
            print(f"오류 발생: {e}")
            return "N/A"

def main():
    """메인 함수"""
    crawler = NaverStockCrawler()
    
    print("🚀 네이버 금융 주가 크롤러 시작!\n")
    
    # 삼성전자 주가 정보 가져오기
    print("1. 삼성전자 주가 정보:")
    samsung_info = crawler.get_stock_info('005930')
    crawler.print_stock_info(samsung_info)
    
    print("\n" + "="*60 + "\n")
    
    # 간단한 주가 조회 예제
    print("2. 간단한 주가 조회:")
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
        time.sleep(0.5)  # 서버 부하 방지

if __name__ == "__main__":
    main()