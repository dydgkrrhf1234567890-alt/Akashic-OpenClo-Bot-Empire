import os
import time
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# 환경 변수에서 RPC URL, 지갑 프라이빗 키 불러오기
RPC_URL = os.getenv("POLYGON_RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
MY_ADDRESS = Web3.toChecksumAddress(os.getenv("MY_ADDRESS"))  # 0xd5ea893E19278a4E8cCA88a5E1447Da17C72f7ac

# 스마트컨트랙트 주소 및 ABI (예시)
CONTRACT_ADDRESS = Web3.toChecksumAddress("0xYourContractAddress")  # 본인 스마트컨트랙트 주소로 변경 필요
CONTRACT_ABI = [
    # 필수 부분만 간략화, 실제 ABI 넣을 것
    {
        "inputs": [],
        "name": "claimProfit",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getPendingProfit",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

def main():
    # 1. Web3 연결
    web3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not web3.isConnected():
        print("RPC 연결 실패")
        return

    # 2. 스마트컨트랙트 객체 생성
    contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    
    # 3. 현재 대기중인 수익 조회
    pending_profit = contract.functions.getPendingProfit().call({'from': MY_ADDRESS})
    pending_eth = web3.fromWei(pending_profit, 'ether')
    print(f"대기중인 수익: {pending_eth} POL")

    # 4. 수익이 최소 기준 이상일 경우 청구 수행
    MINIMUM_CLAIM_AMOUNT = web3.toWei(0.01, 'ether')
    if pending_profit >= MINIMUM_CLAIM_AMOUNT:
        print("수익 청구 실행!")
        
        # 트랜잭션 빌드
        nonce = web3.eth.get_transaction_count(MY_ADDRESS)
        txn = contract.functions.claimProfit().buildTransaction({
            'chainId': 137,  # 폴리곤 메인넷 체인ID
            'gas': 200000,
            'gasPrice': web3.eth.gas_price,
            'nonce': nonce
        })
        
        # 서명 후 전송
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"청구 트랜잭션 전송됨: {web3.toHex(tx_hash)}")

        # 트랜잭션 완료 대기
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print("트랜잭션 완료:", receipt.status)
    else:
        print("청구 대기 조건 미충족. 다음에 다시 시도.")

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print("오류 발생:", e)
        # 5분마다 실행 (원하는 주기로 조정 가능)
        time.sleep(300)
