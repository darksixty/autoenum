import subprocess
import os
import getpass
import sys

def execute_in_terminal(command):
    subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{command}; exec bash"])

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Please run this script with 'sudo'.")
        sys.exit(1)

    targetip = input("Enter Target IP address: ")

    # Get the sudo password from the user without displaying it in clear text
    sudopassword = getpass.getpass("Enter your sudo password: ")

    print(targetip + " has been selected")
    print("Starting enumeration")

    # Set the full file path for Gobuster's output
    savepath = "/home/kali/HackTheBox/"  # Update this with your desired save path
    gofilename = "gobuster_output.txt"  # Update this with your desired filename
    filepath = os.path.join(savepath, gofilename)

    # Execute Nmap with the sudo password provided
    nmap_command = f"echo '{sudopassword}' | sudo -S nmap -T4 -A -sV -Pn {targetip}"
    execute_in_terminal(nmap_command)

    # Execute Gobuster in a separate terminal window
    gobuster_command = f"gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -o {filepath} -u {targetip}"
    execute_in_terminal(gobuster_command)

    # Execute Nikto in a separate terminal window
    nikto_command = f"nikto -h {targetip}"
    execute_in_terminal(nikto_command)

    print("Enumeration started in separate terminal windows.")
