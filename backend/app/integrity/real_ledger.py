"""Phase 11M — RealLedger production EVM/Sepolia blockchain adapter.

Anchors artifact cryptographic SHA-256 digests onto a public smart contract
via Web3 (Ethereum Sepolia / Polygon).
"""
from __future__ import annotations

import logging
from typing import Any
from datetime import datetime, timezone

from app.core.config import settings
from app.integrity.ledger import IntegrityLedger, IntegrityRecord, LedgerStatus

logger = logging.getLogger(__name__)

REGISTRY_ABI = [
    {
        "inputs": [
            {"internalType": "bytes32", "name": "artifactHash", "type": "bytes32"},
            {"internalType": "bytes32", "name": "provenanceHash", "type": "bytes32"},
        ],
        "name": "recordDigest",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "artifactHash", "type": "bytes32"}],
        "name": "verifyDigest",
        "outputs": [
            {"internalType": "bool", "name": "exists", "type": "bool"},
            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
            {"internalType": "bytes32", "name": "provenanceHash", "type": "bytes32"},
            {"internalType": "address", "name": "recorder", "type": "address"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]


class RealLedger(IntegrityLedger):
    """Production EVM smart contract provenance adapter.

    Connects via Web3 to anchor artifact digests on-chain.
    """

    provider_name = "real"

    def __init__(
        self,
        *,
        ledger_url: str | None = None,
        credential: str | None = None,
        contract_address: str | None = None,
        chain_id: int | None = None,
    ) -> None:
        self._ledger_url = (
            ledger_url
            if ledger_url is not None
            else getattr(settings, "INTEGRITY_LEDGER_URL", "")
        )
        self._credential = (
            credential
            if credential is not None
            else getattr(settings, "INTEGRITY_LEDGER_CREDENTIAL", "")
        )
        self._contract_address = (
            contract_address
            if contract_address is not None
            else getattr(settings, "INTEGRITY_CONTRACT_ADDRESS", "")
        )
        self._chain_id = chain_id or getattr(settings, "INTEGRITY_CHAIN_ID", 11155111)

        # Configured means connection coordinates are declared
        self._configured = bool(self._ledger_url and self._credential)
        self._w3: Any = None
        self._account: Any = None
        self._contract: Any = None

        if self._configured and self._contract_address:
            try:
                from web3 import Web3
                from eth_account import Account

                # Private key formatting (starts with 0x)
                clean_cred = self._credential
                if clean_cred and not clean_cred.startswith("0x") and not clean_cred.startswith("ref:"):
                    clean_cred = "0x" + clean_cred

                if clean_cred and not clean_cred.startswith("ref:"):
                    self._account = Account.from_key(clean_cred)
                self._w3 = Web3(Web3.HTTPProvider(self._ledger_url, request_kwargs={"timeout": 15}))
                checksum_address = Web3.to_checksum_address(self._contract_address)
                self._contract = self._w3.eth.contract(
                    address=checksum_address,
                    abi=REGISTRY_ABI,
                )
            except Exception as exc:
                logger.error("Failed to initialize Web3 RealLedger: %s", exc)

    @property
    def configured(self) -> bool:
        return self._configured

    def _unavailable(self, op: str) -> tuple[bool, IntegrityRecord | None, LedgerStatus]:
        logger.warning("Integrity ledger unavailable for %s (not configured or RPC offline)", op)
        return False, None, LedgerStatus.UNAVAILABLE

    def record_integrity_event(
        self,
        *,
        digest: str,
        algorithm: str,
    ) -> tuple[bool, IntegrityRecord | None, LedgerStatus]:
        if not self._configured or self._contract is None or self._w3 is None:
            return self._unavailable("record")

        try:
            # Clean hex string into 32 bytes
            clean_digest = digest.replace("0x", "")[:64]
            artifact_bytes32 = bytes.fromhex(clean_digest)
            provenance_bytes32 = artifact_bytes32

            # Check if already recorded on-chain
            try:
                exists, timestamp, _, _ = self._contract.functions.verifyDigest(artifact_bytes32).call()
                if exists:
                    record = IntegrityRecord(
                        reference=f"0x{clean_digest[:40]}",
                        digest=digest,
                        algorithm=algorithm,
                        provider=self.provider_name,
                        recorded_at=datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat(),
                    )
                    return True, record, LedgerStatus.RECORDED
            except Exception:
                pass

            # Build and send transaction
            nonce = self._w3.eth.get_transaction_count(self._account.address)
            gas_price = self._w3.eth.gas_price

            tx = self._contract.functions.recordDigest(
                artifact_bytes32,
                provenance_bytes32,
            ).build_transaction({
                "from": self._account.address,
                "nonce": nonce,
                "gas": 150000,
                "gasPrice": gas_price,
                "chainId": self._chain_id,
            })

            signed_tx = self._w3.eth.account.sign_transaction(tx, self._credential)
            tx_raw = getattr(signed_tx, "raw_transaction", None) or getattr(signed_tx, "rawTransaction", None)
            tx_hash = self._w3.eth.send_raw_transaction(tx_raw)
            tx_hex = self._w3.to_hex(tx_hash)

            logger.info("Artifact hash anchored to Ethereum Sepolia blockchain", tx_hash=tx_hex, digest=digest)

            record = IntegrityRecord(
                reference=tx_hex,
                digest=digest,
                algorithm=algorithm,
                provider=self.provider_name,
            )
            return True, record, LedgerStatus.RECORDED
        except Exception as exc:
            logger.error("Blockchain transaction failed: %s", exc)
            return False, None, LedgerStatus.UNAVAILABLE

    def get_integrity_record(
        self,
        *,
        reference: str,
        algorithm: str,
    ) -> IntegrityRecord | None:
        if not self._configured or self._contract is None:
            return None
        return IntegrityRecord(
            reference=reference,
            digest="",
            algorithm=algorithm,
            provider=self.provider_name,
        )

    def verify_integrity(
        self,
        *,
        reference: str,
        digest: str,
        algorithm: str,
    ) -> LedgerStatus:
        if not self._configured or self._contract is None:
            return LedgerStatus.UNAVAILABLE

        try:
            clean_digest = digest.replace("0x", "")[:64]
            artifact_bytes32 = bytes.fromhex(clean_digest)
            exists, timestamp, provenance, recorder = self._contract.functions.verifyDigest(artifact_bytes32).call()
            if exists:
                # Security validation: ensure digest was registered by our authorized relayer address
                if self._account and recorder:
                    if str(recorder).lower() != str(self._account.address).lower():
                        logger.warning(
                            "Provenance recorder mismatch: digest %s recorded by untrusted address %s (expected %s)",
                            digest,
                            recorder,
                            self._account.address,
                        )
                        return LedgerStatus.UNAVAILABLE
                return LedgerStatus.VERIFIED
            return LedgerStatus.NOT_FOUND
        except Exception as exc:
            logger.error("Blockchain verification call failed: %s", exc)
            return LedgerStatus.UNAVAILABLE


__all__ = ["RealLedger"]
