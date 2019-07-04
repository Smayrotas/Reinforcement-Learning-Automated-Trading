import gym
from alpha_vantage import foreignexchange, techindicators,cryptocurrencies
import numpy as np
from gym.utils import seeding
from gym import spaces
import agent
import utils
from matplotlib import pyplot as plt

#Check Out what gym.Env should be returning


'''FOCUS ON ONLY ONE TRADE DECISIONS'''

'''
Primary Rules for trading:

1. Only trading ONE Ticker
2. Only one position can be opened at any single point in time
3. Can only hold long and no short

--> All these parameters can be changed later when I have more experience in machine learning
'''

'''
-->Things to do over the next few days
1. Update the capital with profit/los

2. Work on Optimising the Reward Function

'''

class tradingEnvironment(gym.Env):


    def __init__(self,trainData,cashInHand,uPnL):

        self.n_Assets=1



        env = gym.make('Copy-v0')
        env.reset()

        self.y = list()
        self.x = list()

        self.trainData=trainData
        self.currentStep=0
        self.maxStep=50000

        self.currency_Price=None


        self.initValue=cashInHand
        self.initPnL=uPnL

        self.unrealizedPnl=self.initPnL

        self.tradesInfo=np.zeros((self.maxStep*2,5)) #Array with ID|Ticker Symbol|BOUGHT PRICE|SOLD PRICE|VOLUME in the future this can have quantity as well collumns

        '''
        Actions: Buy, Sell, Hold
        
        Real Action Environment:3*noOfStocksOwned
        
        --> Maybe think about the states more
        
        States: Long, Neutral
        
        Real States Could be --> [Number of Stocks Owned, Stock Prices, Cash in Hand]
        '''

        self.openPositions=0


        states=['Neutral','Long']
        actions=['Buy','Sell','Hold']

        self.observation_space=spaces.Discrete(len(states))
        self.action_space=spaces.Discrete(len(actions))

        self._seed()


    def _step(self, action):

        self.updatePositions(action)
        self.currency_Price=self.trainData[self.currentStep]


        observation=self.observeCurrentState()
        self.updateInfoTable(action)
        reward=self.updatePnl()


        self.x.append(self.currentStep)
        self.y.append(reward)

        info={'unrealized PnL':self.unrealizedPnl}
        if self.currentStep==self.maxStep:
            done = True
        else:
            done=False
            self.currentStep+=1

        self.agent.replay(observation, reward, done, info)

        return observation,reward,done,info

    def _reset(self):
        self.openPositions=0
        self.x=list()
        self.y = list()
        self.currentStep=0
        self.updateInfoTable('Delete')
        return self.observeCurrentState()

    def _seed(self, seed=None):
        seeds=seeding.np_random(seed)
        return [seeds]

    def _render(self):
        return None

    def updateInfoTable(self,action):

        if action=='Delete':
            self.tradesInfo=np.zeros((self.maxStep*2,5))
        else:
            self.tradesInfo[self.currentStep, 0] = self.currentStep + 1

            if action==2:
                return
            elif action==0:
                self.tradesInfo[self.currentStep, 2] = self.currency_Price
            elif action==1:
                self.tradesInfo[self.currentStep, 3] = self.currency_Price
            self.tradesInfo[self.currentStep, 4] = 100000
            '''Lets assume volume is constant at 100 for now'''
        return

    def updatePositions(self,action):

        try:
            if (action==0):
                self.openPositions+=1
            elif (action==1):
                self.openPositions+=-1
        except:
            print('a')

    def rememberAgent(self,agent):
        self.agent=agent


    def updatePnl(self):

        ids=self.tradesInfo[:,0]
        a=len(np.nonzero(ids)[0])-1
        Volume=self.tradesInfo[a,4]

        PreviousBoughPrice=self.tradesInfo[a-1,2]
        CurrentSellPrice=self.tradesInfo[a,3]

        if  (PreviousBoughPrice is not 0) and (CurrentSellPrice is not 0) and (a is not 0):
            updatedPnl = Volume * (CurrentSellPrice- PreviousBoughPrice)
            return updatedPnl

        elif self.tradesInfo[a-1,3] is not 0:
           return 0


    def observeCurrentState(self):
        '''States  Neutral(0) or Long(1) thus return ALL actions for that state'''
        Q=self.agent.Q

        try:
            return Q[:,self.openPositions], self.openPositions
        except:
            return 0



