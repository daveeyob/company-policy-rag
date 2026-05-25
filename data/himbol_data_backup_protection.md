# Himbol Policy: Data Backup, Redundancy, and Protection Standards

**Document Reference: POL-IT-BCK18**
**Effective Date: January 1, 2026**

## 1. Core Transaction Database Redundancy Schedule

To prevent transaction history loss for banking ledger rows and M-Nakfa wallet distributions, the IT systems architecture implements a tri-level automated backup loop. Real-time differential log replication executes every 15 minutes from regional nodes to the central vault array at the Asmara Head Office. Complete snapshot system backups are compiled daily at 11:30 PM and written to a secure physical local storage unit.

## 2. Long-Term Archive Retentions and Offline Security

Encrypted weekly database backups must be written to read-only optical storage media and securely transported to a designated off-site safe deposit box in Mendefera every Monday morning. To maximize security and comply with compliance laws, all financial transaction histories, remote client verification records, and AML logs must be retained for a minimum of 7 calendar years before erasure.
