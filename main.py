import numpy as np
import traci


simulation = "highway/highway_project.sumocfg"

sumoBinary = "sumo-gui"
sumoCmd = [sumoBinary, "-c", simulation]

traci.start(sumoCmd)


def speed_and_waiting_time(edge):
   speed = 0
   #waiting = 0
   vehicles = traci.edge.getLastStepVehicleIDs(edge)
   for vehicle in  vehicles:
      speed = traci.vehicle.getSpeed(vehicle)
      #waiting_time = traci.vehicle.getAccumulatedWaitingTime(vehicle)
      speed += speed
      #waiting += waiting_time
   if (len(vehicles) > 0):
      avg_speed = speed / len(vehicles)
      #avg_waiting_time = waiting / len(vehicles)
   #return speed, waiting
   return speed


num_states = 2 # Trafic light on or off
num_actions = 2  # Switch / Don't switch
alpha = 0.5  
gamma = 0.5  
alpha_decay_rate = 1
num_episodes = 25
current_episode = 0
max_steps = 1000  # Number of steps per episodes
length_light = 10
epsilon = 1
epsilon_decay_rate = 0.99

max_speed = 34 * 3.6

traffic_light_id = "ramp_lights"

states = ("r", "G")
state = "G"
traci.trafficlight.setRedYellowGreenState(traffic_light_id, state)

Q = {"r":np.random.rand(num_actions), "G":np.random.rand(num_actions)}


step = 0
while current_episode < num_episodes:
   
   # Just to make sure the traffic is already on the highway when the learning starts
   if step == 0:
      for i in range(100):
         traci.simulationStep()

   for s in range(max_steps):

      if step % length_light == 0:
         # Action 0 : change, Action 1 change pas
         if np.random.rand() < epsilon:
               action = np.random.randint(num_actions)
         else:
            action = np.argmax(Q[state])
         
         print("action", action)

         before_lights_speed = speed_and_waiting_time("before_lights")
         after_lights_speed = speed_and_waiting_time("after_lights")
         #before_ramp_speed, before_ramp_waiting = speed_and_waiting_time("before_ramp")
         after_ramp_speed = speed_and_waiting_time("after_ramp")
         #highway_end_speed = speed_and_waiting_time("highway_end")

         average_speed = (after_ramp_speed + after_lights_speed + before_lights_speed) / 3
         if average_speed == 0:
            reward = -1
         else:
            reward = max_speed / average_speed

         print(state, reward, action)

         # Interaction avec l'environnement
         if action == 0:
            if state == "G":
               next_state = "r"
            else:
               next_state = "G"
         else:
            next_state = state

         Q[state][action] = Q[state][action] + alpha * (reward + gamma * np.max(Q[next_state]) - Q[state][action])

         alpha = alpha * alpha_decay_rate
         epsilon = epsilon * epsilon_decay_rate

         # Passage à l'état suivant
         state = next_state
         traci.trafficlight.setRedYellowGreenState(traffic_light_id, state)

      step += 1
      traci.simulationStep()
   current_episode += 1
   print(current_episode)

traci.close()
print("Result", Q)
	