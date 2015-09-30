import pdb, os
import subprocess
import re
from subprocess import Popen, PIPE

# This will only work within the netmask of the machine the program is running on cross router MACs will be lost
ip ="10.11.12.95"

#PING to place target into system's ARP cache 
process = subprocess.Popen(["ping", "-c","4", ip], stdout=subprocess.PIPE)
process.wait()

result = process.stdout.read()
print(result)

#MAC address from IP
pid = Popen(["arp", "-n", ip], stdout=PIPE)
s = pid.communicate()[0]

# [a-fA-F0-9] = find any character A-F, upper and lower case, as well as any number
# [a-fA-F0-9]{2} = find that twice in a row
# [a-fA-F0-9]{2}[:|\-] = followed by either a ?:? or a ?-? character (the backslash escapes the hyphen, since the  # hyphen itself is a valid metacharacter for that type of expression; this tells the regex to look for the hyphen character, and ignore its role as an operator in this piece of the expression)
# [a-fA-F0-9]{2}[:|\-]? = make that final ?:? or ?-? character optional; since the last pair of characters won't be followed by anything, and we want them to be included, too; that's a chunk of 2 or 3 characters, so far
# ([a-fA-F0-9]{2}[:|\-]?){6} = find this type of chunk 6 times in a row

mac = re.search(r"([a-fA-F0-9]{2}[:|\-]?){6}", s).groups()[0] #LINUX VERSION ARP
mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0] #MAC VERSION ARP
print(mac)

