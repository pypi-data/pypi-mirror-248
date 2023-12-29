#! /usr/bin/env python
# -*- coding: latin1 -*-
""" tapa12config.py

Configuration file for Reptor Target Adabas

Adapter reads replication messages

It contains the following information:
- messaging system parameters
- list of subscriptions
- data format of each subscription
- target database/file number for updates
- special processing functions for processing data

Note: Currently one subscription is supported with a list of
      files with different formats

Example: used with readris.py (see there for more)

    adabas/arf/readris.py -f mm.temp.rpeapemu -a tapa12config


"""

from adabas.datamap import *
from adabas.arf.reptor import ParmsSubscription,ParmsSfile
# from adabas.exx.broker import ParmsBrokerService

# define the mapping of data in record buffer to attributes
# of EmpTel class

FBPEMU=\
  'AA,16,A,UN,4,U,PA,2,P,FX,2,F,BI,2,B,FL,4,G,AN,32,A,DT,4,P,TI,7,P,'\
  'LO,1,B,MU1-3,4,A,C1,1,P,'\
  'P11,4,A,P21(1-2),4,A,P31,1,P,'\
  'P12,4,A,P22(1-2),4,A,P32,1,P,'\
  'C2,1,P,OK,2,A.'

# define formats and mapping for each file specified in subscription
#psf=ParmsSfile(sdbid=8,sfnr=11,tdbid=12,tfnr=7,\
#      fb=empTelFormat,dmap=emp)

psf=ParmsSfile(sdbid=10006,sfnr=25,tdbid=12,tfnr=125,\
      fb=FBPEMU,dmap=None)

# define subscription with all its sfiles defined
#psu=ParmsSubscription(subscription='EMPLOYE8',sversion='01',sfiles=[psf])

psu=ParmsSubscription(subscription='PEMU',sversion='01',sfiles=[psf])



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
