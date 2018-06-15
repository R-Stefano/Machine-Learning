import numpy as np
import random
from tkinter import *
from tkinter import messagebox
import time 

class drawer():
    def __init__(self, grid, agent, goal):
        self.window=Tk()
        #don't show it when createdm remove from the screen
        self.window.withdraw()
        self.startAgentPos=agent
        self.goal=goal
        self.window.title("Maze")
        self.width=500
        self.height=500
        self.canvas = Canvas(self.window, width=self.width, height=self.height, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.rows = grid.shape[0]
        self.columns = grid.shape[1]
        self.cellwidth = self.width/self.columns
        self.cellheight = self.height/self.rows

        #store the shapes in a dictionary where the key are the coordinates of the shape
        self.rect = {}
        for row in range(self.columns):
            for column in range(self.rows):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                if agent[0]==row and agent[1]==column:
                    color="green"
                elif goal[0]==row and goal[1]==column:
                    color="blue"
                elif grid[row][column]==1:
                    color="white"
                elif grid[row][column]==2:
                    color="red"
                else:
                    color="black"
                self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill=color, tags="rect")
        
    def redraw(self, agentNow, agentPrev):
        #reverse the withdraw command
        self.window.deiconify() 
        #remove prev agent green block
        item_id = self.rect[agentPrev[0],agentPrev[1]]
        self.canvas.itemconfig(item_id, fill="white")
        #set the new one
        item_id = self.rect[agentNow[0],agentNow[1]]
        self.canvas.itemconfig(item_id, fill="green")
        self.window.update()
        time.sleep(0.3)
    
    def reset(self,agentPrev):
        item_id = self.rect[agentPrev[0],agentPrev[1]]
        self.canvas.itemconfig(item_id, fill="white")

    def showEnv(self):
        #reverse the withdraw command
        self.window.deiconify() 
        messagebox.showinfo("System", "Continue?")
        self.window.withdraw()

    def displayOptimalPath(self, qtable, ncolumns):
        status=True
        pathState=[self.startAgentPos[0],self.startAgentPos[1]]
        while status:
            row=pathState[0]*ncolumns
            column=pathState[1]
            flatted=row+column

            #retrieve which action is best in a state
            bestNextState=np.argmax(qtable[flatted,:])
            
            #up
            if bestNextState==0:
                pathState[0]-=1
            #down
            elif bestNextState==1:
                pathState[0]+=1
            #left
            elif bestNextState==2:
                pathState[1]-=1
            #right
            else:
                pathState[1]+=1

            if pathState[0]==self.goal[0] and pathState[1]==self.goal[1] :
                status=False
            else:            
                item_id = self.rect[pathState[0],pathState[1]]
                self.canvas.itemconfig(item_id, fill="yellow")
        
        self.window.mainloop()

class optimalPathDrawer():
    def __init__(self, grid, agent, goal):
        self.window=Tk()
        #don't show it when createdm remove from the screen
        self.window.withdraw()
        self.startAgentPos=agent
        self.goal=goal
        self.window.title("Optimal path")
        self.width=500
        self.height=500
        self.canvas = Canvas(self.window, width=self.width, height=self.height, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.rows = grid.shape[0]
        self.columns = grid.shape[1]
        self.cellwidth = self.width/self.columns
        self.cellheight = self.height/self.rows

        #store the shapes in a dictionary where the key are the coordinates of the shape
        self.rect = {}
        for row in range(self.columns):
            for column in range(self.rows):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                if agent[0]==row and agent[1]==column:
                    color="green"
                elif goal[0]==row and goal[1]==column:
                    color="blue"
                elif grid[row][column]==1:
                    color="white"
                elif grid[row][column]==2:
                    color="red"
                else:
                    color="black"
                self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill=color, tags="rect")

    def reset(self):
        #convert yellow blocks to white
        for row in range(self.columns):
            for column in range(self.rows):
                item_id = self.rect[row, column]
                color=self.canvas.itemcget(item_id, "fill")
                if color=="yellow":
                    self.canvas.itemconfig(item_id, fill="white")
        
        self.window.withdraw()
    
    def displayOptimalPath(self, qtable, ncolumns, nrows, epoch):
        status=True
        pathState=[self.startAgentPos[0],self.startAgentPos[1]]
        while status:
            row=pathState[0]*ncolumns
            column=pathState[1]
            flatted=row+column

            #retrieve which action is best in a state
            bestNextState=np.argmax(qtable[flatted,:])
            
            #up
            if bestNextState==0:
                pathState[0]-=1
            #down
            elif bestNextState==1:
                pathState[0]+=1
            #left
            elif bestNextState==2:
                pathState[1]-=1
            #right
            else:
                pathState[1]+=1

            #
            if pathState[0]<0:
                pathState[0]=0
            elif pathState[0]>=nrows:
                pathState[0]=nrows-1

            if pathState[1]<0:
                pathState[1]=0
            elif pathState[1]>=ncolumns:
                pathState[1]=ncolumns-1
            

            if pathState[0]==self.goal[0] and pathState[1]==self.goal[1] :
                status=False
            else:            
                item_id = self.rect[pathState[0],pathState[1]]
                color=self.canvas.itemcget(item_id, "fill")
                #the agent is in a loop
                if color=="yellow":
                    status=False
                else:
                    self.canvas.itemconfig(item_id, fill="yellow")

        #reverse the withdraw command
        self.window.deiconify()
        text="Optimal path after " + str(epoch) +  " episodes. \nContinue with training?"
        messagebox.showinfo("System", text)
        self.reset()



