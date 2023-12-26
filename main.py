import traci

simulation = "highway/highway_project.sumocfg"

sumoBinary = "sumo-gui"
sumoCmd = [sumoBinary, "-c", simulation]

traci.start(sumoCmd)


def speed_and_waiting_time(edge):
   speed = 0
   waiting = 0
   vehicles = traci.edge.getLastStepVehicleIDs(edge)
   for vehicle in  vehicles:
      speed = traci.vehicle.getSpeed(vehicle)
      waiting_time = traci.vehicle.getAccumulatedWaitingTime(vehicle)
      speed += speed
      waiting += waiting_time
   if (len(vehicles) > 0):
      avg_speed = speed / len(vehicles)
      avg_waiting_time = waiting / len(vehicles)
   return speed, waiting


step = 0
while True:

   before_lights_speed, before_lights_waiting = speed_and_waiting_time("before_lights")
   after_lights_speed, after_lights_waiting = speed_and_waiting_time("after_lights")
   before_ramp_speed, before_ramp_waiting = speed_and_waiting_time("before_ramp")
   after_ramp_speed, after_ramp_waiting = speed_and_waiting_time("after_ramp")
   highway_end_speed, highway_end_waiting = speed_and_waiting_time("highway_end")


   # To change the traffic light state, set it to "G" or "r"
   """
   traffic_light_id = "ramp_lights"
   state = "G"
   traci.trafficlight.setRedYellowGreenState(traffic_light_id, state)
   """

   step += 1
   traci.simulationStep()
	