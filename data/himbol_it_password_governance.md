# Himbol Policy: Core Systems Password Governance and Access Control

**Document Reference: POL-IT-PWD14**
**Effective Date: January 1, 2026**

## 1. Complexity Requirements and Expiration Cycles

Access to the Himbol transaction ledger and M-Nakfa backend database demands strict authentication controls. All user passwords must be a minimum of 12 characters, including uppercase letters, lowercase letters, numbers, and special symbols. System access passwords expire automatically every 60 calendar days. The system will reject any new password that matches any of the user's previous 8 historical password iterations.

## 2. Lockout Thresholds and Account Re-Activation

Accounts will experience an automatic administrative lock after 3 consecutive failed login attempts on any terminal. Locked accounts can only be re-activated following verification by the IT Helpdesk based at the Asmara Head Office. IT support technicians are strictly prohibited from issuing temporary credentials via phone conversations without first confirming the employee's unique HR personnel code.
