## O mininet

O mininet é uma máquina virtual criada na Universidade de Stanford, que tem como objetivo simular o funcionamento de uma topologia de rede. 

## Instruções

Para compilar e executar a topologia deve-se:

1. Ir ao diretório onde está o script redes.py 
2. Executar: sudo python redes.py

## Topologia

A topologia usada foi com 3 switchs alinhados, no qual cada um representa uma sala. O s1 tem 20 hosts, o s2 tem 10 hosts e o s3 tem 10 hosts. O s1 esta conectado com o s2 e o s2 está conectado com o s3.
A largura de banda entre os switchs é maior que entre o switch e seu host. A topologia foi baseada no sistema da JBA Imóveis e pode ser facilmente adaptada e usada no laboratório do Dinf da UFPR.

## Testes


### Erro de Encaminhamento
Para simular um erro de encaminhamento usei situação em que o link entre um host e seu respectivo switch fosse quebrado, e após isso tentasse se comunicar com outra máquina.

``` bash
    mininet> link s1 h4 down
    mininet> h4 ping h40
    connect: Network is unreachable
    mininet> h40 ping h4
    PING 10.0.0.1 (10.0.0.1) 56(84) bytes of data.
    From 10.0.0.2 icmp_seq=1 Destination Host Unreachable
    From 10.0.0.2 icmp_seq=2 Destination Host Unreachable
    From 10.0.0.2 icmp_seq=3 Destination Host Unreachable
    From 10.0.0.2 icmp_seq=4 Destination Host Unreachable
    From 10.0.0.2 icmp_seq=5 Destination Host Unreachable
    From 10.0.0.2 icmp_seq=6 Destination Host Unreachable
    ^C
    --- 10.0.0.1 ping statistics ---
    9 packets transmitted, 0 received, +6 errors, 100% packet loss, time 8057ms

```
__Conclusão:__ Conclui com isso que ao tentar conectar-se com uma máquina que possui um problema no link ou cabeamento com o seu respectivo switch ela não pode enviar pacotes e nem receber de quaisquer outras máquinas.

### Congestionamento
Para simular isso, deve-se enviar inúmeros pacotes entre hosts e verificar a largura de banda.

``` bash
    mininet> iperf
    *** Iperf: testing TCP bandwidth between h1 and h40 
    *** Results: ['433 Kbits/sec', '538 Kbits/sec']
    mininet> h1 ping -c100 h8 
    mininet> iperf
    *** Iperf: testing TCP bandwidth between h1 and h40 
    *** Results: ['397 Kbits/sec', '453 Kbits/sec']
```

__Conclusão:__ Conclui com esse teste que ao comparar a largura de banda antes de enviar pacotes e depois de enviados a largura de banda diminui consideravelmente. 
O que nos prova que se enviarmos ainda mais a ponto de chegar no limite da largura, ou mais, haverá congestionamento na rede.


### Largura de banda disponível
Para testarmos a largura de banda vamos testar antes com um baixo delay, de 5ms para os links entre os hosts e o switch e 1ms entre os switches, e 100 pacotes. 

Entre hosts de memsmo switch:

``` bash
    mininet> h1 ping -c100 h2
    100 packets transmitted, 84 received, 16% packet loss, time 99450ms
    rtt min/avg/max/mdev = 21.414/25.184/51.527/6.757 ms

``` 
Entre hosts de switchs diferentes:

``` bash
    mininet> h1 ping -c100 h40
    100 packets transmitted, 79 received, 21% packet loss, time 99665ms
    rtt min/avg/max/mdev = 29.085/62.113/237.252/37.077 ms


```

Agora com o delay entre os links de 20ms e entre os switchs de 4ms, com os mesmos 100 pacotes, obtemos:

``` bash
    mininet> h1 ping -c100 h2
    100 packets transmitted, 94 received, 6% packet loss, time 99299ms
    rtt min/avg/max/mdev = 81.672/87.601/178.865/11.461 ms
```

Entre switchs diferentes:

``` bash
    mininet> h1 ping -c100 h40
    100 packets transmitted, 79 received, 21% packet loss, time 99409ms
    rtt min/avg/max/mdev = 99.340/109.443/217.084/18.647 ms

```
__Conclusao:__ Conclui com esse teste que quando ha comunicação entre hosts de switchs diferentes há uma perda maior de pacotes, menor taxa de pacotes recebidos e em muitos casos um tempo maior de envio. 
Além disso, de acordo com os testes anteriores podemos ver que a largura de banda é fortemente influenciada pela quantidade de pacotes enviados pelos hosts, e que ela diminui quando se tem muitos, o que pode tornar
o ambiente propício a erros e colisões. 

### Prioridade
Não consegui simular esse caso por conta do problema ao instalar e executar o OVS na máquina virtual mininet. Mas se fosse testar, ele daria prioridade para a mensagem (no qual a mensagem com maior prioridade chega antes que a com menor) ou por caminho. 
O switch tem uma tabela na qual ele mapeia a prioridade dos caminhos. Como mostra o exemplo a seguir:

``` bash

    mininet> sh ovs-ofctl show s1
    OFPT_FEATURES_REPLY (xid=0x2): dpid:0000000000000001
    n_tables:254, n_buffers:256
    capabilities: FLOW_STATS TABLE_STATS PORT_STATS QUEUE_STATS ARP_MATCH_IP
    actions: OUTPUT SET_VLAN_VID SET_VLAN_PCP STRIP_VLAN SET_DL_SRC SET_DL_DST SET_NW_SRC SET_NW_DST SET_NW_TOS SET_TP_SRC SET_TP_DST ENQUEUE
    1(s1-eth1): addr:be:22:14:42:b8:9a
    config:     0
    state:      0
    current:    10GB-FD COPPER
    speed: 10000 Mbps now, 0 Mbps max
    2(s1-eth2): addr:46:26:0a:c6:78:12
    config:     0
    state:      0
    current:    10GB-FD COPPER
    speed: 10000 Mbps now, 0 Mbps max
    3(s1-eth3): addr:82:85:b3:ba:68:c8
    config:     0
    state:      0
    current:    10GB-FD COPPER
    speed: 10000 Mbps now, 0 Mbps max
    4(s1-eth4): addr:66:b0:35:2f:4c:10
    config:     0
    state:      0
    current:    10GB-FD COPPER
    speed: 10000 Mbps now, 0 Mbps max
    LOCAL(s1): addr:b2:98:b9:65:30:41
    config:     0
    state:      0
    speed: 0 Mbps now, 0 Mbps max
    OFPT_GET_CONFIG_REPLY (xid=0x4): frags=normal miss_send_len=0

```

Nesse caso, ocorreu um erro de encaminhamento:

``` bash

    mininet> h1 ping h2
    PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
    From 10.0.0.1 icmp_seq=1 Destination Host Unreachable
    From 10.0.0.1 icmp_seq=2 Destination Host Unreachable
    From 10.0.0.1 icmp_seq=3 Destination Host Unreachable
    ^C
    — 10.0.0.2 ping statistics —
    5 packets transmitted, 0 received, +3 errors, 100% packet loss, time 4025ms
    pipe 3
    
``` 

E ao priorizar atravez de alguns comandos ele possibilitou o envio da mensagem corretamente: 

``` bash

    mininet> h1 ping h2
    PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
    64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=1.69 ms
    64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=0.069 ms
    ^C
    — 10.0.0.2 ping statistics —
    2 packets transmitted, 2 received, 0% packet loss, time 1002ms
    rtt min/avg/max/mdev = 0.069/0.884/1.699/0.815 ms
    
``` 