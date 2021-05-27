def lognormal_loss(p_tx, d,r=2,sigma=1):
    #d is distance in meter!
    pl_0 = 40.0476035#0.11441574835#31.0181026683
    x_g= np.random.normal(0,sigma)
    ex = (pl_0 + (10*r*math.log10(d)) +x_g - (10*math.log10(p_tx)))/-10
    return 10**ex

def distance_lognormal_loss(p_tx,p_rx,r=2,sigma=1):
    pl_0 = 40.0476035#31.0181026683
    x_g= 0 #np.random.normal(0,sigma) if you are solving for distance consider mean 0
    ex = ((10 * math.log10(p_tx)) - (10 * math.log10(p_rx)) - pl_0 + x_g)/(10 * r)
    return 10**ex

def power_transmit_lognormal_loss(p_rx,d,r=2,sigma=1):
    pl_0 = 40.0476035#31.0181026683
    #x_g= np.random.normal(0,sigma) this is going to be transmit power ... it should not be stochastic
    #ex = (math.log10(p_rx) + pl_0+ (10 * r * math.log10(d)))/10.0
    return math.exp(r * math.log(d) + 9.221301483) * p_rx

def mixed_adversary_samples(benign,left_adverserial, right_adverserial,length=10,ratio=0.5):
    # This creates sequence of samples where malicious samples's half-sequence is drawn from begning distrbution
    total = len(benign)

    a = np.array_split(benign,total/length)
    a_r = np.array_split(benign,(total/length)/ratio )
    b_r = np.array_split(left_adverserial,(total/length)/ratio )
    c_r = np.array_split(right_adverserial,(total/length)/ratio )
    a_b = np.concatenate([a_r,b_r],axis=1)
    a_c = np.concatenate([a_r,c_r],axis=1)
    
    return np.concatenate([a,a_b,a_c]),np.concatenate([[0] * len(a) ,[1] * (len(a_b) + len(a_c))])

def samples(benign,left_adverserial, right_adverserial,length=10):
    a = np.array_split(benign,len(benign)/length)
    b = np.array_split(left_adverserial,len(left_adverserial)/length)
    c = np.array_split(right_adverserial,len(right_adverserial)/length)    
    return np.concatenate([a,b,c]),np.concatenate([[0] * len(a) ,[1] * (len(b) + len(c))])

def classifier(sample,tr=0.01):
    global benign_sender_receiver
    #print(sample)
    return 0 if stats.ks_2samp(benign_sender_receiver,sample)[1] > tr else 1

def fix(circles):
    r0 = circles[0][2]
    x1 = circles[1][0]
    y1 = circles[1][1]
    r1 = circles[1][2]
    x2 = circles[2][0]
    y2 = circles[2][1]
    r2 = circles[2][2]
    x = -1*((math.pow(r0,2)*y1)-(math.pow(r0,2)*y2)+(math.pow(r1,2)*y2)-(math.pow(r2,2)*y1)-(math.pow(x1,2)*y2)+(math.pow(x2,2)*y1)-(math.pow(y1,2)*y2)+(math.pow(y2,2)*y1))/(2 *(x1*y2-x2*y1))
    y = (math.pow(r0,2)*x1-math.pow(r0,2)*x2+math.pow(r1,2)*x2-math.pow(r2,2)*x1-math.pow(x1,2)*x2+math.pow(x2,2)*x1+math.pow(y2,2)*x1+math.pow(y1,2)*x2)/(2*(x1*y2-x2*y1))
    return (x,y)


def find_label(clf,x,rate=15):
    r0_a0 = np.array([lognormal_loss(p_tx=x,d=norm(r_0-a_0),sigma=1.0) for i in range(10000)])
    e=0
    for ii in range(rate):
        e+=clf.predict([np.array(random.sample(r0_a0.tolist(),10)).reshape(-1,1)])[0]
        
    return 1-e/rate


def find_label_r(clf,x,rate=15):
    r0_a0 = np.array([lognormal_loss(p_tx=x,d=norm(r_0-a_0),sigma=1.0) for i in range(10000)])
    e=0
    for ii in range(rate):
        e+=clf.predict([np.array(random.sample(r0_a0.tolist(),10)).reshape(-1,1)])[0]
        
    return 1-e/rate
