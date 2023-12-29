#! /usr/bin/env python
# -*- coding: latin1 -*-
""" out1Config.py
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

$Date: 2012-10-15 13:22:09 +0200 (Mon, 15 Oct 2012) $
$Rev: 389 $
"""

#  Copyright 2004-2008 Software AG
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

from adabas.datamap import *
from adabas.arf.reptor import ParmsSubscription,ParmsSfile
from adabas.exx.broker import ParmsBrokerService

# define the mapping of data in record buffer to attributes
# of EmpTel class

empTelFormat='AA,AC,AD,AE,AH,8,U,AL,AN,AM,AO,AP.'

# create datamap object for Employees-Telephone-List
emp=Datamap('EmplTel',
    String('personnel_id',  8),
    String('firstname',    20),
    String('m_initial',    20),
    String('lastname',     20),
    String('birth',         8),
    String('country',       3),
    String('areacode',      6),
    String('phone',        15),
    String('department',    6),
    String('jobtitle',     25)
    )

# define formats and mapping for each file specified in subscription
#psf=ParmsSfile(sdbid=8,sfnr=11,tdbid=12,tfnr=7,\
#      fb=empTelFormat,dmap=emp)
psf=ParmsSfile(sdbid=10006,sfnr=11,tdbid=12,tfnr=7,\
      fb=empTelFormat,dmap=emp)

# define subscription with all its sfiles defined
#psu=ParmsSubscription(subscription='EMPLOYE8',sversion='01',sfiles=[psf])
psu=ParmsSubscription(subscription='EMPLOYEE',sversion='01',sfiles=[psf])


# define Reptor Broker parameters
pbs=ParmsBrokerService(\
        broker_id='daey:3800',\
        server_class='REPTOR',
        server_name='MMSERV',
        service='OUT4',
        user_id='UEmplTel')

