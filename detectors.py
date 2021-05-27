import numpy as np
from numpy.linalg import norm
import random
from sklearn.gaussian_process.kernels import WhiteKernel, ExpSineSquared, RBF,ConstantKernel
from sklearn.gaussian_process import GaussianProcessRegressor
from scipy.stats import betabinom
from sklearn.metrics import confusion_matrix


class SinglePointDetector:
    _estimator_type ='classifier'
    classes_ = [0,1]
    
    def fit(self,x):
        self.x_min = x.min()
        self.x_max = x.max()
        return self
    
    def predict(self,x):
        return np.array([0 if p>= self.x_min and p<= self.x_max else 1 for p in x])
    
class LiklihoodRatioDetector:
    _estimator_type='classifier'
    classes_=[0,1]
    
    def fit(self,x_b,x_m,fp_rate):
        self.scaler = preprocessing.MinMaxScaler().fit(x_b)
        x = self.scaler.transform(x_b)
        self.gm = GaussianMixture(1,covariance_type='spherical',init_params='kmeans',n_init=1000,max_iter=1000,reg_covar=1e-10)
        self.gm.fit(x)
        
        r_m = []
        r_b = []
        for i in range(100):
            r_b.append(self.predict_prob(np.array(random.sample(x_b.tolist(),10)).reshape(-1,1)))
            r_m.append(self.predict_prob(np.array(random.sample(x_m.tolist(),10)).reshape(-1,1)))
        
        y = [1] * len(r_m) + [0] * len(r_b)
        fpr, tpr, thresholds = metrics.roc_curve(y,r_m+r_b,pos_label=1,drop_intermediate=False)
        self.threshold = thresholds[np.where(fpr==fp_rate)[0][0]]
        return self
    
    def predict_prob(self,x):
        x = self.scaler.transform(x)
        gm_m_null = GaussianMixture(1,covariance_type='spherical',init_params='kmeans',n_init=1000,max_iter=1000,reg_covar=1e-10)
        gm_m_null.fit(x)
        if np.exp(self.gm.score(x)) == 0:
            return 0
        return np.exp(gm_m_null.score(x))/np.exp(self.gm.score(x))
    
    def predict(self,X):
        return [1 if self.predict_prob(x) > self.threshold else 0 for x in X]


class RandomizedLiklihoodRatioDetector:
    _estimator_type='classifier'
    classes_=[0,1]
    classifiers = []
    thresholds = []
    def __init__(self,n,r,a,b):
        self.n = n
        self.r = r
        self.a = a
        self.b = b
        
        
        
    def get_index(self):
        x = np.arange(self.n)
        #         fig, ax = plt.subplots(1, 1)
        #         ax.plot(x, betabinom.pmf(x, n-1, a, b), 'bo', ms=8, label='betabinom pmf')
        #         plt.show()
        return np.random.choice(np.arange(self.n), p=betabinom.pmf(x, self.n-1, self.a, self.b))
        
    def fit(self,x_b,x_m,fp_rate):
        print('Im called here!')
        self.classifiers = []
        x_min = x_b.reshape(-1,1).mean()
        x_max = x_b.reshape(-1,1).max()
        i = [  (-(((np.tanh((i-x_min)/(self.n*self.r)) * (x_max-x_min)))/np.tanh(1/self.r))+x_min,
                 (((np.tanh((i-x_min)/(self.n*self.r)) * (x_max-x_min)))/np.tanh(1/self.r))+x_min) for i in range(1,self.n+1)]

        self.scaler = preprocessing.MinMaxScaler().fit(x_b)
        x = self.scaler.transform(x_b)
        
        for c_i in range(self.n):
            gm = GaussianMixture(1,covariance_type='spherical',init_params='kmeans',n_init=1000,max_iter=1000,reg_covar=1e-10)
            gm.fit(x)

            r_m = []
            r_b = []
            for i in range(100): #### CHANGEEEEEEEEEEEEEEEE THIS BACK TO 100
                r_b.append(self.predict_prob_gm(np.array(random.sample(x_b.tolist(),10)).reshape(-1,1),gm))
                r_m.append(self.predict_prob_gm(np.array(random.sample(x_m.tolist(),10)).reshape(-1,1),gm))

            y = [1] * len(r_m) + [0] * len(r_b)
            fpr, tpr, thresholds = metrics.roc_curve(y,r_m+r_b,pos_label=1,drop_intermediate=False)
            #print('{0}\n\t{1}'.format(list(zip(fpr,tpr)),thresholds))
            found = np.where(fpr==fp_rate)[0]
            if len(found) == 0:
                found = np.where(tpr==1.0)[0]
            #print(found)
            #print(thresholds[found[0]])
            self.thresholds.append(thresholds[found[0]])
            self.classifiers.append(gm)
        return self
    
    def predict_prob_gm(self,x,gm):
        x = self.scaler.transform(x)
        gm_m_null = GaussianMixture(1,covariance_type='spherical',init_params='kmeans',n_init=1000,max_iter=1000,reg_covar=1e-10)
        gm_m_null.fit(x)
        if np.exp(gm.score(x)) == 0:
            return 0
        return np.exp( gm_m_null.score(x))/np.exp(gm.score(x))
    
    def predict_prob(self,x):
        i = self.get_index() #np.random.randint(0,len(self.thresholds))
        return self.predict_prob_gm(x,self.classifiers[i]),i
        
    
    def predict(self,X):
        probs = [self.predict_prob(x) for x in X]
        #print(probs)
        return [1 if prob[0] > self.thresholds[prob[1]] else 0 for prob in probs]


