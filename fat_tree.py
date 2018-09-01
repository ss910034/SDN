from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import Controller,RemoteController
from mininet.topo import Topo
from mininet.link import Link, Intf, TCLink


class Fattree(Topo):
    
    CoreSwitchList = []
    AggSwitchList = []
    EdgeSwitchList = []
    Host = []

    def __init__(self,k,density):
        #initialize
        self.pod = k
        self.iCoreLayerSwitch = (k/2)**2
        self.iAggLayerSwitch = k*k/2
        self.iEdgeLayerSwitch = k*k/2
        self.density = density
        self.iHost = self.iEdgeLayerSwitch * density

        #Init Topo
        Topo.__init__(self)

    def createTopo(self):
        self.createCoreLayerSwitch(self.iCoreLayerSwitch)
        self.createAggLayerSwitch(self.iAggLayerSwitch)
        self.createEdgeLayerSwitch(self.iEdgeLayerSwitch)
        self.createHost(self.iHost)
    
    def netaddSwitch(self,number,level,switch_list):
        for i in range(1,number+1):
            if i >= int(10):
                check = "0"
            else:
                check = "00"
            switch_list.append(self.addSwitch('s'+str(level)+check+str(i)))

    def createCoreLayerSwitch(self,number):
        self.netaddSwitch(number,1,self.CoreSwitchList)

    def createAggLayerSwitch(self,number):
        self.netaddSwitch(number,2,self.AggSwitchList)

    def createEdgeLayerSwitch(self,number):
        self.netaddSwitch(number,3,self.EdgeSwitchList)

    def createHost(self,number):
        for i in range(1,number+1):
            if i >= int(10):
                check = "0"
            else:
                check = "00"
            self.Host.append(self.addHost('h4'+check+str(i)))

    def createLink(self,bw_c2a=0.2,bw_a2e=0.1,bw_e2h=0.5):
        end = self.pod/2
        for x in range(0,self.iAggLayerSwitch,end):
            for i in range(0,end):
                for j in range(0,end):
                    self.addLink(self.CoreSwitchList[i*end+j],self.AggSwitchList[x+i],bw=bw_c2a)
        
        for x in range(0,self.iEdgeLayerSwitch,end):
            for i in range(0,end):
                for j in range(0,end):
                    self.addLink(self.AggSwitchList[x+i],self.EdgeSwitchList[x+j],bw=bw_a2e)
    
        for x in xrange(0, self.iEdgeLayerSwitch):
            for i in xrange(0, self.density):
                self.addLink(self.EdgeSwitchList[x],self.Host[self.density * x + i],bw=bw_e2h)
    
    def set_ovs_protocol_13(self,):
        self._set_ovs_protocol_13(self.CoreSwitchList)
        self._set_ovs_protocol_13(self.AggSwitchList)
        self._set_ovs_protocol_13(self.EdgeSwitchList)

    def _set_ovs_protocol_13(self, sw_list):
            for sw in sw_list:
                cmd = "sudo ovs-vsctl set bridge %s protocols=OpenFlow13" % sw
                os.system(cmd)


def createTopo():
    topo = Fattree(4,2)
    topo.createTopo()
    topo.createLink(bw_c2a=0.2,bw_a2e=0.1,bw_e2h=0.05)

    Controller_ip = "127.0.0.1"
    Controller_port = 6633
    net = Mininet(topo=topo,link=TCLink,controller=None,autoSetMacs=True,autoStaticArp=True)
    net.addController('c0',controller=RemoteController,ip=Controller_ip,port=Controller_port)
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    createTopo()