import time
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv('POLYGON_RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
MY_ADDRESS = os.getenv('MY_ADDRESS')
web3 = Web3(Web3.HTTPProvider(RPC_URL))

def main():
    if not web3.isConnected():
        print("RPC 연결 실패")
        return

    # 자동 수익 청구 로직(간단히 예시)
    print(f"자동 수익 청구 봇 실행 중({MY_ADDRESS})")

    # 여기서 스마트컨트랙트 호출 및 트랜잭션 서명, 전송 구현

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(f"오류 발생: {e}")
        time.sleep(300)  # 5분마다 실행
