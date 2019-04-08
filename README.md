# HIBP-Validator
Have I Been Pwned (HIBP) Email Validator
## Help
```
$ python hibp-validator.py hh
usage: hibp-validator.py [-h] -t TARGETS [-o CSV] [-v] [-vv] [-d DELAY]
                         [-j JITTER] [-i INDEX]

Work in progress...

optional arguments:
  -h, --help            show this help message and exit
  -t TARGETS, --targets TARGETS
                        File to read or target address. Includes @domain.com
  -o CSV, --csv CSV     File to write
  -v, --verbose         Verbose output
  -vv, --debug          Less tool output, only shows good/bad/info error
                        messages.
  -d DELAY, --delay DELAY
                        The delay between attempts (default 3000ms)
  -j JITTER, --jitter JITTER
                        The delay jitter between attempts. Multiplied by sleep
                        delay (default 0.2)
  -i INDEX, --index INDEX
                        Start from this count (index). Good for fast-
                        forwarding through a file
```
## Example
Use -t to test for a single username or give it a list of users in a file (include the domain as well).
```
$ python hibp-validator.py -t sammbertram@gmail.com 

╦ ╦╦╔╗ ╔═╗  ╦  ╦┌─┐┬  ┬┌┬┐┌─┐┌┬┐┌─┐┬─┐
╠═╣║╠╩╗╠═╝  ╚╗╔╝├─┤│  │ ││├─┤ │ │ │├┬┘
╩ ╩╩╚═╝╩     ╚╝ ┴ ┴┴─┘┴─┴┘┴ ┴ ┴ └─┘┴└─
                                                 version: 0.1
                     

[*] 2019-04-08 12:35:54
[*] Testing single account (sammbertram@gmail.com)
[*] 2019-04-08 12:35:57
[*] done
```
Read the CSV file
```
$ cat output_hibp.csv 
2019-04-08 12:35:54:264069,sammbertram@gmail.com,PayAsUGym;Onliner Spambot;B2B USA Businesses;Bitly;LinkedIn;MyFitnessPal;Verifications.io;Bitcoin Security Forum Gmail Dump;Whitepages;Linux Forums;Ticketfly
```
