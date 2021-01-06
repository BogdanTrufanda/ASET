import pprint
import nmap3


def nmap_scan(target: str):
    print (f"Starting service scan on target {target}")
    nmap = nmap3.Nmap()
    results = nmap.scan_top_ports(target)
    pprint.pprint(results)


