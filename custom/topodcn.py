#!/usr/bin/python

from mininet.topo import Topo

class ClosTopo(Topo):

	"""
	# name: ToR's name
	# noSrv: number of servers
	"""
	def buildToR(self, name: str, noSrv: int):
		ToR = self.addSwitch(name)
		for i in range(noSrv):
			srv = self.addHost(f'{name}-server{i}')
			self.addLink(srv, ToR)
		return ToR

	"""
	# name: aggregation block's name
	# noBlk: number of aggregation blocks
	# noToRs: number of ToRs
	"""
	def buildAggregation(self, name: str, noBlk: int, noToRs: int):
		noSrv = 20

		aggr_blks = []
		for i in range(noBlk):
			aggr_blk = self.addSwitch(f'{name}-aggr{i}')
			aggr_blks.append(aggr_blk)

		for i in range(noToRs):
			ToR = self.buildToR(f'{name}-ToR{i}', noSrv)
			for aggr_blk in aggr_blks:
				self.addLink(ToR, aggr_blk)

		return aggr_blks

	"""
	# name: cluster's name
	# noSpines: number of spine blocks
	# noAggrs: number of aggregation blocks
	"""
	def buildCluster(self, name: str, noSpines: int, noAggrs: int):
		noAggrBlks = 4
		noToRs = 16
		spines = []
		for i in range(noSpines):
			spine = self.addSwitch(f'{name}-spine{i}')
			spines.append(spine)
		
		# we want let the last aggregation block connect to external
		for i in range(noAggrs-1):
			aggr_switchs = self.buildAggregation(f'{name}-aggr{i}', noAggrBlks, noToRs)
			for aggr_switch in aggr_switchs:
				for spine in spines:
					self.addLink(aggr_switch, spine)
		
		# external aggregation block, no ToRs, connect to all spine blocks
		# 0 means no ToRs
		ext_switchs = self.buildAggregation(f'{name}-ext-aggr{noAggrs-1}', noAggrBlks, 0)
		for ext_switch in ext_switchs:
			for spine in spines:
				self.addLink(ext_switch, spine)

		# return switchs for external link
		return ext_switchs

	"""
	# name: device's name
	# noClsts: number of clusters
	"""
	def addDFD(self, name: str, noClsts: int):
		# add datacenter level freedome border
		self.DFDs[name] = []
		for i in range(4):
			FDB = self.addSwitch(f'{name}-FDB{i}')
			self.DFDs[name].append(FDB)
		
		# add clusters
		for i in range(noClsts):
			ext_switchs = self.buildCluster(f'{name}-cluster{i}', 4, 8)
			for ext_switch in ext_switchs:
				for FDB in self.DFDs[name]:
					self.addLink(ext_switch, FDB)

	"""
	# noDFDs: number of datacenter freedomes
	"""
	def buildCampus(self, noDFDs: int):

		# add campus freedome borders
		self.CFDBs = []
		for i in range(4):
			CFDB = self.addSwitch(f'CFDB{i}')
			self.CFDBs.append(CFDB)

		# add datacenter freedomes (DFDs)
		self.DFDs = {}
		for i in range(noDFDs):
			key = f'DFD{i}'
			self.addDFD(key, 8)
		
		# add link: connect all FDBs at datacenter level with all FDBs at campus level
		for CFDB in self.CFDBs:
			for key,DFD in self.DFDs.items():
				for DFDB in DFD:
					self.addLink(DFDB, CFDB)


	def build(self):
		self.buildCampus(8)


topos = { 'clostopo': ( lambda: ClosTopo() ) }
