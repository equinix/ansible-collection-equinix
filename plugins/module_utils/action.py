#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import enum

class Action(enum.Enum):
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
    GET = 'get'
    LIST = 'list'

CREATE = Action.CREATE
UPDATE = Action.UPDATE
DELETE = Action.DELETE
GET = Action.GET
LIST = Action.LIST