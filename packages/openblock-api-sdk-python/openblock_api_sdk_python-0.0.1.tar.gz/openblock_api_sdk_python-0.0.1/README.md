# Python SDK for Openblock Wallet API

# API Documentation
- [Official documentation](https://docs.openblock.com/zh-Hans/OpenBlock/API/Enterprise%20Wallet/)

# Installation

```bash
pip install openblock-api-sdk-python
```

# Usage
> Consider `/openapi/company_wallet/balance/` as a reference, the full code can be located in the demo/api_demo directory.
* Get api key and secret

https://docs.openblock.com/OpenBlock/API/Enterprise%20Wallet/#overview

* Get your balance
```python
from openblock_api_sdk_python.client import CompanyWalletClient
import openblock_api_sdk_python.param.company_param as company_param

# Refer to https://docs.openblock.com/OpenBlock/API/Enterprise%20Wallet/#overview to get your api key and secret
client = CompanyWalletClient.CompanyWalletClient(
    api_key="YOUR API KEY",
    secret="YOUR SECRET",
)

params = company_param.GetBalanceParam()
params.chain_name = "Polygon"
params.page = 0
params.limit = 20
resp = client.get_balance(params)

if resp.status_code == 200:
    print(resp.json())
else:
    print(resp.text)

```
