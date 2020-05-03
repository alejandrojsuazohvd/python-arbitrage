# python-arbitrage
### Developed by Alejandro Suazo
This is a python arbitrage application that trades currencies between Zcash, Bitcoin, and Etherium.

### Project
This application attemps to capitalize on fluctuations of cryptocurrency relative values and trading to facilitate profit through arbitrage.
 
### High Level Design
![Image of High Level Design](https://drive.google.com/uc?export=download&id=1cwRVs0sIHR3WCb2rPSTTJA3GPxfw--0e)

### The Arbitrage Algorithm Design
We have prices of trade pairs
```
if AB, BC, CA, BA, CB, and AC
     then if the ratio of price between AB is ratio_1, AC is ratio_2, CB is ratio_3
        if ratio_1 > ratio_2 & ratio_3
             then trade A -> C -> B -> A
```
Ex: If the ratios are as follows
```    
2:4 > 1:2 & 2:3
   then A -> C -> B -> A would have a 50% return on investment.
``` 

Then the algorithm continues to do this comparison. BTC is the most truthful orderbook so we will keep our running balance on BTC
2nd problem: trade fees.
So I determined the maximum fees per trade and the GAIN after the trade has COVER the fee costs.
so this now requires the algorithm to determine potential gain on prior to committing a transaction
The condition is as follows
```
if ratio_AB > ratio_AC & ratio_CB
   AND ratio_AC & ratio_CB & ratio_BA > fee %
      then trade A -> C -> B -> A
```


### Requirements
Must have Python3 installed.

Docker is not necessary but **strongly recommended**.

If running through only python the shirmpy-python package will be required. This can be avoided by using docker to run this application. See setup for more information.


### Setup
_NONE!_ If you use the provided docker container run script, you will not need to install anything else onto your machine and the docker container will take care of all of the setup.

If you are **not** going to use the docker container and would like to run the code directly please install shrimpy-python. The project is only dependet on one non-native python library `shrimpy-python`.
```
pip install shrimpy-python
```

### Running
#### Running the Docker Container
Using the docker route,
All you need to do is run the included run_docker.sh script with sudo privileges.
```bash
sudo ./run_docker.sh
```
#### Running The Python
To run the python directly on your box. Go into the root directory of this application and run: 
```
python pythonArbitrage.py
```
Again this route requires the shrimpy-python library. See setup section for more information.
#### Going through the dedicated CICD pipeline
To accomplish this is a little more involved but more production ready and facilitates the rest of the design.

First clone the Jenkins respository 
```bash
git clone https://github.com/alejandrojsuazohvd/jenkins-arbitrage.git
```

Then run the setup_docker.sh script with sudo privileges.
```bash
sudo ./setup_docker.sh
```
This will walk you through a creation of a user named `jenkins`.

Once creating a jenkins user you will be able to run, the run_docker.sh script **found in the jenkins-arbitrage directory** with sudo privileges (not to be confused with the one within the python project).
```bash
sudo ./run_docker.sh
```
Your Jenkins instance should now be running on `http://localhost:8080`

To start the python arbitrage program we now have to do a few things!

1.) Go into your jenkins instance on a web browser.
![Step1](https://drive.google.com/uc?export=download&id=1sJLSdeNkr46yYbsb10IXonBikIMZolyy)

2.) Find the ArbitragePythonCICD job and click into it.
![Step2](https://drive.google.com/uc?export=download&id=195tg9UAVV4Kk7NWQSHwXO5yFuhcvhyJe)

3.) In the ArbitragePythonCICD job click the `Build Now` option on the left menu. This will begin the initial instance of your pythonArbitrage job. You should see a new job on your build history section.
![Step3](https://drive.google.com/uc?export=download&id=18W9E65SOxlUdylPo5S18K8I4Jz1dWRsv)

4.) Click on the number of you latest build to go into it's page.
![Step4](https://drive.google.com/uc?export=download&id=1BiMbbPjz41dL8A92ASblMmAYAm333uXd)

5.) Click on Console Output to see if your python project started successfully.
![Step5](https://drive.google.com/uc?export=download&id=1IB2AMGYvHp1KA6dFqI-RrT22GyxjS5KP)

Now! So long as your jenkins server is running, it will automatically poll for updates to the github repository and stop/rerun a new instance of the latest code! 

### All together now!
With each method you should always have a local webserver that displays you applications logs (including trades) at 
```bash
http://localhost:8081
```

## Results
Is it profitable? 
- Sadly, no. There are a few limitations that I discovered throughout the process. 
    - 1.) Market trades take time. Especially if you're going through intermediary companies.
    - 2.) Fees are extraordinarily high.
    - 3.) For trades to succeed you need accurate information. Some trading pair order books can have lackluster trust. 
    - 4.) Market fluctuations make it difficult to keep track of overall USD value although quantity of crytocurrency is known.
    
Can this be improved?
- Absolutely. 
    - There is significant effort for people to handle trades and conversions on their own instead of a intermediary company.
    - Additionally, the performance could be improved if I work more directly with the Exchange I am using (Gemini for this application). Because I'm going through Shrimpy I am making two network hops for my trades to go through. Although Shrimpy does provide connections and orderbooks of a variety of source. I would not conduct trade through their service. I would only do orderbook data gathering with their socket services.  
  
