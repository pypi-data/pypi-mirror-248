class GetHdWalletAddressParam:
    def __init__(self):
        self.hd_wallet_id = None


class GetBalanceParam:
    def __init__(self):
        self.chain_name = None
        self.currency = None
        self.hd_wallet_id = None
        self.page = None
        self.limit = None


class TokenDataParam:
    def __init__(self):
        self.address = None
        self.symbol = None
        self.decimals = None


class AddCustomTokenParam:
    def __init__(self):
        self.chain_name = None
        self.hd_wallet_id = None
        self.sync_wallets = None
        self.token_data = None  # type is TokenDataParam


class GetTransactionHistroyParam:
    def __init__(self):
        self.chain_name = None
        self.page = None
        self.limit = None
        self.order_by = None
        self.asc = None
        self.hd_wallet_id = None


class GetApprovalsParam:
    def __init__(self):
        self.page = None
        self.limit = None
        self.status = None


class AgreeApprovalParam:
    def __init__(self):
        self.record_id = None
        self.agree = None


class DappInfo:
    def __init__(self):
        self.origin = None,
        self.href = None,
        self.portName = None,
        self.icon = None,
        self.dappName = None,


class TxInfoParam:
    def __init__(self):
        self.transaction_type = None
        self.chain = None
        self.fromAddress = None  # api doc txinfo param from
        self.to = None
        self.tokenAddress = None
        self.value = None
        self.nonce = None
        self.gasLimit = None
        self.gasPrice = None
        self.maxPriorityFeePerGas = None
        self.maxFeePerGas = None
        self.data = None
        self.pretreatment_value = None
        self.token_id = None
        self.dappInfo = None
        self.original_record_id = None
        self.operate_type = None


class NewApprovalParam:
    def __init__(self):
        self.action = None
        self.hd_wallet_id = None
        self.txinfo = None  # type is TxInfoParam
