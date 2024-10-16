#!/usr/bin/env python3
import read_disks_serials  # Import the other script
import json

# Call a function from read_disk_serials (assuming it has one)

file = open('output.txt', 'w')
file.write(json.dumps(read_disks_serials.read_dump('images/','unreadable/')))