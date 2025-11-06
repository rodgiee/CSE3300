# Final Skeleton
#
# Hints:
#
# To check the source and destination of an IP packet, you can use
# the header information... For example:
#
# ip_header = packet.find('ipv4')
#
# if ip_header.srcip == "1.1.1.1":
#   print "Packet is from 1.1.1.1"
#
# Important Note: the "is" comparison DOES NOT work for IP address
# comparisons in this way. You must use ==.
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def send_out(self, packet, packet_in, port):
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 30
    msg.hard_timeout = 30

    msg.actions.append(of.ofp_action_output(port = port))
    msg.data = packet_in
    self.connection.send(msg)

  def send_drop (self, packet, packet_in):
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 30
    msg.hard_timeout = 30
    msg.data = packet_in
    self.connection.send(msg)
    return

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. 
    #   - port_on_switch: represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet.
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    # You should use these to determine where a packet came from. To figure out where a packet 
    # is going, you can use the IP header information.

    ip = packet.find('ipv4')
    if ip is None:
      ipv2 = packet.find('ipv6')
      if ipv2 is None:
        self.send_out(packet, packet_in, of.OFPP_FLOOD)
      return

    if switch_id == 1:
      if ip.dstip == '10.1.1.10':
        self.send_out(packet, packet_in, 1)
      else:
        self.send_out(packet, packet_in, 2)
      return

    elif switch_id == 2:
      if ip.dstip == '10.2.2.20':
        self.send_out(packet, packet_in, 1)
      else:
        self.send_out(packet, packet_in, 2)
      return

    elif switch_id == 3:
      if ip.dstip == '10.3.3.30':
        self.send_out(packet, packet_in, 1)
      else:
        self.send_out(packet, packet_in, 2)
      return

    elif switch_id == 4:
      icmp = packet.find('icmp')
      if ip.srcip=='123.45.67.89' and ((icmp is not None) or (ip.dstip == '10.5.5.50')):
        self.send_drop(packet, packet_in)
      elif ip.dstip == '123.45.67.89':
        self.send_out(packet, packet_in, 1)
      elif ip.dstip == '10.1.1.10':
        self.send_out(packet, packet_in, 2)
      elif ip.dstip == '10.2.2.20':
        self.send_out(packet, packet_in, 3)
      elif ip.dstip == '10.3.3.30':
        self.send_out(packet, packet_in, 4)
      elif ip.dstip == '10.5.5.50':
        self.send_out(packet, packet_in, 5)
      return

    elif switch_id == 5:
      if ip.dstip == '10.5.5.50':
        self.send_out(packet, packet_in, 1)
      else:
        self.send_out(packet, packet_in, 2)
      return

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
