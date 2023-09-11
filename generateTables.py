#!/bin/python
import json

metersPerFoot = 0.3048
feetPerMeter = 1 / metersPerFoot
feetPerMile = 5280.0
metersPerMile = metersPerFoot * feetPerMile
milesPerFoot = 1 / feetPerMile
milesPerMeter = milesPerFoot * feetPerMeter
metersPerKilometer = 1000.0
kilometersPerMeter = 1/metersPerKilometer
kilometersPerFoot = kilometersPerMeter * metersPerFoot
kilometersPerMile = kilometersPerMeter * metersPerMile
milesPerKilometer = 1 / kilometersPerMile
feetPerKilometer = 1 / kilometersPerFoot

caves = json.load(open("caves.json"))

template = ""
with open('template.html') as f: template = f.read()

def valueInMeters(val):
    if 'number' in val:
        number = val['number']
        if 'units' in val:
            units = val['units']
            match units:
                case 'meters':
                    return number
                case 'feet':
                    return number * metersPerFoot
                case 'miles':
                    return number * metersPerMile
                case 'kilometers':
                    return number * metersPerKilometer
                case _:
                    return -1
        else:
            return -1
    else:
        return -1

def valueInFeet(val):
    if 'number' in val:
        number = val['number']
        if 'units' in val:
            units = val['units']
            match units:
                case 'meters':
                    return number * feetPerMeter
                case 'feet':
                    return number
                case 'miles':
                    return number * feetPerMile
                case 'kilometers':
                    return number * feetPerKilometer
                case _:
                    return -1
        else:
            return -1
    else:
        return -1

def valueInKilometers(val):
    if 'number' in val:
        number = val['number']
        if 'units' in val:
            units = val['units']
            match units:
                case 'meters':
                    return number * kilometersPerMeter
                case 'feet':
                    return number * kilometersPerFoot
                case 'miles':
                    return number * kilometersPerMile
                case 'kilometers':
                    return number
                case _:
                    return -1
        else:
            return -1
    else:
        return -1

def valueInMiles(val):
    if 'number' in val:
        number = val['number']
        if 'units' in val:
            units = val['units']
            match units:
                case 'meters':
                    return number * milesPerMeter
                case 'feet':
                    return number * milesPerFoot
                case 'miles':
                    return number
                case 'kilometers':
                    return number * milesPerKilometer
                case _:
                    return -1
        else:
            return -1
    else:
        return -1


    if "depth" in cave:
        depth = cave["depth"]
        if type(depth) is int:
            if "depthUnits" in cave:
                units = cave["depthUnits"]
                if units == "meters":
                    return depth
                elif units == "kilometers":
                    return depth * 1000.0
                elif units == "feet":
                    return depth * metersPerFoot
                elif units == "miles":
                    return depth * metersPerMile
                else:
                    return -1
        else:
            return -1
    else:
        return -1

# returns a string with <td> cells with the relevant info
# about the cave. Does not include a <tr> outer tag.
def caveToTableCells(cave, country=True, caveType=True):
    row = ''
    if caveType:
        row += f'<td>{cave.get("type", "")}</td>'
    row += f'<td>{cave["name"]}</td>'
    row += f'<td>{valueInKilometers(cave["length"]): .3f}</td>'
    row += f'<td>{valueInMiles(cave["length"]): .3f}</td>'
    row += f'<td>{valueInMeters(cave["depth"]): .3f}</td>'
    row += f'<td>{valueInFeet(cave["depth"]): .3f}</td>'
    if country:
        row += f'<td>{cave["country"]}</td>'
    row += f'<td>{cave["state/province"]}</td>'
    row += f'<td>{cave.get("county", "")}</td>'
    row += f'<td>{cave.get("source", "")}</td>'
    row += f'<td>{cave.get("dateUpdated", "")}</td>'

    return row

# first handle usa caves
usaCaves = []
usaCavesSolutional = []
for cave in caves:
    if 'country' in cave and cave['country'] == 'United States of America':
        usaCaves.append(cave)
        if 'type' in cave and cave['type'] == 'solutional':
            usaCavesSolutional.append(cave)

# USA long caves, incl non solutional
usaCaves.sort(key=lambda cave : valueInMeters(cave['length']), reverse=True)
usaLongCavesTableHtml = """<tr>
            <th>rank</th>
            <th>type</th>
            <th>name</th>
            <th>length (kilometers)</th>
            <th>length (miles)</th>
            <th>depth (meters)</th>
            <th>depth (feet)</th>
            <th>state/province</th>
            <th>county</th>
            <th>source</th>
            <th>date</th>
        </tr>
"""
for i, cave in enumerate(usaCaves):
    usaLongCavesTableHtml += f'<tr><td>{i+1}</td>' + caveToTableCells(cave, country=False, caveType=True) + '</tr>\n'
usaLongCavesHtml = template.replace('TITLE', 'USA long caves, including non-solutional').replace('TABLEROWS', usaLongCavesTableHtml)

with open('usaLongInclNonSolutional.html', 'w') as f:
    f.write(usaLongCavesHtml)

# USA long caves, solutional only
usaCavesSolutional.sort(key=lambda cave : valueInMeters(cave['length']), reverse=True)
usaLongCavesSolutionalTableHtml = """<tr>
            <th>rank</th>
            <th>name</th>
            <th>length (kilometers)</th>
            <th>length (miles)</th>
            <th>depth (meters)</th>
            <th>depth (feet)</th>
            <th>state/province</th>
            <th>county</th>
            <th>source</th>
            <th>date</th>
        </tr>
"""
for i, cave in enumerate(usaCavesSolutional):
    usaLongCavesSolutionalTableHtml += f'<tr><td>{i+1}</td>' + caveToTableCells(cave, country=False, caveType=False) + '</tr>\n'
usaLongCavesSolutionalHtml = template.replace('TITLE', 'USA long caves, solutional only').replace('TABLEROWS', usaLongCavesSolutionalTableHtml)

with open('usaLongInclSolutional.html', 'w') as f:
    f.write(usaLongCavesSolutionalHtml)


# generate deep caves of USA, incl non solutional