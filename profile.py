import geni.portal as portal
import geni.rspec.igext as IG
import geni.rspec.pg as pg

pc = portal.Context()
request = pc.makeRequestRSpec()

tourDescription = \
tour = IG.Tour()
tour.Description(IG.Tour.TEXT,tourDescription)
request.addTour(tour)
prefixForIP = "192.168.1."
link = request.LAN("lan")

for i in range(2):
  if i == 0:
    node = request.XenVM("webserver")
  else:
    node = request.XenVM("observer") 
  if i == 0:
    node.routable_control_ip = "true"
  else:
    node.routable_control_ip = "false"
  
  node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD"
  iface = node.addInterface("if" + str(i))
  iface.component_id = "eth1"
  iface.addAddress(pg.IPv4Address(prefixForIP + str(i + 1), "255.255.255.0"))
  link.addInterface(iface)  
  
  if i == 0:
    node.addService(pg.Execute(shell="sh", command="bash /local/repository/silly.sh"))
  else:
    continue
 
pc.printRequestRSpec(request)
