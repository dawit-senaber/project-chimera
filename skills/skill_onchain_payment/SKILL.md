# Skill: On-Chain Payment
**Description**: Interface for processing cryptocurrency transactions for ad placements or influencer rewards.
**Input Contract**:
- `amount` (float): Value to send.
- `recipient_wallet` (string): The target Ethereum/Solana address.
**Output Contract**:
- `tx_hash` (string): The blockchain transaction identifier.
- `status` (string): Confirmation status (pending/success).