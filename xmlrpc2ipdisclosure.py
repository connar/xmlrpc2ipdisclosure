from googlesearch import search
import requests
from tabulate import tabulate
import time
import sys
import warnings

warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

def help():
    print("This script dorks for WordPress websites exposing xmlrpc.php and checks if 'pingback.ping' is enabled.\nFull methodology at: https://www.invicti.com/blog/web-security/xml-rpc-protocol-ip-disclosure-attacks/\n")
    print("Usage: python find_xmlrpc_pingback.py [number_of_domains_to_be_found]\n")

def is_pingback_enabled(response_text):
    # Can be customized for any other method
    return "pingback.ping" in response_text

def build_xml_payload():
    return '''<?xml version="1.0" encoding="UTF-8"?>
<methodCall>
<methodName>system.listMethods</methodName>
<params></params>
</methodCall>'''

def main():
    if len(sys.argv) < 2:
        help()
        sys.exit(1)

    help()
    num_results = int(sys.argv[1])

    # From https://www.exploit-db.com/ghdb/4678
    query = 'inurl:"/xmlrpc.php?rsd" ext:php'
    found_urls = []

    print("\n[*] Searching for WordPress sites with xmlrpc.php exposed...\n")

    try:
        results = search(query, sleep_interval=0.2, num_results=num_results)
        for url in results:
            if 'xmlrpc.php' in url:
                clean_url = url.split('?')[0]
                found_urls.append(clean_url)
    except Exception as e:
        print(f"[!] Error during Google search: {e}")
        sys.exit(1)

    table_data = []
    headers = ["Website", "Pingback Enabled"]

    print(f"[*] Scanning {len(found_urls)} endpoints...\n")

    for url in found_urls:
        try:
            headers_req = {'Content-Type': 'application/xml'}
            resp = requests.post(url, data=build_xml_payload(), headers=headers_req, timeout=10, verify=False)
            time.sleep(0.5)
            pingback = "Yes" if is_pingback_enabled(resp.text) else "No"
            table_data.append([url, pingback])
        except Exception:
            table_data.append([url, "Error"])

    print(tabulate(table_data, headers=headers, tablefmt="grid", stralign="center"))

if __name__ == "__main__":
    main()
