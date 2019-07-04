import utils, agent
import environment as env
import numpy as np
import argparse
import matplotlib
from matplotlib import pyplot as plt


if __name__== '__main__':
    parser=argparse.ArgumentParser()

    parser.add_argument('-e', '--episode', type=int, default=2000,
                      help='number of episode to run')

    parser.add_argument('-i','--investInit',type=int, default=1000,
                        help='initial to invest')

    parser.add_argument('-u', '--unrealizedPnl', type=int, default=0,
                        help='starting unrealized pnl')

    date, bid, ask=utils.getData()
    spread=(bid+ask)/2
    trainData=np.array(spread)

    args = parser.parse_args()

    initToInvest=args.investInit
    unrealizedPnl=args.unrealizedPnl


    env=env.tradingEnvironment(trainData,initToInvest,unrealizedPnl)

    state_size = env.observation_space.n
    action_size = env.action_space.n

    ag=agent.agent(state_size,action_size)
    env.rememberAgent(ag)


    #Assuming current state with no positions!


    for e_episode in range(args.episode):

        fig = plt.figure(1)
        fig.show()
        fig.canvas.draw()


        observation=env._reset()

        for t in range(100000):
            initialState, openPositions = env.observeCurrentState()

            env._render()


            actResult=ag.act(initialState, openPositions)

            nextAction=actResult[1]

            observation, reward, done, info= env._step(nextAction)

            '''env.animate(reward)'''

            ag.replay(observation,reward,done,info)
            env.rememberAgent(ag)

            if done:
                a=env.y
                b=env.x
                lis=a
                comb=[a,lis]
                c=list(filter(lambda a: a!=0 and a>=0,a))
                a=list(a)
                d=list()

                for i in a:
                    ind=a.index(i)
                    if (abs(i)!=0 and abs(i)>=0):
                        d.append(ind)
                        a[ind]=-1
                lenx=len(d)
                leny = len(c)
                plt.scatter(d,c)
                plt.show(block=False)
                print('Episode Finished {} timesteps'.format(t+1))
                break
        break
    print (ag.Q)
    env.close()





