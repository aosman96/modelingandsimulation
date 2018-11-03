# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 18:24:16 2018

@author: ahmos
"""

import sys
import os
import subprocess
import shutil
import re 
import csv
import webbrowser
import argparse
import numpy as np
from time import sleep



class Component(object):
    """docstring for Component"""
    def __init__(self,Type,firstNode,SecondNode,value,intialvalue):
        self.firstNode = firstNode
        self.secondNode=SecondNode
        self.value=value
        self.Type=Type
        self.intialvalue = intialvalue
file  = open('testcases/2.txt')
index = 0
h = -1
Nodes= set()
Vsrcsreal= set()
Vsrcs = list()
Capictors = list()
Inductors = list()
InductorsReal = set()
ind_index=0
secondvariable=0
Components = []
for line in file:
    if(index == 0):
        h = float(line)
        index = index+1
        continue
    if(index == 1 ):
        secondvariable = float(line)
        index = index+1
        continue
    
    splited = line.split(" ")
    firstNode = re.search(r'\d+',splited[1]).group()
    firstNodeNum =  int(firstNode)
    secondNode = re.search(r'\d+',splited[2]).group()
    secondNodeNum =  int(secondNode)
    Nodes.add(firstNodeNum)
    Nodes.add(secondNodeNum)
   # print(firstNodeNum,secondNodeNum)
    value = float(splited[3])
    intialvalue = float(splited[4])
    Type = splited[0]+str(len(Vsrcs))
    if(  "Vsrc" in Type ):
        Vsrcsreal.add(Type)
        Vsrcs.append(value)
    if("I" in Type):
        ss = "L"+str(ind_index)
        ind_index+=1
        InductorsReal.add(ss)
        Vsrcs.append(-1 * value /h * intialvalue)
    Components.append(Component(Type,firstNodeNum,secondNodeNum,value,intialvalue))
#print(Nodes)
#print(Vsrcs)

def CreateLhsMatrix(Compnents,n,m):
    #print("the square matrix is ",n+m)
    ind=0
    Matrix = np.zeros((n+m,n+m))
    for comp in Components:
        if("R" in comp.Type):
           # print("True -=========== R")
           # print("indices is " ,comp.firstNode,comp.secondNode,comp.value  )
            if(comp.firstNode !=0):
                Matrix[comp.firstNode-1][comp.firstNode-1]+= 1/comp.value
               
            if(comp.secondNode !=0): 
                Matrix[comp.secondNode-1][comp.secondNode-1]+= 1/comp.value
            
            if(comp.secondNode !=0 and comp.firstNode !=0):
                Matrix[comp.secondNode-1][comp.firstNode-1]+=   (1/(-1* comp.value))
                Matrix[comp.firstNode-1][comp.secondNode-1]+=   (1/( -1*comp.value))
            
        elif("Vsrc" in comp.Type):
            ks = re.search(r'\d+',comp.Type).group()
            k =  int(ks)
            postive = comp.firstNode
            negative = comp.secondNode
            if(postive !=0):
                Matrix[postive-1][int(k+n)]= 1
                Matrix[int(k+n)][postive-1] = 1
            if(negative !=0 ):
                Matrix[int(negative-1)][int(k+n)]= -1 
                Matrix[int(k+n)][int(negative-1)] = -1  
                
                
        elif("C" in comp.Type):
            value = h/comp.value
            if(comp.firstNode !=0):
                Matrix[comp.firstNode-1][comp.firstNode-1]+= 1/value
               
            if(comp.secondNode !=0):
                Matrix[comp.secondNode-1][comp.secondNode-1]+= 1/value
            
            if(comp.secondNode !=0 and comp.firstNode !=0):
                Matrix[comp.secondNode-1][comp.firstNode-1]+=   (1/(-1* value))
                Matrix[comp.firstNode-1][comp.secondNode-1]+=   (1/( -1*value))
    
        elif("I" in comp.Type):
            ks = re.search(r'\d+',comp.Type).group()
            k =  int(ks)
            postive = comp.firstNode
            negative = comp.secondNode
            if(postive !=0):
                Matrix[postive-1][int(k+n)]= 1
                Matrix[int(k+n)][postive-1] = 1
            if(negative !=0 ):
                Matrix[int(negative-1)][int(k+n)]= -1 
                Matrix[int(k+n)][int(negative-1)] = -1 
            ind+=1       
            Matrix[int(n+ind)][int(n+ind)]=-1 * comp.value/h  
    return Matrix
            
            
def CreateRhsMatrix(Components,n,m,Vsrcs,z,iteration):
    ind=0
    Matrix = np.zeros((n+m,1))
   # for i in range(m):
     #   value=Vsrcs.pop()  
     #   Matrix[n+i][0]=value
    #print("comp = ",Components)
    for comp in Components:
        if("Vsrc" in comp.Type):
             ks = re.search(r'\d+',comp.Type).group()
             k =  int(ks)
             Matrix[n+k]=Vsrcs[k]
        elif("I" in comp.Type):
            ks = re.search(r'\d+',comp.Type).group()
            k =  int(ks)
            if(iteration !=h):
                comp.intialvalue = z[n+k]
            Matrix[n+k]= -1 * comp.value/h * comp.intialvalue
            ind+=1
        elif("Isrc" in comp.Type):
          #  print("isrc found")
            if(comp.firstNode !=0 ):
               Matrix[comp.firstNode-1]+= comp.value
            if(comp.secondNode != 0 ):
              Matrix[comp.secondNode-1]+= -1*comp.value
        elif("C" in comp.Type):
          #  print("we Found C ============================================")
            if(iteration!=h):
                print("we have new value")
                comp.intialvalue = z[comp.firstNode-1]-z[comp.secondNode-1]
            if(comp.firstNode !=0 ):
               Matrix[comp.firstNode-1]+= comp.value/h * comp.intialvalue
            if(comp.secondNode != 0 ):
              Matrix[comp.secondNode-1]+=-1* comp.value/h * comp.intialvalue

            
    return Matrix

X = np.zeros((int(len(Nodes))-1+int(len(Vsrcs)),1))
it=0;
iti=0;
Vsrcsold= list.copy(Vsrcs)
Results=[]
while it!=secondvariable:
    iti+=1
    it = it+1
    Vsrcs = list.copy(Vsrcsold)
    A= CreateLhsMatrix(Components,int(len(Nodes))-1,int(len(Vsrcs)))
    Z= CreateRhsMatrix(Components,int(len(Nodes))-1,int(len(Vsrcs)),Vsrcs,X,it)
    #print("the Z is " ,Z)
    #print("A matrix is = ",  A)
    #print("Z matrix is = ",  Z)
    try:
        inverse = np.linalg.inv(A)    
       # print(inverse)    
        X= np.matmul(inverse,Z)
        Results.append(X)
        print("the output of iteration", it , "is = ",X)
    except np.linalg.LinAlgError as err:
        print("Error in A" , err)
            
            # Not invertible. Skip this one.
        pass

outputFile = open("Results.txt","w+")
R =np.array(Results)
Nodes.pop()
for i in range(int(len(Nodes))+int(len(Vsrcs))):
    step = h
    if(len(Nodes)!=0):
        outputFile.writelines("V"+str(Nodes.pop())+"\n")
    elif(len(Vsrcsreal)!=0):
        outputFile.writelines("I"+str(Vsrcsreal.pop())+"\n")
    elif(len(InductorsReal)!=0):
        outputFile.writelines("I_"+str(InductorsReal.pop())+"\n")
    for j in range(iti):
        print(str(R[j][i]))
        string_toprint = str(step)+" "+str(R[j][i])+"\n"
        string_toprint = string_toprint.replace("[","")
        string_toprint = string_toprint.replace("]","")
        outputFile.writelines(string_toprint)
        step+=h
    outputFile.write("\n")    
outputFile.close()