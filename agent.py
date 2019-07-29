#One environment that can trade only GBPUSD exchange rates.
#It should take the action from the agent and return the reward along with the new state

from alpha_vantage import foreignexchange, techindicators,cryptocurrencies
import quandl
import random
import numpy as np
import math
import environment


class agent(object):

    def __init__(self,state_size,action_size):
        self.state_size=state_size
        self.action_size=action_size

        self.memory=[]

        self.Q=np.random.rand(action_size,state_size)

        print(self.Q)

        self.step=1

        self.epsilon=0.3
        self.epsilon_decay=0.4
        self.epsilon_min=0.1
        self.alpha=0.2
        self.interest_rate=1 #Try to download that from a database

    def remember(self,state, action, reward, next_state, done):
        self.memory.append(state, action, reward, next_state, done)


    def act(self,state, openPositions):

        if (np.random.rand()<=self.epsilon):

            if (openPositions>=1):
                Col=[np.random.randint(1,3,size=1)]

            else:

                Col = [np.random.randint(0,2,size=1)]

                if (Col[0]==1):
                    Col=[2]
        else:

            if (openPositions==1):
                number= np.max(state[1:3])
                Col = np.where(state == number)
            else:
                number= np.max([state[0],state[2]])
                Col = np.where(state == number)

        self.currentState=state
        self.nextAction=Col

        print (Col[0])
        b=Col[0]
        a=Col[0].__str__()[1:len(Col[0].__str__())-1]

        action = Col[0]

        if (len(a.__str__())>1):
            action=list(Col[:])[0][1]

        return (state,action)

    def replay(self,observation, reward, done, info):

        actions=observation[0]
        openPositions=observation[1]


        '''Could potentially extrct differnt features from paper Financial trading as a game'''
        #The function that governs everything
        currentState=np.where(self.Q==self.currentState[0])[0][0]

        self.Q[self.nextAction,currentState]=(1-self.alpha)*self.Q[self.nextAction,currentState]
        + self.alpha*(reward+math.exp(-self.interest_rate*self.step)*np.max(self.currentState))


        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        self.step+=1



