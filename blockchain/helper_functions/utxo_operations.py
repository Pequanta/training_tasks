from models import UTXO, UTXOSet
from uuid import UUID
from typing import List
class UTXO_Operation:
    def __init__(self):
        self.utxos = UTXOSet
        self.last_utxo = None
    def add_utxo(self, utxo: UTXO) -> None:
            """Add a new UTXO to the set."""
            self.utxos.append(utxo)

    def get_balance(self, address: str) -> int:
        """
        Calculate the total balance for a given address.

        Args:
            address (str): Address to calculate the balance for.

        Returns:
            int: Total balance in satoshis (or smallest unit).
        """
        return sum(utxo.value for utxo in self.utxos if utxo.address == address and not utxo.spent)

    def get_utxos_by_address(self, address: str) -> List[UTXO]:
        """
        Retrieve all UTXOs for a given address.

        Args:
            address (str): Address to find UTXOs for.

        Returns:
            List[UTXO]: List of UTXOs associated with the address.
        """
        return [utxo for utxo in self.utxos if utxo.address == address and not utxo.spent]