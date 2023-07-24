from tkinter import *
import matplotlib.pyplot as plt
from DP import preparation as DP
from DataPrep import createPopulation
from SE import selection as SE
from Evolution import evolve

class gui:

    def GUI():
        global entry1, entry2, truck, targetValue
        window= Tk()
        window.title('VRP')
        window.geometry('400x300')
        window.resizable(False,False)

        Label(window, text="Start Point", fg= 'blue',font=("Arial", 17)).place(x=160, y=20)

        Label(window, text="X :", font=("bold", 10)).place(x=120, y=70)

        Label(window, text="Y :", font=("bold", 10)).place(x=120, y=120)

        Label(window, text="Number of Trucks:", font=("bold", 10)).place(x=12, y=170)

        Label(window, text="Expected Value :", font=("bold", 10)).place(x=15, y=220)

        entry1 = Entry (window)
        entry1.place(x=150, y=70)

        entry2 = Entry (window)
        entry2.place(x=150, y=120)

        truck = Entry (window)
        truck.place(x=150, y=170)

        targetValue = Entry (window)
        targetValue.place(x=150, y=220)
        Button(window, text='Next', relief="flat", bg='blue', fg='white', font=("bold"), command=gui.run).place(x=190, y=250)

        window.mainloop()

    def create_line(coordinates, n):
        lineColor = ["red", "blue", "yellow", "green", "black", "brown", "cyan", "magenta"]
        for i in range(len(coordinates)-1):
            plt.plot([coordinates[i][0],coordinates[i+1][0]], [coordinates[i][1], coordinates[i+1][1]], color=lineColor[n])
            plt.pause(0.00001)

    def create_map(generations, bestPath):
        m = DP.create_dictionary()
        lineColor = ["red", "blue", "yellow", "green", "black", "brown", "cyan", "magenta"]
        coordinates = []
        coordinates.append(m["Start"])
        c=1
        n=0
        for str in generations:
                    
            str+=" "
            plt.cla()
            plt.title("Locations", fontsize=20)
            plt.scatter(coordinates[0][0], coordinates[0][1],s=100,color=lineColor[0])
            plt.annotate("Start", (coordinates[0][0], coordinates[0][1]+10))
            plt.xlabel("X", fontweight='bold')
            plt.ylabel("Y", fontweight='bold')
            for x in str:

                if(x==" "):
                    coordinates.append(m["Start"])
                    gui.create_line(coordinates, n)
                    coordinates = []
                    coordinates.append(m["Start"])
                    n+=1
                    if n==len(lineColor):
                        n=0
                    c=1
                else:
                    coordinates.append(m[x])
                    plt.scatter(coordinates[c][0], coordinates[c][1],s=40,color=lineColor[n])
                    plt.annotate(x, (coordinates[c][0], coordinates[c][1]+10))
                    c+=1
            plt.pause(1)

        bestPath+= " "
        plt.show()
        plt.title("Optimal Solution", fontsize=20)
        plt.scatter(coordinates[0][0], coordinates[0][1],s=100,color=lineColor[0])
        plt.annotate("Start", (coordinates[0][0], coordinates[0][1]+10))
        plt.xlabel("X", fontweight='bold')
        plt.ylabel("Y", fontweight='bold')

        for z in bestPath:
                
            if(z==" "):
                coordinates.append(m["Start"])
                gui.create_line(coordinates, n)
                coordinates = []
                coordinates.append(m["Start"])
                n+=1
                if n==len(lineColor):
                    n=0
                c=1
            else:
                coordinates.append(m[z])
                plt.scatter(coordinates[c][0], coordinates[c][1],s=40,color=lineColor[n])
                plt.annotate(z, (coordinates[c][0], coordinates[c][1]+10))
                c+=1

        return coordinates

    def run():
        truckNum = int(truck.get())
        x=int(entry1.get())
        y=int(entry2.get())

        DP(x, y)

        population = createPopulation(truckNum)
        
        e = evolve(population)
        generations = []
        maxlist = {}
        for i in range(10):
            temp = e
            ft = DP.calc_fitness(temp, int(targetValue.get()))
            _2d = [temp,ft]
            e = evolve(_2d)
            dict = SE.sort(_2d)
            f = DP.represent(dict)
            maxlist[f[0][0]]=f[1][0]
                
            generations.append(f[1][0])
            print(f[0][0], " ", f[1][0])

        m = max(maxlist.keys())
        print("Optimal Solution: " , m , " " , maxlist[m])

        gui.create_map(generations, maxlist[m])