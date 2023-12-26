import copy
import hashlib
import hmac
import json
from urllib.parse import urljoin
from uuid import uuid4

import requests

import openblock_api_sdk_python.param.company_param as company_param


class CompanyWalletClient:
    def __init__(self, api_key, secret, server="https://auth.openblock.com"):
        self.api_key = api_key
        self.secret = secret
        self.server = server

    def get_wallet_info(self):
        """
        Refer to https://docs.openblock.com/OpenBlock/API/Enterprise%20Wallet/#get-company-wallet-information
        """
        return self._do_req("GET", "/openapi/company_wallet/info/")

    def get_hd_wallet_address(self, params: company_param.GetHdWalletAddressParam):
        """
        Refer to https://docs.openblock.com/OpenBlock/API/Enterprise%20Wallet/#get-company-wallet-hd-wallet-address
        """
        return self._do_req(
            "GET", "/openapi/company_wallet/hd_wallet_address/", object2dict(params)
        )

    def get_balance(self, params: company_param.GetBalanceParam):
        """
        Refer to https://docs.openblock.com/OpenBlock/API/Enterprise%20Wallet/#get-wallet-balance
        """
        return self._do_req(
            "GET", "/openapi/company_wallet/balance/", object2dict(params)
        )

    def add_custom_token(self, params: company_param.AddCustomTokenParam):
        """
        Refer to https://docs.openblock.com/OpenBlock/API/Enterprise%20Wallet/#add-custom-token
        """
        params_dict = object2dict(params, ["token_data"])
        if params.token_data:
            token_data = object2dict(params.token_data)
            params_dict["token_data"] = json.dumps(token_data)
        return self._do_req(
            "POST", "/openapi/company_wallet/custom_token/", params=params_dict
        )

    def get_transaction_histroy(self, params: company_param.GetTransactionHistroyParam):
        """
        Refer to https://docs.openblock.com/OpenBlock/API/Enterprise%20Wallet/#transaction-history
        """
        return self._do_req(
            "GET",
            "/openapi/company_wallet/tx_history/",
            params=object2dict(params),
        )

    def get_approvals(self, params: company_param.GetApprovalsParam):
        """
        Refer to https://docs.openblock.com/OpenBlock/API/Enterprise%20Wallet/#get-approval-list
        """
        return self._do_req(
            "GET", "/openapi/company_wallet/approvals/", params=object2dict(params)
        )

    def new_approval(self, params: company_param.NewApprovalParam):
        """
        Refer to https://docs.openblock.com/OpenBlock/API/Enterprise%20Wallet/#create-transaction-approval
        """
        params_dict = object2dict(params, ["txinfo"])
        if params.txinfo:
            txinfo = object2dict(params.txinfo, ["fromAddress", "dappInfo"])
            if params.txinfo.fromAddress:
                txinfo["from"] = params.txinfo.fromAddress
            if params.txinfo.dappInfo:
                txinfo["dappInfo"] = object2dict(params.txinfo.dappInfo)
            params_dict["txinfo"] = json.dumps(txinfo)
        return self._do_req(
            "POST", "/openapi/company_wallet/approval/new/", params=params_dict
        )

    def agree_approval(self, params: company_param.AgreeApprovalParam):
        """
        Refer to https://docs.openblock.com/OpenBlock/API/Enterprise%20Wallet/#approvereject-approval
        """
        return self._do_req(
            "POST",
            "/openapi/company_wallet/approval/agree/",
            params=object2dict(params),
        )

    def _do_req(self, method, path, params=None, **kwargs):
        params = params or {}
        method = method.upper()

        if method not in ["GET", "POST"]:
            raise ValueError("method must be GET or POST")

        params = self._gen_params(params)

        url = urljoin(self.server, path)
        if method == "GET":
            response = requests.get(url, params=params, **kwargs)
        else:
            response = requests.post(url, data=params, **kwargs)

        return response

    def _gen_params(self, params: dict) -> dict:
        ret = copy.deepcopy(params)
        ret["nonce"] = params.get("nonce") or str(uuid4()).upper()
        ret["sign"] = self._gen_sign(ret)
        ret["api_key"] = self.api_key
        return ret

    def _gen_sign(self, params: dict) -> str:
        # order keys in alpha ascending
        params = {k: params[k] for k in sorted(params)}
        strs = "&".join(["{0}={1}".format(k, v) for k, v in params.items()])
        strs = f"{strs}&api_key={self.api_key}"

        return _hmac_sha256(self.secret, strs).upper()


def _hmac_sha256(key, message):
    """Encrypt the message using HmacSHA256 algorithm"""

    key = bytes(key, "utf-8")
    message = bytes(message, "utf-8")
    return hmac.new(key, message, hashlib.sha256).hexdigest()


def object2dict(params, except_key=None):
    if not except_key:
        except_key = []
    params_dict = {}
    for key, value in params.__dict__.items():
        if key not in except_key and value is not None:
            params_dict[key] = value
    return params_dict
