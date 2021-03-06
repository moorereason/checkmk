#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2014             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Filesize,
    Integer,
    TextAscii,
    Tuple,
)

from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)


@rulespec_registry.register
class RulespecCheckgroupParametersDockerNodeDiskUsage(CheckParameterRulespecWithItem):
    @property
    def group(self):
        return RulespecGroupCheckParametersApplications

    @property
    def check_group_name(self):
        return "docker_node_disk_usage"

    @property
    def title(self):
        return _("Docker node disk usage")

    @property
    def match_type(self):
        return "dict"

    @property
    def parameter_valuespec(self):
        return Dictionary(
            help=
            _("Allows to define levels for the counts and size of Docker Containers, Images, Local Volumes, and the Build Cache."
             ),
            elements=[
                ("size",
                 Tuple(
                     title=_("Size"),
                     elements=[
                         Filesize(title=_("Warning at"), allow_empty=False),
                         Filesize(title=_("Critical at"), allow_empty=False),
                     ],
                 )),
                ("reclaimable",
                 Tuple(
                     title=_("Reclaimable"),
                     elements=[
                         Filesize(title=_("Warning at"), allow_empty=False),
                         Filesize(title=_("Critical at"), allow_empty=False),
                     ],
                 )),
                ("count",
                 Tuple(
                     title=_("Total count"),
                     elements=[
                         Integer(title=_("Warning at"), allow_empty=False),
                         Integer(title=_("Critical at"), allow_empty=False),
                     ],
                 )),
                ("active",
                 Tuple(
                     title=_("Active"),
                     elements=[
                         Integer(title=_("Warning at"), allow_empty=False),
                         Integer(title=_("Critical at"), allow_empty=False),
                     ],
                 )),
            ],
        )

    @property
    def item_spec(self):
        return TextAscii(
            title=_("Type"),
            help=_("Either Containers, Images, Local Volumes or Build Cache"),
            allow_empty=True,
        )
