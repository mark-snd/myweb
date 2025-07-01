#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
네이버 금융 주가 크롤러 사용 예제

이 파일은 naver_stock_crawler_v2.py를 사용하는 다양한 예제를 보여줍니다.
"""

from naver_stock_crawler_v2 import NaverStockCrawler
import time

def example_single_stock():
    """단일 종목 조회 예제"""
    print("=" * 60)
    print("🔍 단일 종목 조회 예제")
    print("=" * 60)
    
    crawler = NaverStockCrawler()
    
    # 삼성전자 정보 조회
    stock_info = crawler.get_stock_info('005930')
    if stock_info:
        crawler.print_stock_info(stock_info)
    else:
        print("❌ 주식 정보를 가져올 수 없습니다.")

def example_multiple_stocks():
    """여러 종목 조회 예제"""
    print("\n" + "=" * 60)
    print("📊 여러 종목 조회 예제")
    print("=" * 60)
    
    crawler = NaverStockCrawler()
    
    # 주요 종목들
    stocks = {
        '005930': '삼성전자',
        '000660': 'SK하이닉스',
        '035420': 'NAVER',
        '005380': '현대차',
        '051910': 'LG화학',
        '035720': '카카오',
        '068270': '셀트리온'
    }
    
    print("📈 현재 주가 조회 결과:")
    print("-" * 40)
    
    for code, name in stocks.items():
        price = crawler.get_simple_stock_price(code)
        print(f"{name:>8} ({code}): {price:>12}원")
        time.sleep(0.3)  # 서버 부하 방지

def example_custom_stock():
    """사용자 입력 종목 조회 예제"""
    print("\n" + "=" * 60)
    print("✏️  사용자 입력 종목 조회 예제")
    print("=" * 60)
    
    crawler = NaverStockCrawler()
    
    print("종목 코드를 입력하세요 (예: 005930)")
    print("종료하려면 'quit' 또는 'exit'를 입력하세요.")
    
    while True:
        try:
            stock_code = input("\n종목 코드: ").strip()
            
            if stock_code.lower() in ['quit', 'exit', 'q']:
                print("👋 프로그램을 종료합니다.")
                break
            
            if not stock_code:
                print("❌ 종목 코드를 입력해주세요.")
                continue
            
            if len(stock_code) != 6 or not stock_code.isdigit():
                print("❌ 올바른 6자리 종목 코드를 입력해주세요.")
                continue
            
            print(f"🔍 {stock_code} 종목 정보를 조회중...")
            stock_info = crawler.get_stock_info(stock_code)
            
            if stock_info:
                print()
                crawler.print_stock_info(stock_info)
            else:
                print(f"❌ {stock_code} 종목 정보를 찾을 수 없습니다.")
                
        except KeyboardInterrupt:
            print("\n👋 프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

def example_price_comparison():
    """가격 비교 예제"""
    print("\n" + "=" * 60)
    print("⚖️  가격 비교 예제")
    print("=" * 60)
    
    crawler = NaverStockCrawler()
    
    # 비교할 종목들 (IT 관련 주식)
    it_stocks = {
        '005930': '삼성전자',
        '035420': 'NAVER',
        '035720': '카카오',
        '018260': '삼성에스디에스',
        '036570': '엔씨소프트'
    }
    
    print("💻 IT 관련 주식 가격 비교:")
    print("-" * 50)
    
    stock_prices = []
    
    for code, name in it_stocks.items():
        price_str = crawler.get_simple_stock_price(code)
        try:
            # 가격 문자열에서 숫자만 추출
            price = int(price_str.replace(',', '').replace('원', ''))
            stock_prices.append((name, code, price, price_str))
        except:
            stock_prices.append((name, code, 0, price_str))
        time.sleep(0.3)
    
    # 가격순으로 정렬
    stock_prices.sort(key=lambda x: x[2], reverse=True)
    
    for i, (name, code, price, price_str) in enumerate(stock_prices, 1):
        print(f"{i}. {name:>12} ({code}): {price_str:>12}")

def main():
    """메인 함수"""
    print("🚀 네이버 금융 주가 크롤러 예제 프로그램")
    print("=" * 60)
    
    # 각 예제 실행
    example_single_stock()
    example_multiple_stocks()
    example_price_comparison()
    
    # 사용자 입력 예제는 마지막에 (대화형)
    print("\n" + "=" * 60)
    response = input("사용자 입력 예제를 실행하시겠습니까? (y/n): ").strip().lower()
    if response in ['y', 'yes', '예', 'ㅇ']:
        example_custom_stock()
    
    print("\n🎉 모든 예제가 완료되었습니다!")

if __name__ == "__main__":
    main()