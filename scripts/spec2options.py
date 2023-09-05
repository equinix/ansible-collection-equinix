#!/usr/bin/env python3

# TODO: 
# - elements to fields of type list
# - string->str, integer->int, boolean->bool, number->float
# - line lenngth max 160
# - quote strings with special chars

import re
import sys
import yaml

_RE_COMBINE_WHITESPACE = re.compile(r"\s+")

# regexp for combining empty lines and space into one new line
_RE_COMBINE_EMPTY_LINES1 = re.compile(r"(\S)\n(\S)")


SPEC = ""
MODEL = ""


def fix_desc(s, k):
    if k == "always_pxe":
        return [_RE_COMBINE_WHITESPACE.sub(" ", s)]
    if k == "features":
        s = s.replace("```", "`")
    s = _RE_COMBINE_EMPTY_LINES1.sub(r'\1 \2', s)
    ls = s.split("\n\n")
    return [i.strip() for i in ls]


def fix_type(t):
    if t == 'array':
        return 'list'
    if t == 'object':
        return 'dict'
    if t == 'boolean':
        return 'bool'
    if t == 'date-time':
        return 'str'
    return t


backupDescModel = {
    "DeviceUpdateInput": "DeviceCreateInput",
}

missing_desc = {
    "termination_time": "The time at which the device will be terminated.",
    "href": "The URL of the resource.",
}


def getBackupDesc(k):
    if MODEL in backupDescModel:
        backupModel = backupDescModel[MODEL]
        backupSpec = SPEC['components']['schemas'][backupModel]
        if k in backupSpec['properties']:
            return backupSpec['properties'][k]['description']
    return None


def to_optblock_dict(k, d):
    if 'description' not in d:
        d['description'] = getBackupDesc(k)
        if d['description'] is None:
            d['description'] = missing_desc[k]

    desc = fix_desc(d['description'], k)
    return dict(
        name=k,
        type=fix_type(d['type']),
        description=desc,
        choices=d.get('enum', None),
        required=d.get('required', False),
        default=d.get('default', None),
    )


def print_optblock(k, d):
    ob = to_optblock_dict(k, d)
    print(f"    {k}:")
    print(f"        type: {ob['type']}")
    print(f"        description:")
    for l in ob['description']:
        print(f"            - {l}")
    if ob['choices']:
        print(f"        choices:")
        for c in ob['choices']:
            print(f"        - {c}")
    if ob['required']:
        print(f"        required: {ob['required']}")
    if ob['default']:
        print(f"        default: {ob['default']}")


skip = ['id', 'tags', 'href']


def main():
    global SPEC
    global MODEL
    specfilename = sys.argv[1]
    MODEL = sys.argv[2]
    with open(specfilename) as specfile:
        SPEC = yaml.safe_load(specfile)
    dci = SPEC['components']['schemas'][MODEL]
    for p in dci['properties']:
        if p in skip:
            continue
        print_optblock(p, dci['properties'][p])
        print()


if __name__ == '__main__':
    main()
