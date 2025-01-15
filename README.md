# Abuse-WriteOwner

## Overview

**Abuse-WriteOwner** is a Python script designed to automate the exploitation of the `WriteOwner` permission in Active Directory (AD) objects. This tool allows security professionals to:

1. Take ownership of an AD object.
2. Assign themselves `GenericAll` permissions on the object.
3. Reset the object's password.
4. Optionally clean up changes by removing `GenericAll` permissions.

This tool is intended for **authorized penetration testing and red team operations** only. Unauthorized use is illegal.

---

## Features

- Automates privilege escalation using `WriteOwner` in AD.
- Uses Impacket tools to modify ownership and permissions.
- Integrates the `net` command for password changes.
- Provides optional cleanup functionality.

---

## Requirements

### Tools

- **Impacket**: Ensure the `owneredit.py` and `dacledit.py` scripts from Impacket are in the working directory.
   - https://github.com/fortra/impacket/blob/master/examples/owneredit.py
   - https://github.com/fortra/impacket/blob/master/examples/dacledit.py    
- **`net`**** Command**: Pre-installed on systems like Kali Linux, accessible via PATH.

### Environment

- Python 3.6 or higher.
- Operating system: Kali Linux or similar security-focused distributions.

### Permissions

- Attacker account must have `WriteOwner` permissions on the target AD object.

---

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/WriteOwner-Abuse.git
   cd WriteOwner-Abuse
   ```

2. Install Impacket if not already installed:

   ```bash
   pip install impacket
   ```

3. Ensure `owneredit.py` and `dacledit.py` are in the script's directory.

---

## Usage

### Command Syntax

```bash
python writeowner_abuse.py \
  --domain <domain_name> \
  --attacker-user <attacker_username> \
  --attacker-password <attacker_password> \
  --victim-user <victim_username> \
  --domain-controller <domain_controller_fqdn> \
  --new-password <new_password>
```

### Example

```bash
python writeowner_abuse.py \
  --domain example.local \
  --attacker-user attacker1 \
  --attacker-password AttackerPass123 \
  --victim-user victim1 \
  --domain-controller dc.example.local \
  --new-password NewP@ssword123
```

### Cleanup

When prompted, you can choose to remove the added `GenericAll` permissions:

```bash
[?] Do you want to remove the added permissions? (yes/no): yes
```

---

## Legal Disclaimer

This tool is for educational purposes and authorized security assessments only. Unauthorized use of this tool against systems without explicit permission is illegal and unethical.

---

