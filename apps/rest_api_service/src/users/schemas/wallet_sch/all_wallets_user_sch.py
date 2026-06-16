from pydantic import BaseModel

class AllWalletUser(BaseModel):
    title: str
    wallet_address: str
    #balance_eth: str
    model_config = {"from_attributes": True}


class AllWalletsResponse(BaseModel):
    items: list[AllWalletUser]
    model_config = {"from_attributes": True}