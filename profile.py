import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.igext as IG

pc = portal.Context()
request = pc.makeRequestRSpec()

tourDescription = \
"""
This profile provides a two node set for Assignmetn two of CSC586
"""
tour = IG.Tour()
tour.Description(IG.Tour.TEXT,tourDescription)
request.addTour(tour)
prefixForIP = "192.168.1."
link = request.LAN("lan")

for i in range(2):
  if i == 0:
    node = request.XenVM("webserver") #create webserver
  else:
    node = request.XenVM("observer")  #create observer
  if i == 0:
    node.routable_control_ip = "true" #public ip for webserver
  else:
    node.routable_control_ip = "false" #private ip for obsever
  
  node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD"
  iface = node.addInterface("if" + str(i))
  iface.component_id = "eth1"
  iface.addAddress(pg.IPv4Address(prefixForIP + str(i + 1), "255.255.255.0"))
  link.addInterface(iface)  
  
  if i == 0:
    node.addService(pg.Execute(shell="sh", command="bash /local/repository/silly.sh"))
  else:
    continue
  
# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
