#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2014, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a sepaself.rate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

import unittest
import numpy
from nupic.research.spatial_pooler import SpatialPooler
from sensorimotor.spatial_pooler_monitor_mixin import (
  SpatialPoolerMonitorMixin)
class MonitoredSpatialPooler(SpatialPoolerMonitorMixin, SpatialPooler): pass

class SpatialPoolerMonitorMixinTest(unittest.TestCase):

  VERBOSITY = 2


  def setUp(self):
    # Initialize the spatial pooler
    self.sp = MonitoredSpatialPooler(
                       inputDimensions=(15,),
                       columnDimensions=(4,),
                       potentialRadius=15,
                       numActiveColumnsPerInhArea=1,
                       globalInhibition=True,
                       synPermActiveInc=0.03,
                       potentialPct=1.0)

    cat = numpy.array( [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype='uint8')
    dog = numpy.array( [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0], dtype='uint8')
    rat = numpy.array( [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], dtype='uint8')
    bat = numpy.array( [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1], dtype='uint8')
    output = numpy.zeros((4,), dtype="int")
    self.activeColumns = numpy.zeros((400,4), dtype="int")
    for i in xrange(100):
        self.sp.compute(cat, learn=True, activeArray=output)
        self.activeColumns[4*i+0] = output
        self.sp.compute(dog, learn=True, activeArray=output)
        self.activeColumns[4*i+1] = output
        self.sp.compute(rat, learn=True, activeArray=output)
        self.activeColumns[4*i+2] = output
        self.sp.compute(bat, learn=True, activeArray=output)
        self.activeColumns[4*i+3] = output


  def testGetActiveColumn(self):
    # test whether the active column indices are correctly stored
    for i in range(400):
        self.assertTrue(self.activeColumns[i][self.sp.mmGetTraceActiveColumns().data[i]]==1)


  def testGetActiveDutyCycles(self):
    # test whether active duty cycle are calculated correctly
    self.assertTrue(numpy.sum(self.sp.mmGetDataDutyCycles()) == 400)


  def testClearHistory(self):
    # test whether history has been cleared with mmClearHistory
    # if we run clear history, the traces should be empty
    self.sp.mmClearHistory()
    self.assertTrue(self.sp.mmGetTraceActiveColumns().data==[])
    self.assertTrue(self.sp.mmGetTraceNumConnections().data==[])


  def testGetTraceNumConnections(self):
    self.assertTrue(self.sp.mmGetTraceNumConnections().data[-1]>=3*4)


  def testGetDefaultTrace(self):
    # default trace with verbosity level==1 returns count traces of activeColumn
    # and connections
    defaultTrace = self.sp.mmGetDefaultTraces()
    self.assertTrue(all(defaultTrace[0].data))
    self.assertTrue(max(defaultTrace[0].data)==1)

    # default trace with verbosity==2 returns indices trace of activeColumn
    # and count trace of connections
    defaultTrace = self.sp.mmGetDefaultTraces(verbosity=2)
    for i in range(len(defaultTrace[0].data)):
        self.assertTrue(self.sp.mmGetTraceActiveColumns().data[i] == defaultTrace[0].data[i])


  def testGetDefaultMetrics(self):
    # print default metrics
    print self.sp.mmPrettyPrintMetrics(self.sp.mmGetDefaultMetrics())

if __name__ == "__main__":
  unittest.main()
