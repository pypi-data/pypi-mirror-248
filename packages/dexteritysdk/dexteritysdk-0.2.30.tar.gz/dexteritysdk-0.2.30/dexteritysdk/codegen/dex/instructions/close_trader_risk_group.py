# LOCK-BEGIN[imports]: DON'T MODIFY
from .instruction_tag import InstructionTag
from dataclasses import dataclass
from dexteritysdk.solmate.utils import to_account_meta
from io import BytesIO
from podite import BYTES_CATALOG
from solders.instruction import (
    AccountMeta,
    Instruction,
)
from solders.pubkey import Pubkey
from typing import (
    List,
    Optional,
    Union,
)

# LOCK-END


# LOCK-BEGIN[ix_cls(close_trader_risk_group)]: DON'T MODIFY
@dataclass
class CloseTraderRiskGroupIx:
    program_id: Pubkey

    # account metas
    owner: AccountMeta
    trader_risk_group: AccountMeta
    market_product_group: AccountMeta
    receiver: AccountMeta
    remaining_accounts: Optional[List[AccountMeta]]

    def to_instruction(self):
        keys = []
        keys.append(self.owner)
        keys.append(self.trader_risk_group)
        keys.append(self.market_product_group)
        keys.append(self.receiver)
        if self.remaining_accounts is not None:
            keys.extend(self.remaining_accounts)

        buffer = BytesIO()
        buffer.write(InstructionTag.to_bytes(InstructionTag.CLOSE_TRADER_RISK_GROUP))

        return Instruction(
            accounts=keys,
            program_id=self.program_id,
            data=buffer.getvalue(),
        )

# LOCK-END


# LOCK-BEGIN[ix_fn(close_trader_risk_group)]: DON'T MODIFY
def close_trader_risk_group(
    owner: Union[str, Pubkey, AccountMeta],
    trader_risk_group: Union[str, Pubkey, AccountMeta],
    market_product_group: Union[str, Pubkey, AccountMeta],
    receiver: Union[str, Pubkey, AccountMeta],
    remaining_accounts: Optional[List[AccountMeta]] = None,
    program_id: Optional[Pubkey] = None,
):
    if program_id is None:
        program_id = Pubkey.from_string("FUfpR31LmcP1VSbz5zDaM7nxnH55iBHkpwusgrnhaFjL")

    if isinstance(owner, (str, Pubkey)):
        owner = to_account_meta(
            owner,
            is_signer=True,
            is_writable=True,
        )
    if isinstance(trader_risk_group, (str, Pubkey)):
        trader_risk_group = to_account_meta(
            trader_risk_group,
            is_signer=False,
            is_writable=True,
        )
    if isinstance(market_product_group, (str, Pubkey)):
        market_product_group = to_account_meta(
            market_product_group,
            is_signer=False,
            is_writable=False,
        )
    if isinstance(receiver, (str, Pubkey)):
        receiver = to_account_meta(
            receiver,
            is_signer=False,
            is_writable=True,
        )

    return CloseTraderRiskGroupIx(
        program_id=program_id,
        owner=owner,
        trader_risk_group=trader_risk_group,
        market_product_group=market_product_group,
        receiver=receiver,
        remaining_accounts=remaining_accounts,
    ).to_instruction()

# LOCK-END
