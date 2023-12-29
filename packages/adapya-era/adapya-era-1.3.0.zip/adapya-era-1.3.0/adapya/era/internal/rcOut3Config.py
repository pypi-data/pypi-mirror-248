#! /usr/bin/env python
# -*- coding: latin1 -*-
""" rcOut3Config.py
Configuration file for Reptor Client that reads replication messages
from Reptor output queue

It contains the following information:
- messaging system parameters
- list of subscriptions
- data format of each subscription
- target database/file number for updates
- special processing functions for processing data

Note: Currently one subscription is supported with a list of
      files with different formats

$Date: 2023-12-01 00:54:33 +0100 (Fri, 01 Dec 2023) $
$Rev: 1072 $
"""

from adapya.base.datamap import *
from adapya.era.reptor import ParmsSubscription,ParmsSfile
from adapya.entirex.broker import ParmsBrokerService

# define the mapping of data in record buffer to attributes
# of EmpTest class

empTestFormat='AA,16,AC,16,AD,16,AK,4,AN,4.'

# create datamap object for Employees-Telephone-List
emp=Datamap('EmplTest',
    String('TestId',  16),
    String('firstname',    16),
    String('middlename',   16),
    Packed('postcode',      4),
    Packed('areacode',      4),
    encoding='cp424'            # hebrew ebcdic codepage
    )

# define formats and mapping for each file specified in subscription
#psf=ParmsSfile(sdbid=8,sfnr=11,tdbid=12,tfnr=7,\
#      fb=empTelFormat,dmap=emp)
psf=ParmsSfile(sdbid=10026,sfnr=11,tdbid=0,tfnr=0,\
      fb=empTestFormat,dmap=emp)

# define subscription with all its sfiles defined
#psu=ParmsSubscription(subscription='EMPLOYE8',sversion='01',sfiles=[psf])
psu=ParmsSubscription(subscription='EMPLOYEE',sversion='01',sfiles=[psf])


# define Reptor Broker parameters
pbs=ParmsBrokerService(\
        broker_id='daey:3800',\
        server_class='REPTOR',
        server_name='MMSERV',
        service='OUT3',
        user_id='MM')

#  Copyright 2004-2023 Software AG
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
