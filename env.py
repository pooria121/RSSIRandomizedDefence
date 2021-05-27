
class SimEnviroment:

    def __init__(self):
        #default transmit power by nodes in mW
        self.p_tx = 15

        #the location of the sender
        self.s_0 = np.array([0,8])

        #the location of the receiver
        self.r_0 = np.array([10,0])

        #three probing location of the adversary
        self.a_0 = np.array([0,0])
        self.a_1 = np.array([-1,0])
        self.a_2 = np.array([0,-2])


        #how really r0 preceive s0 and a0
        self.r0_s0 = np.array([lognormal_loss(p_tx=p_tx,d=norm(r_0-s_0),sigma=1.0) for i in range(10000)])
        self.r0_a00= np.array([lognormal_loss(p_tx=p_tx,d=norm(r_0-a_0),sigma=1.0) for i in range(10000)])
        
        find_adverserial_fix()
    
    
    
    def graph_receiver_percetion(self):
        #what reciever register when adversary transmit
        r0_a0_min = np.array([lognormal_loss(p_tx=self.adversary_spoof_tx_min,d=norm(self.r_0-self.a_0),sigma=1.0) for i in range(10000)])
        
        #what reciever register when adversary transmit
        r0_a0_max = np.array([lognormal_loss(p_tx=self.adversary_spoof_tx_max,d=norm(self.r_0-self.a_0),sigma=1.0) for i in range(10000)])
        
         #what reciever register when adversary transmit
        r0_a0_mean = np.array([lognormal_loss(p_tx=self.adversary_spoof_tx_mean,d=norm(self.r_0-self.a_0),sigma=1.0) for i in range(10000)])
        
        plt.hist(self.r0_s0,bins=100, alpha=0.4,label='Sender') 
        plt.hist(r0_a0_mean,bins=100, alpha=0.4,label='Adversary(Mean)')
        plt.hist(r0_a0_max,bins=100, alpha=0.4,label='Adversary(Max)')
        plt.hist(r0_a0_min,bins=100, alpha=0.4,label='Adversary(Min)')
        plt.legend(loc='upper right')
        plt.show()

        
    def adversary_tx_range_values(self):
        return {'min_tx' : self.adversary_spoof_tx_min,
                'max_tx' : self.adversary_spoof_tx_max,
                'mean_tx': self.adversary_spoof_tx_mean}
        
    def find_adverserial_fix(self):
        #recording adversery captures from the three location into 3 indecies of a list
        a_s = [np.array([lognormal_loss(p_tx=self.p_tx,d=norm(self.a_0-self.s_0),sigma=1.0) for i in range(10000)]),
               np.array([lognormal_loss(p_tx=self.p_tx,d=norm(self.a_1-self.s_0),sigma=1.0) for i in range(10000)]),
               np.array([lognormal_loss(p_tx=self.p_tx,d=norm(self.a_2-self.s_0),sigma=1.0) for i in range(10000)])]
        
        a_r = [np.array([lognormal_loss(p_tx=self.p_tx,d=norm(self.a_0-self.r_0),sigma=1.0) for i in range(10000)]),
               np.array([lognormal_loss(p_tx=self.p_tx,d=norm(self.a_1-self.r_0),sigma=1.0) for i in range(10000)]),
               np.array([lognormal_loss(p_tx=self.p_tx,d=norm(self.a_2-self.r_0),sigma=1.0) for i in range(10000)])]


        #find fix on the sender and the receiver 
        a_s_circles_min = [np.append(self.a_0,[distance_lognormal_loss(self.p_tx,self.a_s[0].mean() + 3*self.a_s[0].std())]),
                           np.append(self.a_1,[distance_lognormal_loss(self.p_tx,self.a_s[1].mean() + 3*self.a_s[1].std())]),
                           np.append(self.a_2,[distance_lognormal_loss(self.p_tx,self.a_s[2].mean() + 3*self.a_s[2].std())])]
        s_fix_min = np.array(fix(a_s_circles_min))

        a_r_circles_min = [np.append(self.a_0,[distance_lognormal_loss(self.p_tx,self.a_r[0].mean() + 3*self.a_r[0].std())]),
                           np.append(self.a_1,[distance_lognormal_loss(self.p_tx,self._r[1].mean() + 3*self.a_r[1].std())]),
                           np.append(self.a_2,[distance_lognormal_loss(self.p_tx,self.a_r[2].mean() + 3*self.a_r[2].std())])]
        r_fix_min = np.array(fix(a_r_circles_min))

        # find how r0 would percieve s0 in terms of RSSI value
        preceived_rssi_by_r0_min = lognormal_loss(self.p_tx, norm(s_fix_min-r_fix_min))

        #adjust power to emulate preceived RSSI value at estimate distance of the receiving node
        self.adversary_spoof_tx_min = power_transmit_lognormal_loss(preceived_rssi_by_r0_min,norm(r_fix_min))

        
        ###############################################################################################################################
        #find fix on the sender and the receiver
        a_s_circles_max = [np.append(self.a_0,[distance_lognormal_loss(self.p_tx,self.a_s[0].mean() - 2*self.a_s[0].std())]),
                            np.append(self.a_1,[distance_lognormal_loss(self.p_tx,self.a_s[1].mean() - 2*self.a_s[1].std())]),
                            np.append(self.a_2,[distance_lognormal_loss(self.p_tx,self.a_s[2].mean() - 2*self.a_s[2].std())])]
        s_fix_max = np.array(fix(a_s_circles_max))

        a_r_circles_max = [np.append(self.a_0,[distance_lognormal_loss(self.p_tx,self.a_r[0].mean() - 2*self.a_r[0].std())]),
                            np.append(self.a_1,[distance_lognormal_loss(self.p_tx,self.a_r[1].mean() - 2*self.a_r[1].std())]),
                            np.append(self.a_2,[distance_lognormal_loss(self.p_tx,self.a_r[2].mean() - 2*self.a_r[2].std())])]
        r_fix_max = np.array(fix(a_r_circles_max))

        # find how r0 would percieve s0 in terms of RSSI value
        preceived_rssi_by_r0_max = lognormal_loss(p_tx, norm(s_fix_max-r_fix_max))

        #adjust power to emulate preceived RSSI value at estimate distance of the receiving node
        self.adversary_spoof_tx_max = power_transmit_lognormal_loss(preceived_rssi_by_r0_max,norm(r_fix_max))

        ###############################################################################################################################
        a_s_circles_mean = [np.append(self.a_0,[distance_lognormal_loss(self.p_tx,self.a_s[0].mean())]),
                            np.append(self.a_1,[distance_lognormal_loss(self.p_tx,self.a_s[1].mean())]),
                            np.append(self.a_2,[distance_lognormal_loss(self.p_tx,self.a_s[2].mean())])]
        s_fix_mean = np.array(fix(a_s_circles_mean))

        a_r_circles_mean = [np.append(self.a_0,[distance_lognormal_loss(self.p_tx,self.a_r[0].mean())]),
                            np.append(self.a_1,[distance_lognormal_loss(self.p_tx,self.a_r[1].mean())]),
                            np.append(self.a_2,[distance_lognormal_loss(self.p_tx,self.a_r[2].mean())])]
        r_fix_mean = np.array(fix(a_r_circles_mean))

        # find how r0 would percieve s0 in terms of RSSI value
        #preceived_rssi_by_r0_mean = lognormal_loss(self.p_tx, norm(s_fix_mean-r_fix_mean))

        #adjust power to emulate preceived RSSI value at estimate distance of the receiving node
        self.adversary_spoof_tx_mean = power_transmit_lognormal_loss(preceived_rssi_by_r0_mean,norm(r_fix_mean))

       

        