#goal is -1, empty block is 1, wall is 0, mortal block is 2
class maze():
    
    def __init__(self, maze, timestepReward, finalReward, limitTimeStep, badReward=0):
        #convert the list to a np array
        self.maze=np.array(maze)
        #set the agent position to the top-left block
        self.agent=[0,0]
        #store the previous agent position
        self.prevAgentPosition=self.agent
        #Find the element with value -1, take its index and store it in form [x,y]
        self.goal=np.argwhere(self.maze==-1).reshape(-1)
        #store the reward obtained at each timestep
        self.reward=timestepReward
        #store the reward obtained when goal block is reached
        self.finalReward=finalReward
        #If set, store the reward obtained to finish in a mortal block
        self.badReward=badReward
        #store the possible actions
        self.actions=["UP","DOWN","LEFT","RIGHT"]
        #set a limit timestep
        self.maxTimestep=limitTimeStep
        self.timestep=0
        #instantiate an object for the UI
        self.display=drawer(self.maze, self.agent, self.goal)
        #instantiate object to show the optimal path
        self.optimalDisplay=optimalPathDrawer(self.maze, self.agent, self.goal)
    
    def reset(self):
        self.display.reset(self.prevAgentPosition)
        self.agent=[0,0]
        self.prevAgentPosition=self.agent
        self.timestep=0

        flatted=self.flatPosition(self.agent)
        return flatted

    #the action parameter is a number between 0 and 3
    def step(self, action):
        self.prevAgentPosition=self.agent.copy()
        #retrieve the action based on the index passed when this method has been called
        actionName=self.actions[action]
        if actionName=="LEFT":
            #take y coord of the agent
            agentPosition=self.agent[1]
            nextPosition=agentPosition-1
            #the agent is on the top line or the next position is a wall, so not move
            if not (nextPosition<0 or self.maze[self.agent[0]][nextPosition]==0):
                self.agent[1]=nextPosition
        elif actionName=="RIGHT":
            #take y coord of the agent
            agentPosition=self.agent[1]
            nextPosition=agentPosition+1
            #the agent is on the bottom line or the next position is a wall, so not move
            if not(nextPosition>self.maze.shape[1]-1 or self.maze[self.agent[0]][nextPosition]==0):
                self.agent[1]=nextPosition
        elif actionName=="UP":
            #take x coord of the agent
            agentPosition=self.agent[0]
            nextPosition=agentPosition-1
            #the agent is on the most right line or the next position is a wall, so not move
            if not(nextPosition<0 or self.maze[nextPosition][self.agent[1]]==0):
                self.agent[0]=nextPosition
        else:
            #take x coord of the agent
            agentPosition=self.agent[0]
            nextPosition=agentPosition+1
            #the agent is on the most left line or the next position is a wall, so not move
            if not(nextPosition>self.maze.shape[0]-1 or self.maze[nextPosition][self.agent[1]]==0):
                self.agent[0]=nextPosition

        self.timestep+=1

        #if the agent didn't reach the goal in the limit timesteps
        if(self.timestep>self.maxTimestep):
            flatted=self.flatPosition(self.agent)
            return flatted, self.badReward, True
        #check if the agent reached the end of the maze
        elif self.agent[0]==self.goal[0] and self.agent[1]==self.goal[1]:
            flatted=self.flatPosition(self.agent)
            return flatted,self.finalReward, True
        #agent finished in mortal block, game finished
        elif self.maze[self.agent[0]][self.agent[1]]==2:
            flatted=self.flatPosition(self.agent)
            return flatted,self.badReward, True
        else:
            flatted=self.flatPosition(self.agent)
            #return next state flatted, reward, isGameFinished
            return flatted, self.reward, False
    
    #display the maze after the agent moved
    def observe(self):
        self.display.redraw(self.agent, self.prevAgentPosition)

    #display the path that the agent follow based on the qtable passed as parameter
    def displayOptimalPath(self, table, epoch):
        self.optimalDisplay.displayOptimalPath(table, self.maze.shape[1], self.maze.shape[0], epoch)

    ##########HELPFUL FUNCTIONS##############

    #convert agent position to flat array es. [2,1] (if the array is 7x7) 2*7 + 1=15
    def flatPosition(self, agent):
            row=self.agent[0]*self.maze.shape[1]
            column=self.agent[1]
            flatted=row+column
            return flatted

    #return the number of actions
    def getNActions(self):
        return len(self.actions)

    def changeEnv(self):
        self.maze[3][0]=1

    #return the number of blocks in the maze
    def getNStates(self):
        return self.maze.shape[0] * self.maze.shape[1]

    #used to show the maze structure
    def showEnv(self):
        #display until it is closed
        self.display.showEnv()
    