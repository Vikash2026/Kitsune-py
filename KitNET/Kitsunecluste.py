import numpy as np
import Kitsunecluster

# Kitsunecluster is a lightweight online anomaly detection algorithm based on an ensemble of autoencoders.

class Kitsunecluster:
    #NLB: Network learning before anomoly scores
    #TLM: Times taken to learn mapping
    #LRC: Learning of cluster
    #feature_map
    
    def __init__(self,n,max_autoencoder_size=10,TLM=None,NLB=10000,LRC=0.3,hr=.54, feature_map = None):
        
        self.NLB = NLB
        if TLM is None:
            self.TLM = NLB
        else:
            self.TLM = TLM
        if max_autoencoder_size <= 0:
            self.m = 1
        else:
            self.m = max_autoencoder_size
        self.lr = LRC
        self.hr = hr
        self.n = n

        self.n_trained = 0 
        self.n_executed = 0 
        self.v = feature_map
        if self.v is None:
            print("Feature-Mapper: train-mode, Anomaly-Detector: off-mode")
        else:
            self.__createNLB__()
            print("Feature-Mapper: execute-mode, Anomaly-Detector: train-mode")
        self.TLM = CC.corClust(self.n) 
        self.ensembleLayer = []
        self.outputLayer = None

    def process(self,x):
        if self.n_trained > self.TLM + self.NLB: 
            return self.execute(x)
        else:
            self.train(x)
            return 0.0

    def train(self,x):
        if self.n_trained <= self.TLM and self.v is None: 
            self.TLM.update(x)
            if self.n_trained == self.TLM: #If the feature mapping should be instantiated
                self.v = self.TLM.cluster(self.m)
                self.__createNLB__()
                print("The Feature-Mapper found a mapping: "+str(self.n)+" features to "+str(len(self.v))+" autoencoders.")
                print("Feature-Mapper: execute-mode, Anomaly-Detector: train-mode")
        else: #train layers
            S_l1 = np.zeros(len(self.ensembleLayer))
            for a in range(len(self.ensembleLayer)):
                # make sub instance for autoencoder 'a'
                xi = x[self.v[a]]
                S_l1[a] = self.ensembleLayer[a].train(xi)
            self.outputLayer.train(S_l1)
            if self.n_trained == self.NLB+self.TLM:
                print("Feature-Mapper: execute-mode, Anomaly-Detector: execute-mode")
        self.n_trained += 1

    #execute 
    def execute(self,x):
        if self.v is None:
            raise RuntimeError('KitNET Cannot execute x.')
        else:
            self.n_executed += 1
            ## Ensemble Layer
            S_l1 = np.zeros(len(self.ensembleLayer))
            for a in range(len(self.ensembleLayer)):
                # make sub inst
                xi = x[self.v[a]]
                S_l1[a] = self.ensembleLayer[a].execute(xi)
            ## OutputLayer
            return self.outputLayer.execute(S_l1)

    def __createNLB__(self):
        for map in self.v:
            params = AE.dA_params(n_visible=len(map), n_hidden=0, lr=self.lr, corruption_level=0, gracePeriod=0, hr=self.hr)
            self.ensembleLayer.append(AE.dA(params))

        params = AE.dA_params(len(self.v), n_hidden=0, lr=self.lr, corruption_level=0, gracePeriod=0, hr=self.hr)
        self.outputLayer = AE.dA(params)
