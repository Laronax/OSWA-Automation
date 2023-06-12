import os
import sys
import subprocess
import concurrent.futures

MAXTHREAD=2
def run_command(command):
    process = subprocess.Popen(command, shell=True)
    process.communicate()
    return process.returncode

def run_commands_parallel(commands, max_threads):
    return_codes = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_command = {executor.submit(run_command, command): command for command in commands}
        for future in concurrent.futures.as_completed(future_to_command):
            command = future_to_command[future]
            try:
                return_code = future.result()
                return_codes.append(return_code)
                print(f"Command '{command}' returned code: {return_code}")
            except Exception as e:
                print(f"Command '{command}' raised an exception: {e}")

    return return_codes

def create_folders(filenames):
    print(filenames)
    for fname in filenames:
        folder_name = fname.strip()
        os.makedirs(folder_name, exist_ok=True)
        print(f"Created folder: {folder_name}")
    print("Folder creation completed.")

if __name__ == '__main__':
    # Check if the file path argument is provided
    if len(sys.argv) < 2:
        print("Please provide the file path as a command-line argument.")
        sys.exit(1)
    file_path = sys.argv[1]
    file=open(file_path, 'r')
    lines = file.readlines()	
    file.close()
    create_folders(lines)
    commands=[]
    #Add nmap commands
    for line in lines:
        tline=line.strip()
        commands.append(f"nmap -A {tline} -Pn -oN ./{tline}/nmapout	")
    # Run the commands in parallel
    
    for line in lines:
        tline="http://"+line.strip()+"/"
        commands.append(f"wfuzz -c -z file,/usr/share/seclists/Discovery/Web-Content/raft-medium-files.txt --hc 404 {tline}|tee ./line/wfuzzfilediscovery")
        tline=tline+"/"
        commands.append(f"wfuzz -c -z file,/usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt --hc 404 {tline}./line/wfuzzfolder	discovery")

    # Print the return codes of each command
    return_codes = run_commands_parallel(commands,MAXTHREAD)
    for i, return_code in enumerate(return_codes):
        print(f"Command {i+1} returned code: {return_code}")
