# DynDNS Client IsFree.top
DynDNS IsFree.top is a free DynDNS client that automatically updates your dynamic domain name on the dns.isfree.top platform.

It offers a simple, secure, and commitment-free solution to host your own DynDNS service on an open infrastructure.

## Main Features:
- Free and ad-free: No subscription required, no tracking involved.
- Easy to configure: Just enter your email address and the DynDNS tokens you want to update.
- Secure: Authentication is done using unique tokens—no passwords needed.
- Cross-platform: A single lightweight Python script works on both Windows and Linux.

## Download Client Windows 

<!-- BEGIN LATEST DOWNLOAD BUTTON -->
[![Download Windows](https://custom-icon-badges.demolab.com/badge/-Download-blue?style=for-the-badge&logo=download&logoColor=white "Download Windows")](https://raw.githubusercontent.com/isfreetop/dns/refs/heads/main/dyndns-client/windows/windows-dnsisfree.top.zip)
<!-- END LATEST DOWNLOAD BUTTON -->

## Donwload Client Linux

<!-- BEGIN LATEST DOWNLOAD BUTTON -->
[![Download Windows](https://custom-icon-badges.demolab.com/badge/-Download-blue?style=for-the-badge&logo=download&logoColor=white "Download Linux")](https://raw.githubusercontent.com/isfreetop/dns/refs/heads/main/dyndns-client/linux/linux-dnsisfree.top.zip)
<!-- END LATEST DOWNLOAD BUTTON -->

## Donwload Client CLI Synologie/Linux

<!-- BEGIN LATEST DOWNLOAD BUTTON -->
[![Download Windows](https://custom-icon-badges.demolab.com/badge/-Download-blue?style=for-the-badge&logo=download&logoColor=white "Download Linux")](https://raw.githubusercontent.com/isfreetop/dns/refs/heads/main/dyndns-client/sources/dnsisfree.top.cli.py)
<!-- END LATEST DOWNLOAD BUTTON -->


## Configuration

![Screen Install ](/screen/screen1.png)

### Retrieve the token for your record from the dns.isfree.top website.

![Screen Install ](/screen/screen2.png)

![Screen Install ](/screen/screen3.png)


### In the client configuration, enter your email address and token.

![Screen Install ](/screen/screen4.png)

![Screen Install ](/screen/screen5.png)

### The DNS update occurs every 10 minutes.

## Configure CLI for Synologie 

Go to DSM > Control Panel > Task Scheduler.

Create a new task > Scheduled task > User-defined script.

Command: /usr/bin/python3 /volume1/homes/admin/dnsisfree.top.cli.py

## DNS Free Is Top
https://dns.isfree.top