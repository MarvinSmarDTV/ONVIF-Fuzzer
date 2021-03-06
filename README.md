# ONVIF Fuzzer

*Python 3.6.5*

## Requirements

- requests >= 2.18.4

## Description

This tool is for fuzz parameters of ONVIF messages (IP cameras are targeted right now).

## Usage

```
Fuzzer.py <template file> <ip address> [-p <port>] <service url> <user> <password> <known payloads file> <payload count>
```
- Template files are included in *commands_templates* directory (these files must be populated with default values with the *populate.py* tool)
- \<ip address> is the address of an IP camera
- You can specify a custom destination port with *-p* option
- The *service url* is the url that handle the ONVIF service (like "/onvif/device_service")
- You must specify *user* and *password* for authenticate requests (for now, only HTTP Digest is currently in use)
- You can specify a custom known attacks list file in the last argument (a default one is provided with this tool)
- You can choose how many **random** payloads are generated per parameter

### Default parameters value in template files (*populate.py* tool)

You must specify default parameters value to use in template files by replacing the '?' by its default value.

The *populate.py* tool was made for that:

```
populate.py <ODTT results file> <templates directory> <output directory>
```
- ODTT (ONVIF Device Test Tool) results file that contains requests with parameters
- Directory that contains template files (commands_templates for example)
- The output directory that will contains populated template files (existing or not)

> So, to fuzz a camera you must run a test suite from ONVIF Device Test Tool 17.12, then run the *populate.py* tool and finally, run the fuzzer.

## TODO

- Improve command line arguments handling with argparse for example to add features
- Add a better *analyse_response()* function
- In ONVIFMessage, use SoapUI comments to add or delete optional XML nodes
