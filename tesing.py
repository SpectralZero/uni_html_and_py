"""
Python examples 
for reading and writing .txt, .csv, .xml, and .json files

Created on: 2025-11-08
By: Jamal Alqbail
Id: 3200606025
"""
import csv
import json
import xml.etree.ElementTree as ET

"""
Note: i have used with statement to handle file operations,
it closes the file automatically after the block is executed. 
Much easier :))
"""


# -------- TXT File Example --------
print("----- TXT File Example (Writing) -----")
# Write to TXT file
with open("example.txt", "w") as f:
    f.write("Hello, world!\nThis is a text file.")

print("\n----- TXT File Example (Reading) -----")
# Read from TXT file
with open("example.txt", "r") as f:
    content = f.read()
    print(content)


# -------- CSV File Example --------
print("\n----- CSV File Example (Writing) -----")
# Write to CSV file
with open("example.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Age", "ID"])
    writer.writerow(["Fadi", 23, "3110606025"])
    writer.writerow(["Khalid", 25, "3321606026"])

print("\n----- CSV File Example (Reading) -----")
# Read from CSV file
with open("example.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)


# -------- JSON File Example --------
data = {"name": "Jamal", "age": 24, "skills": ["Python", "Security"]}
print("\n----- JSON File Example (Writing) -----")
# Write to JSON file
with open("example.json", "w") as f:
    json.dump(data, f, indent=2)

print("\n----- JSON File Example (Reading) -----")
# Read from JSON file
with open("example.json", "r") as f:
    loaded = json.load(f)
    print(loaded)


# -------- XML File Example --------
print("\n----- XML File Example (Writing) -----")
# Write XML file
root = ET.Element("person")
ET.SubElement(root, "name").text = "Jamal"
ET.SubElement(root, "age").text = "24"
tree = ET.ElementTree(root)
tree.write("example.xml")

print("\n----- XML File Example (Reading) -----")
# Read XML file
tree = ET.parse("example.xml")
root = tree.getroot()
for child in root:
    print(child.tag, ":", child.text)
