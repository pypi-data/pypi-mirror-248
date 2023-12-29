#! /usr/bin/env python
# -*- coding: latin1 -*-
""" --- rcOut1.py ---

Adabas Replication Facility Client Example

Generic subscription processor to Adabas file

Program reads Reptor output queue via Broker ACI call interface
as a server

rcOut1Config.py file defines the configuration for processing:
  Broker parameters
  Adabas source and target files
  data structure of subscription

The program could be extended to process an input variable to
read in the name of the configuration file thus working for
multiple subscriptions

o to do:
  transaction continuation
  stats() move into reptor URBS handler
  sversion checking

$Date: 2014-01-28 13:29:09 +0100 (Tue, 28 Jan 2014) $
$Rev: 520 $
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


import sys
import datetime # requires Python2.3

import adabas
from adabas.api import *
from adabas import stck

from adabas.arf     import reptor,urb
from adabas.arf.urb import *

from adabas.exx import broker
from adabas.exx.broker import *

dt=datetime.datetime(datetime.MINYEAR,1,1)
DELTA0=datetime.timedelta(0)

repli = reptor.Replicator()

class Counter:
    def __init__(self):
        global dt
        self.dt=dt.now()
        self.bytes=0L
        self.messages=0L
        self.records=0L
        self.transactions=0L
        self.transUpdCnt=0

cntr=Counter()



cfgpy='rcOut1Config'
cfg = __import__(cfgpy)
pbs = cfg.pbs  # Broker parameters
psu = cfg.psu  # Subscription
psf = None     # current ParmsSfile object
sfile=0

# information on subscription/file status
transStarted=0 # indicator that a transaction has started
transSeq=0     # current TA sequence number


c1=Adabas(rbl=psu.rblmax,fbl=0) # also used for open/close

c1.cb.dbid=psu.tdbid            # set target database
c1.dumpcb=1

lastIsn=0
curIsn=0
numIsn=0L
rtyp=''


def funUrbr(rr,substat):
  "URBR Record block handler"
  global c1, numIsn, rtyp, curIsn, psf, psu, sfile, transStarted

  if not transStarted: # skipping records of this subscription
    return

  if rr.urbrrsp == 0: # only count successful records
    numIsn+=1
    curIsn=0 # reset curIsn if record is ignored, used in urbd handler
    if rr.urbrfnr==sfile:
      curIsn=rr.urbrisn       # set ISN
      rtyp=rr.urbrtyp
    else: # set new sfile
      fnr=rr.urbrfnr
      for sf in psu.sfiles:
        if fnr == sf.sfnr:    # matched source file
          psf=sf
          curIsn=rr.urbrisn   # set ISN
          sfile=sf.sfnr
          rtyp=rr.urbrtyp
          c1.cb.fnr=sf.tfnr
          c1.cb.isn=curIsn
          c1.cb.rbl=psf.dmap.getsize() # set rbl for current file/format
          c1.cb.fbl=len(psf.fb)
          c1.fb=sf.fb


def funUrbd(dd,substat):
  "URBD data block handler"
  global c1, rtyp, numIsn, curIsn, cntr, psf, transStarted

  if not transStarted: # skipping data of this subscription
    return

  print 'Enter URBD handler: %s %s, isn %d' %\
    (rtyp, dd.urbdtyp, curIsn)

  # ignore record if curIsn not zero
  if curIsn!=0:
    c1.cb.isn=curIsn
    if dd.urbdtyp=='B': # before image
      if rtyp=='D' or rtyp=='U': # delete or update
        try:
          c1.cb.cmd='E1'
          c1.call()
          cntr.transUpdCnt+=1
        except DatabaseError, e:
          if e.apa.cb.rsp == 113: # tolerate rsp-113
            print 'Note: Before Image not found ISN %d' % curIsn
            pass
          else:
            raise
    elif dd.urbdtyp=='A': # after image

      if not (rtyp=='I' or rtyp=='R' or rtyp=='U'):
        # not (insert or Initial state or update)
        raise 'invalid after image for urbrtyp %s' % rtyp

      elif rtyp=='I' or rtyp=='R': # insert or Initial state
        try:
          c1.cb.cmd='E1'
          c1.call()
          cntr.transUpdCnt+=1
        except DatabaseError, e:
          if e.apa.cb.rsp == 113: # tolerate rsp-113
            print 'Note: Before Image not found ISN %d' % curIsn
            pass
          else:
            print e.value
            dump(e.apa.acb, header='Control Block')
            raise

      # insert
      cntr.records+=1
      numIsn+=1

      if dd.urbdlend != c1.cb.rbl:
        raise 'Record data length must be %d bytes, rather than %d.'\
          % (c1.cb.rbl, dd.urbdlend)
      else:
        # copy record
        dlen=dd.urbdlend
        c1.rb[0:dlen]=dd.buffer[dd.offset+URBDL:dd.offset+URBDL+dd.urbdlend]
        c1.cb.cmd='N2'
        try:
          print 'c1.cb.isn %d, curIsn %d' % (c1.cb.isn, curIsn)
          c1.call()
          cntr.transUpdCnt+=1
          print "Inserted record %d into file %d " % (c1.cb.isn, c1.cb.fnr)
        except DatabaseError, e:
          print e.value
          dump(e.apa.acb, header='Control Block')
          dump(e.apa.fb, header='Format Buffer')
          dump(e.apa.rb, header='Record Buffer')
          raise

    else:
      raise 'invalid urbdtyp %s' % dd.urbdtyp

  print 'Exit URBD handler: %s %s, isn %d/%d, num recs %d' %\
    (rtyp, dd.urbdtyp, curIsn,c1.cb.isn, numIsn)


def funUrbt(tt,substat):
  global transSeq, transStarted, cntr
  # urbtStat(tt) currently no stats

  # select only this subscription
  if tt.urbtsnam==psu.subscription:
    transSeq=tt.urbttsnr
    transStarted=1
    cntr.transUpdCnt=0
    print 'Exit URBT handler: %s, tsnr %d, in TA %d, cnt %d' %\
      (tt.urbtsnam, transSeq, transStarted, cntr.transUpdCnt)
  else:
     print 'Skipping subscription %s\n' % tt.urbtsnam


def funUrbe(ee,substat):
  global c1, transSeq, transStarted, cntr, psu

  print 'Enter URBE handler: %s tsnr %d, in TA %d, cnt %d' %\
    (ee.urbesnam, transSeq, transStarted, cntr.transUpdCnt)

  if not transStarted: # skipping this subscription
    return

  if ee.urbesnam!=psu.subscription:
    print 'Error: Unexpected subscription %s' % ee.urbesnam

  elif transStarted and cntr.transUpdCnt>0:
    print 'End Transaction %d for subscription %s with %d updates' %\
      (transSeq, psu.subscription, cntr.transUpdCnt)

    if transSeq != ee.urbetsnr:
       raise 'Error: Expected ta seq number %d, but received %d' %\
         (transSeq, ee.urbetsnr)
    else:
      try:
        c1.et()
        transStarted=0
      except DatabaseError, e:
        print e.value
        dump(e.apa.acb, header='Control Block')
        raise

  print 'Exit URBE handler: %s, tsnr %d, in TA %d, cnt %d' %\
    (ee.urbesnam, transSeq, transStarted, cntr.transUpdCnt)


def funUrbh(hh,substat):
  global cntr
  cntr.messages+=1
  cntr.bytes+=hh.urbhlent

print __doc__

repli.setHandler(URBDEYE, funUrbd)
repli.setHandler(URBEEYE, funUrbe)
repli.setHandler(URBHEYE, funUrbh)
repli.setHandler(URBREYE, funUrbr)
repli.setHandler(URBTEYE, funUrbt)

# minimum and recommended ETB buffer size 30720
bb=Broker(receive_length=30720,send_length=128)
bb.trace=4
#bb.trace=1 # dump buffers before Broker calls
#bb.trace=2 # dump buffers after Broker calls
#bb.trace=4  # print Broker calls

bb.broker_id=pbs.broker_id
bb.user_id=pbs.user_id

bb.server_class=pbs.server_class
bb.server_name =pbs.server_name
bb.service     =pbs.service

print 'broker_id = \t', bb.broker_id
print 'user_id = \t', bb.user_id

print 'server_class = \t', bb.server_class
print 'server_name = \t',bb.server_name
print 'service = \t',bb.service

#o print Adabas parameters


try:
  c1.open(mode=UPD)

except DatabaseError, e:
  print e.value
  dump(e.apa.acb, header='Control Block')
  c1.close()
  print 'Terminating due to error'
  sys.exit(0)


bb.conv_id='NONE'

print '\n%s' % bb.version()

bb.logon()

print '\nKernel %s' % bb.kernelVersion()

bb.register()
# now registered as server and reading the messages

uowCnt=0
# receive loop
while 1:
    try:
        bb.receiveNew(wait='1m')

        repli.process(bb.receive_buffer, bb.receive_length, bb.uowStatus)

    except BrokerTimeOut:
        continue
    except KeyboardInterrupt:
        # clean up
        print 'Now terminating due to KeyboardInterrupt'
        c1.close()
        bb.deregister()
        bb.logoff()
        sys.exit(0)
    except DatabaseError, e:
        print e.value
        dump(e.apa.acb, header='Control Block')
        print 'Now terminating due to DatabaseError'
        c1.close()
        bb.deregister()
        bb.logoff()
        sys.exit(0)

    segmentCnt=1
    while bb.uowStatus==RECV_FIRST or bb.uowStatus==RECV_MIDDLE:
        bb.receive()
        segmentCnt+=1
        try:
            repli.process(bb.receive_buffer, bb.receive_length, bb.uowStatus)
        except DatabaseError, e:
            print e.value
            dump(e.apa.acb, header='Control Block')
            print 'Now terminating due to DatabaseError'
            bb.deregister()
            bb.logoff()
            c1.close()
            sys.exit(0)

    bb.commit()
    uowCnt+=1
    if __debug__:
        print 'uow number %d received with %d segments' % (uowCnt, segmentCnt)

