import requests

# URL of the NSE page that lists stock names
url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"

# Headers to include in the request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    "Cookie": "_ga=GA1.1.960283774.1716295466; _ga_QJZ4447QD3=GS1.1.1716295488.1.1.1716295533.0.0.0; nsit=TOEftrVkLMxSMEaOscW3CLYr; 
              AKA_A2=A; _abck=F54BF07DD29CEEC70D63CB33D0A5CFEF~0~YAAQPK3OFy0p/V6UAQAAxP83jA3lIgXC1+ML3+07ZloD6LSqxy9QCkl8ZydJHkOZCTRp7w28Y1bZw1fVf5/IGNPVN0askHXGajs/PvFAfWbh/def4Rlfsvt2nH1FENNTlcOKmBtgFSYvUn4YPMb0dI0SZ1n0DcU7TF43c5FurnxpfZ2K5nbGn0DMpKVuHDwSiJyLZc3ZvDBf9IMsWJVll08DTd+LflZThxs6XXcAre+kVwzHaooINxtQUW/g2YAiVp/7lOm+6SNBJG03adUSELKjo7HY4WPcbmSmEaXmsUq+dYdxGWj1kX5iI3CcJdrnGz1RVeMVgqO2FelBfh2z0tpDBKLdYC9A8ibHpQcQyQAfGxixQ4HzKjWOZshoNs01Hp4HMKn83YXsyaMUMSqGOfjbIJ5Vq5BCzF2mzTx1o3Tb+oZn4TDTiQSwvaX3t8m6gK/NCXhLEG/cg/QROYtNUE5yXG7R2U68u5rJTCvIF81gqdeCC3ajcIYQaHSxWQ==~-1~-1~-1;",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5"
}

# Send GET request to fetch the content
response = requests.get(url, headers=headers)

# Check if the response is successful
if response.status_code == 200:
    data = response.json()  # Assuming the response is JSON
    # Extract stock names
    for stock in data.get('data', []):
        print(stock.get('symbol'))  # Replace 'symbol' with the key for stock names in the JSON
else:
    print(f"Failed to fetch page. Status code: {response.status_code}")
