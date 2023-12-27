""" This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Created on Dec 22, 2023

@author: pymancer@gmail.com (polyanalitika.ru)
"""

from enum import Enum, EnumMeta


def dict_to_enumdef(name: str, enum_dict: dict, cls: EnumMeta = Enum) -> EnumMeta:
    return cls(name, enum_dict)
