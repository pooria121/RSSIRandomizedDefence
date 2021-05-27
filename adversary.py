

class Adversary:
    query_issued = 30
    
    def __init__(self,X,y,clf,eps=0.01):
        self.eps =eps
        self.clf=clf
        self.X = np.array(X)
        self.y = np.array(y)
        self.X_plot = np.array(np.linspace(X.min(),X.max())).reshape(-1,1)
        self.build_grp()
        
    def build_grp(self):

        gp_kernel = RBF(length_scale=2.0, length_scale_bounds=(0.0, 10.0))  
        # ExpSineSquared(1.0, 5.0, periodicity_bounds=(1e-2, 1e1))  + WhiteKernel(1e-1)
        #kernel = #ConstantKernel(constant_value=1.0, constant_value_bounds=(0.0, 10.0)) * RBF(length_scale=0.5, length_scale_bounds=(0.0, 10.0)) + RBF(length_scale=2.0, length_scale_bounds=(0.0, 10.0))

        grp = GaussianProcessRegressor(kernel=gp_kernel)
        grp.fit(self.X, self.y)
        self.grp=grp

    def graph_belief(self):
        y_gpr, y_std = self.grp.predict(self.X_plot, return_std=True)
        print(y_std)
        plt.plot(self.X_plot,y_gpr,label='Interpolation')
        plt.scatter(self.X,self.y,label='Queried Point')
        plt.fill_between(self.X_plot[:, 0], y_gpr - y_std , y_gpr + y_std , color='darkorange',
                         alpha=0.2,label='Uncertainty')
        plt.legend(loc='lower right')
        plt.ylabel('Probability of Evasion')
        plt.xlabel('TX Power (mW)')
        #plt.ylim([0.7,1.05])
        plt.show()
    def found(self):
        found = np.where(self.y >= 1.0-self.eps )[0]
        if len(found):
            return self.X[found[0]],self.y[found[0]]
        else:
            return False
        
    def next(self):
        y_gpr,y_std = self.grp.predict(self.X_plot,return_std=True)
        x= self.X_plot[np.where(y_std == y_std.max())[0][0]]
        e= self.find_label(x)    
        self.X=np.append(self.X,[[x]]).reshape(-1,1)
        self.y=np.append(self.y,[e])
        self.build_grp()

    def find_label(self,x):
        r0_a0 = np.array([lognormal_loss(p_tx=x,d=norm(r_0-a_0),sigma=1.0) for i in range(10000)])
        e=0
        for ii in range(15):
            e+=self.clf.predict([np.array(random.sample(r0_a0.tolist(),10)).reshape(-1,1)])[0]
            self.query_issued+=1
        return 1-e/15
    

