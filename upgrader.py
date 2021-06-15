#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json

latestVersion = '1.3.0'
errors = 0


def upgradeFile(path):
    with open(path, 'r+', encoding='utf8') as f:
        global errors
        level = json.loads(f.read())
        firstKey = list(level.keys())[0]
        name = os.path.splitext(os.path.basename(path))[0]
        if (firstKey[:6] == 'CHKSUM'):
            level = level[firstKey]
            if (level['softwaredata']['version'] == latestVersion):
                print('{:<9s}{:<25s}{:0<13s}'.format(
                    'Level:', name, ''))
                return
        else:
            if 'softwaredata' in level:
                if (int(level['softwaredata']['version'].replace('.', '')) < 51):
                    print('{:<9s}{:<25s}{:<13s}'.format(
                        'Level: ', name, '- old version'))
                    errors += 1
                    return
            else:
                print('{:<9s}{:<25s}{:<13s}'.format(
                    'Level: ', name, '- no version'))
                errors += 1
                return
        newLevel = upgradeLevel(level['softwaredata']['version'], level)
        f.seek(0)
        f.truncate()
        f.write(newLevel)
    print('{:<9s}{:<25s}{:1<13s}'.format(
        'Level:', name, ''))


def upgradeLevel(version, level):
    if (version == '0.5.1'):
        version = '0.6.0'
        level['projectdata']['monitors'] = []
        level['projectdata']['settings'] = {
            'centerAsOrigin': True
        }
    if (version == '0.6.0'):
        version = '0.6.1'
        level['projectdata']['title'] = 'Level'
    if (version == '0.6.1'):
        version = '0.7.0'
        level['projectdata']['settings']['selectedWorkspaceID'] = 0
        for costume in level['projectdata']['background']['costumes']:
            costume['isSystemCostume'] = False
        for ws in level['projectdata']['workspaces']:
            for costume in ws['sprite']['costumes']:
                costume['isSystemCostume'] = False
    if (version == '0.7.0'):
        version = '0.7.1'
        level['projectdata']['background']['orientation'] = 0
        level['projectdata']['background']['mirrored'] = False
        for ws in level['projectdata']['workspaces']:
            ws['sprite']['orientation'] = 0
            ws['sprite']['mirrored'] = False
    if (version == '0.7.1'):
        version = '1.0.0'
    if (version == '1.0.0'):
        version = '1.0.1'
        for ws in level['projectdata']['workspaces']:
            ws['sprite']['startConfiguration'] = {
                'position': {
                    'x': ws['sprite']['position']['x'],
                    'y': ws['sprite']['position']['y'],
                },
                'rotation': ws['sprite']['rotation'],
                'scale': ws['sprite']['scale'],
                'mirrored': ws['sprite']['mirrored'],
                'orientation': ws['sprite']['orientation'],
                'visible': ws['sprite']['visible']
            }
    if (version == '1.0.1'):
        version = '1.3.0'
        for ws in level['projectdata']['workspaces']:
            ws['sprite']['mobileOnly'] = False
            ws['sprite']['isInput'] = False
            ws['sprite']['layer'] = 1
            ws['sprite']['startConfiguration']['layer'] = -1
    level['softwaredata']['version'] = version
    data = json.dumps(level, separators=(',', ':'), ensure_ascii=False)
    hash = generateHash(data)
    return '{"CHKSUM>#' + hash + '#":' + data + '}'


def generateHash(input):
    fnvPrime = 0x01000193
    hashFwd = 0x811c9dc5
    hashBwd = 0x811c9dc5
    iFwd = 0
    iBwd = len(input) - 1
    intMax = 2 ** 32

    while (iFwd <= len(input) - 1 and iBwd >= 0):
        hashFwd ^= ord(input[iFwd])
        hashFwd = (hashFwd * fnvPrime) % intMax
        hashBwd ^= ord(input[iBwd])
        hashBwd = (hashBwd * fnvPrime) % intMax
        iFwd += 1
        iBwd -= 1
    return '{:08x}'.format(hashFwd) + '{:08x}'.format(hashBwd)


print('{:≡^47}'.format('SOLUTIONS'))
for file in os.listdir('./Solutions'):
    upgradeFile('./Solutions/' + file)
print('{:≡^47}'.format('TEMPLATES'))
for file in os.listdir('./Templates'):
    upgradeFile('./Templates/' + file)
if (errors > 0):
    print('{:≡^47}'.format('ERRORS'))
    print(str(errors) + ' files were unsuccessful!')
