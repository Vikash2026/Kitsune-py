from Kitsune import Kitsune
import numpy as np
import time

print("Unzipping file...")
import zipfile
with zipfile.ZipFile("data.zip","r") as zip_ref:
    zip_ref.extractall()
# File location
path = "data.pcap" 
packet_limit = 
maxAE = 10 
TLMG = 100
NLBG = 100
K = Kitsune(path,packet_limit,maxAE,TLMG,NLBG)

print("Running Kitsune:")
RMSEs = []
i = 0
start = time.time()
while True:
    i+=1
    if i % 1000 == 0:
        print(i)
    rmse = K.proc_next_packet()
    if rmse == -1:
        break
    RMSEs.append(rmse)
stop = time.time()
print("Complete. Time elapsed: "+ str(stop - start))

from scipy.stats import norm
bs = np.log(RMSEs[TLMG+NLBG+1:100000])
logP = norm.logsf(np.log(RMSEs), np.mean(bs), np.std(bs))

print("Plotting results")
from matplotlib import pyplot as plt
from matplotlib import cm
plt.figure(figsize=(10,5))
fig = plt.scatter(range(TLMG+NLBG+1,len(RMSEs)),RMSEs[TLMG+NLBG+1:],s=0.1,c=logProbs[TLMG+NLBG+1:],cmap='RdYlGn')
plt.yscale("log")
plt.title("Anomaly Scores from Kitsune's Execution Phase")
plt.ylabel("RMSE (log scaled)")
plt.xlabel("Time elapsed [min]")
figbar=plt.colorbar()
figbar.ax.set_ylabel('Log Probability\n ', rotation=270)
plt.show()
