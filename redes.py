from mininet.node import CPULimitedHost
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.util import dumpNodeConnections
from mininet.node import CPULimitedHost
from mininet.link import TCLink

class JBATopo(Topo):

    def build(self):
        link = dict(bw=150, delay='5ms', loss=4, max_queue_size=100, use_htb=True)

        # Criando sala 1
        s1 = self.addSwitch('s1')
        for h in range(0, 20):
            host = self.addHost('h%s' % (h + 1), cpu=.5/120)
            self.addLink(host, s1, **link)

        # Criando sala 2
        s2 = self.addSwitch('s2')
        for h in range(20, 30):
            host = self.addHost('h%s' % (h + 1), cpu=.5/120)
            self.addLink(host, s2, **link)

        # Criando sala 3
        s3 = self.addSwitch('s3')
        for h in range(30, 40):
            host = self.addHost('h%s' % (h + 1), cpu=.5/120)
            self.addLink(host, s3, **link)

        # Ligando os switchs entre si
        link = dict(bw=150000, delay='1ms', loss=2, max_queue_size=1000, use_htb=True)
        self.addLink(s1, s2, **link)
        self.addLink(s2, s3, **link)


def run():
    net = Mininet(topo=JBATopo(), host=CPULimitedHost, link=TCLink)
    net.start()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()