import sys
import re
import statistics

numofnodes = 40

# filename = sys.argv[1]
filename = "rand2log2.txt"

with open(filename) as f:
  rows = (line.split() for line in f)
  mainhold = []
  for row in rows:
    mainhold.append(row)
    #print(row)

# to calculate total number of line sent per node

  for x in range(0, numofnodes):
    holder = []
    for row in mainhold:
      if row[1] == "ID:" + str(x+1) and row[2] == "Sending":
        holder.append(row)
    print("Number of packets sent by Node:" + str(x+1) + " is " + str(len(holder)))

  print("")

# Packet delivery ratio

  #for x in range(0, numofnodes):
  holder1 = []
  holder2 = []
  for row in mainhold:
    if row[2] == "Sending":
      holder1.append(row)
    sent = len(holder1)
    # print(row)
    if row[2] == "Received":
      holder2.append(row)
    received = len(holder2)
  print("Packet Delivery Ratio for Nodes is " + str(float(received)/sent))

# row[1] == "ID:" + str(x+1) and
# row[1] == "ID:" + str(x + 1) and
# and row[6] == str(x+1)

  print("")

# for Power usage per Node
  holder = []
  for row in mainhold:
    #print(row)
    if row[2] == "Power" and row[5] == "P":
      holder.append(row)
  for x in range(0, numofnodes):
    temp = []
    for line in holder:
      if line[1] == "ID:" + str(x+1):
        temp.append(line)
    sum = 0
    result = 0
    length = len(temp)
    # print(length)
    for item in temp:
      cpu = int(item[14])
      lpm = int(item[15])
      tx = int(item[16])
      rx = int(item[17])
      result = ((tx*19.5 + rx*21.8 + cpu*1.8 + lpm*0.0545)*3)/(37629*10)
      sum += result
      #print(result)
    avg = float(sum)/length
    print("Average power consumption for Node:" + str(x+1) + " is " + str(avg))

  print("")
# Dissemination Time is the length of time from the introduction of new data into the network, until all of the nodes in the network report having received the new data.
# Assume calculating average Dissemination Time
# = to last string that has their token is newer. Update to token x - generating new token x
  token = []
  for row in mainhold:
    try:
      if row[4] == "Generating":
        token.append(row)
    except IndexError:
      pass
  numoftokens = len(token)
  print("The total number of tokens is " + str(numoftokens) + "\n")

  timings = []
  for x in range(0, numoftokens):
    startime = []
    endtime = []
    for row in mainhold:
      try:
        if row[4] == "Generating" and row[9] == str(x + 1):
            startime.append(row[0])
      except IndexError:
        pass

      try:
        if row[6] == "Update" and row[9] == str(x+1):
          endtime.append(row[0])
      except IndexError:
        pass
      if len(endtime) >= numofnodes-1:
        start = startime[0]
        end = endtime[numofnodes-2]
        print("The start time of token " + str(x+1) + "'s distribution is " + startime[0])
        print("The last time of update for token " + str(x+1) + " is " + endtime[numofnodes-2] + "\n")
        break

    startsplit = start.split(":")
    endsplit = end.split(":")
    #print(startsplit)
    #print(endsplit)
    minutes = (float(endsplit[0]) - float(startsplit[0]))*60
    seconds = float(endsplit[1]) - float(startsplit[1])
    #print(minutes)
    #print(seconds)
    timediff = minutes + seconds
    #print(timediff)
    timings.append(timediff)
  #print(timings)
  timeavg = round(statistics.mean(timings),5)
  print("The average dissemination time is " + str(timeavg) + " seconds")


