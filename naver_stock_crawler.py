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
            company_name = company_name_element.text.strip() if company_name_element else "N/A"
            
            # 현재 주가 가져오기
            current_price_element = soup.select_one('.no_today .blind')
            current_price = current_price_element.text.strip() if current_price_element else "N/A"
            
            # 전일 대비 가격 변동 가져오기
            change_element = soup.select_one('.no_exday .blind')
            change_price = change_element.text.strip() if change_element else "N/A"
            
            # 등락률 가져오기
            change_rate_element = soup.select_one('.no_exday em')
            change_rate = change_rate_element.text.strip() if change_rate_element else "N/A"
            
            # 거래량 가져오기
            volume_element = soup.select_one('table.no_info tr:nth-child(1) td:nth-child(4) em')
            volume = volume_element.text.strip() if volume_element else "N/A"
            
            # 시가총액 가져오기
            market_cap_element = soup.select_one('table.no_info tr:nth-child(3) td:nth-child(2) em')
            market_cap = market_cap_element.text.strip() if market_cap_element else "N/A"
            
            # PER 가져오기
            per_element = soup.select_one('#_per')
            per = per_element.text.strip() if per_element else "N/A"
            
            # PBR 가져오기
            pbr_element = soup.select_one('#_pbr')
            pbr = pbr_element.text.strip() if pbr_element else "N/A"
            
            # 52주 최고/최저가 가져오기
            high_52w_element = soup.select_one('table.no_info tr:nth-child(4) td:nth-child(2) em')
            high_52w = high_52w_element.text.strip() if high_52w_element else "N/A"
            
            low_52w_element = soup.select_one('table.no_info tr:nth-child(4) td:nth-child(4) em')
            low_52w = low_52w_element.text.strip() if low_52w_element else "N/A"
            
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
                '조회시간': time.strftime('%Y-%m-%d %H:%M:%S')
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
        print("=" * 50)

def main():
    """메인 함수"""
    crawler = NaverStockCrawler()
    
    # 삼성전자 주가 정보 가져오기
    samsung_info = crawler.get_stock_info('005930')
    crawler.print_stock_info(samsung_info)
    
    # 다른 종목들도 테스트해보기
    print("\n다른 종목 정보:")
    
    # SK하이닉스
    sk_hynix_info = crawler.get_stock_info('000660')
    crawler.print_stock_info(sk_hynix_info)
    
    # NAVER
    naver_info = crawler.get_stock_info('035420')
    crawler.print_stock_info(naver_info)

if __name__ == "__main__":
    main()