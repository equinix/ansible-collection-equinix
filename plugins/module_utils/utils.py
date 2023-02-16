#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

def dict_get(d, key):
    """
    Get a value from a nested dict using a dot-separated key.
    """
    import q; q(d, key)
    for k in key.split("."):
        if k in d:
            d = d[k]
            if isinstance(d, dict):
                continue
            return d
        else:
            return None
    return d
