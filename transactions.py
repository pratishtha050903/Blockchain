import requests
import matplotlib.pyplot as plt

# Etherscan API endpoint
ETHERSCAN_API_URL = "https://api.etherscan.io/api"

# Your Etherscan API key (sign up on Etherscan to get your own API key)
API_KEY = "INVE93Q249ZGN9D5NMH5JXAXJN6RB29VP5"

def get_transactions(address, start_block, end_block):
    """
    Get transactions for a given Ethereum address within a specified range of blocks.
    """
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": start_block,
        "endblock": end_block,
        "sort": "asc",
        "apikey": API_KEY
    }
    response = requests.get(ETHERSCAN_API_URL, params=params)
    if response.status_code == 200:
        return response.json()["result"]
    else:
        print("Failed to fetch transactions:", response.text)
        return []

def analyze_transactions(transactions):
    """
    Perform statistical analysis of Ethereum transactions and plot data.
    """
    total_transactions = len(transactions)
    unique_addresses = set()
    total_value = 0
    gas_used_values = []
    gas_price_values = []
    time_values = []

    for tx in transactions:
        if isinstance(tx, dict):
            unique_addresses.add(tx.get("to", ""))
            total_value += int(tx.get("value", 0))
            gas_used_values.append(int(tx.get("gasUsed", 0)))
            gas_price_values.append(int(tx.get("gasPrice", 0)))
            time_values.append(int(tx.get("timeStamp", 0)))

    avg_gas_used = sum(gas_used_values) / len(gas_used_values)
    avg_gas_price = sum(gas_price_values) / len(gas_price_values)

    # Plotting
    plt.figure(figsize=(10, 6))

    # Account Time vs Ether(ETH) Value
    plt.subplot(2, 1, 1)
    plt.plot(time_values, [int(tx.get("value", 0)) for tx in transactions], marker='o', linestyle='-')
    plt.xlabel('Time')
    plt.ylabel('Ether(ETH) Value')
    plt.title('Account Time vs Ether(ETH) Value')

    # Account Time vs Gas paid (in ETH)
    plt.subplot(2, 1, 2)
    plt.plot(time_values, [int(tx.get("gasPrice", 0)) * int(tx.get("gasUsed", 0)) for tx in transactions], marker='o', linestyle='-')
    plt.xlabel('Time')
    plt.ylabel('Gas paid (in ETH)')
    plt.title('Account Time vs Gas paid (in ETH)')

    plt.tight_layout()
    plt.show()

    print("Total Transactions:", total_transactions)
    print("Unique Addresses:", len(unique_addresses))
    print("Total Value Transferred:", total_value, "Wei")
    print("Average Gas Used:", avg_gas_used, "Wei")
    print("Average Gas Price:", avg_gas_price, "Wei")

def main():
    # Ethereum address to track transactions
    eth_address = "0x1234567890123456789012345678901234567890"

    # Define the range of blocks to fetch transactions from
    start_block = 10000  # Example start block
    end_block = 10001000    # Example end block

    transactions = get_transactions(eth_address, start_block, end_block)
    if transactions:
        analyze_transactions(transactions)
    else:
        print("No transactions found for the given address and block range.")

if __name__ == "__main__":
    main()
