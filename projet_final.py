from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import ttk
import numpy as np
from numpy import sin ,cos,exp,log,sqrt
import matplotlib.pyplot as plt
from scipy.integrate import quad 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


root=Tk()
root.geometry("500x300")
root.title("Analyse Numérique")

c="blue"

def newWindow():
    window=Toplevel(root)
    window.geometry("480x300")
    window.title("Analyse Numérique")
    
    def callback():
        result = askcolor(title = "Tkinter Color Chooser")
        label_color=Label(window,text=result[1],font=('helvetica', 9, 'bold'))
        label_color.grid(row=6, column=1,pady=0, padx = 0)
        label_color.configure(fg = result[1])
        global c
        c=result[1]
    class RectangleG ( object ) :
        def __init__ (self , a , b , n , f, c ,lx , ly ) :
            self.a = a
            self.b = b
            self.x = np.linspace( a , b , n+1 )
            self.f = f
            self.n = n
            self.c = c
            self.lx = lx
            self.ly = ly
        def integrate ( self , f ) :
            x= self.x
            y= f( x )
            h = float( x[1] - x[0] )
            s = sum( y[ 0 : -1 ] )
            return h * s
        def Graph ( self , f ,c,lx,ly, resolution =1001) :
            xl = self.x
            yl = f(xl)
            xlist_fine =np.linspace( self.a , self.b , resolution )
            for i in range ( self.n ) :
                x_rect = [xl[ i ] , xl[ i ] , xl[ i + 1 ] , xl[i+1] , xl[ i ] ] # abscisses des sommets
                y_rect = [0 , yl[ i ] , yl[ i ] , 0 , 0 ] # ordonnees des sommets
                plt.plot ( x_rect , y_rect , 'r' )
            yflist_fine = f ( xlist_fine )
            plt.plot ( xlist_fine , yflist_fine,color=c )
            plt.plot(xl, yl,"bo")
            plt.xlabel (lx)
            plt.ylabel (ly)
            plt.title ( ' Methode des rectangles gauches' )
            plt.text( 0.5*( self.a+ self.b ) , f(self.b ) , 'I_{} ={:0.8f}'.format(self.n,self.integrate( f ) ) , fontsize =10 )

    class Trapezoidal(object):
        def __init__ (self , a , b , n , f, c ,lx , ly ) :
            self.a = a
            self.b = b
            self.x = np.linspace( a , b , n+1 )
            self.f = f
            self.n = n
            self.c = c
            self.lx = lx
            self.ly = ly
        def integrate(self,f):
            x=self.x
            y=f(x)
            h = float(x[1] - x[0])
            s = y[0] + y[-1] + 2.0*sum(y[1:-1])
            return h * s / 2.0
        def Graph ( self , f ,c,lx,ly, resolution =1001) :
            xl = self.x
            yl = f(xl)
            xlist_fine=np.linspace(self.a, self.b, resolution)
            for i in range(self.n):
                x_rect = [xl[i], xl[i], xl[i+1], xl[i+1], xl[i]] # abscisses des sommets
                y_rect = [0   , yl[i], yl[i+1]  , 0     , 0   ] # ordonnees des sommets
                plt.plot(x_rect, y_rect,"m")
            yflist_fine = f(xlist_fine)
            plt.plot(xlist_fine, yflist_fine,color=c)#plot de f(x)
            plt.plot(xl, yl,"cs")#point support
            plt.xlabel(lx)
            plt.ylabel (ly)
            plt.title ( ' Methode des Trapèzes' )
            plt.text( 0.5*( self.a+ self.b ) , f(self.b ) , 'I_{} ={:0.8f}'.format(self.n,self.integrate( f ) ) , fontsize =10 )

    class Milieu( object ) :
        def __init__ (self , a , b , n , f, c ,lx , ly ) :
            self.a = a
            self.b = b
            self.x = np.linspace( a , b , n+1 )
            self.f = f
            self.n = n
            self.c = c
            self.lx = lx
            self.ly = ly

        def integrate(self,f):
            h=float(self.b-self.a)/(self.n)
            sum1=0
            for i in range(self.n):
                sum1 += f(self.a+(i+1/2)*h)

            I = h*sum1
            return I

        def Graph ( self , f ,c,lx,ly, resolution =1001) :
            xl = self.x
            yl = f(xl)
            xlist_fine =np.linspace( self.a , self.b , resolution )
            for i in range ( self.n ) :
                mi=(xl[i]+xl[i+1])/2
                x_rect = [xl[i], xl[i], xl[i+1], xl[i+1], xl[i]] # abscisses des sommets
                y_rect = [0 , f(mi), f(mi) , 0 , 0 ] # ordonnees des sommets
                plt.plot ( x_rect , y_rect , 'r' )
                plt.plot(mi,f(mi), 'g*')
            yflist_fine = f ( xlist_fine )
            plt.plot ( xlist_fine , yflist_fine,color=c )
            #plt.plot(xl, yl,"bo")
            plt.xlabel ( lx )
            plt.ylabel ( ly )
            plt.title ( ' Methode de Milieux' )
            plt.text( 0.5*( self.a+ self.b ) , f(self.b ) , 'I_{} ={:0.8f}'.format(self.n,self.integrate( f ) ) , fontsize =10 )

    class Simpson(object):
        def __init__ (self , a , b , n , f, c ,lx , ly ) :
            self.a = a
            self.b = b
            self.x = np.linspace( a , b , n+1 )
            self.f = f
            self.n = n
            self.c = c
            self.lx = lx
            self.ly = ly
    
        def integrate(self,f):#calculer la somme ((b-a)/6*n)*[f(a)+2*sum(xi)+4*sum(mi)+f(b)]
            x=self.x #les points supports xi #x(0)=a-->x(n)=b
            y=f(x) #yi variable local y(o)=f(xo)-->y(n)
            h = float(x[1] - x[0])#pas h=(b-a)/2*n
            n = len(x) - 1#nombre subdivision
            if n % 2 == 1:#si le reste de la division =1 impaire
                n -= 1
            s = y[0] + y[n] + 4.0 * sum(y[1:-1:2]) + 2.0 * sum(y[2:-2:2])
            #y[1:-1:2] 
            #calculer la somme
            #T(-1] dernier valeur dans le tableau)
            return h * s / 3.0
    

        def Graph ( self , f ,c,lx,ly, resolution =1001) :
            xl = self.x
            yl = f(xl)
            xlist_fine=np.linspace(self.a, self.b, resolution)
            for i in range(self.n):#range intervalle 0 à n
                xx=np.linspace(xl[i], xl[i+1], resolution)
                #pour chaque subdivisuion  on doit dessiner polynome dnc on doit aussi le subdiviser
                m=(xl[i]+xl[i+1])/2#pt milieu
                aa=xl[i]#borne gauche
                bb=xl[i+1]#borne droite
                l0 = (xx-m)/(aa-m)*(xx-bb)/(aa-bb)
                l1 = (xx-aa)/(m-aa)*(xx-bb)/(m-bb)
                l2 = (xx-aa)/(bb-aa)*(xx-m)/(bb-m)
                P = f(aa)*l0 + f(m)*l1 + f(bb)*l2#fonction dde polynome
                plt.plot(xx,P,'b')#dessiner polynome d'interpolation
                plt.plot(m,f(m),"r*")
            yflist_fine = f(xlist_fine)
            plt.plot(xlist_fine, yflist_fine,color=c)#plot de f(x)
            plt.plot(xl, yl,"cs")#point support
            plt.xlabel(lx)
            plt.ylabel (ly)
            plt.title ( ' Methode de Simpson' )
            plt.text( 0.5*( self.a+ self.b ) , f(self.b ) , 'I_{} ={:0.8f}'.format(self.n,self.integrate( f ) ) , fontsize =10 )

    def sim(a,b,n,f,i,x,y):

        T = Trapezoidal(a,b,n,f,i,x,y)
        S = Simpson(a,b,n,f,i,x,y)
        R = RectangleG(a,b,n,f,i,x,y)
        M = Milieu(a,b,n,f,i,x,y)

        plt.subplot(221)  
        R.Graph(f,i,x,y)
        plt.subplot(222)
        T.Graph(f,i,x,y)
        plt.subplot(223)
        M.Graph(f,i,x,y)
        plt.subplot(224)
        S.Graph(f,i,x,y)
        plt.show()

    N_label=Label(window,text="Choose N: ",font=('helvetica', 9, 'bold'))
    N_label.grid(row=0, column=0,pady=4, padx = 4)

    e_N=Scale(window, from_=0, to=10, orient=HORIZONTAL, length= 300)
    e_N.set(1)
    e_N.grid(row = 0, column = 1, pady=4, padx = 4)

    label_color=Label(window,text="Blue",font=('helvetica', 9, 'bold'),fg="blue")
    label_color.grid(row=6, column=1,pady=0, padx = 0)

    button_color = Button(window, text = "Select color", 
                            command = callback,bg='RoyalBlue1', fg='white', font=('helvetica', 9, 'bold'))
    button_color.grid(row=7, column=1,pady=4, padx = 4)            

    a_label=Label(window,text="Type in A: ",font=('helvetica', 9, 'bold'))
    a_label.grid(row=1, column=0,pady=4, padx = 4)
    a_text=StringVar(window,value='1')
    e_a=Entry(window,textvariable=a_text,width=50)
    e_a.grid(row=1,column=1)

    b_label=Label(window,text="Type in B: ",font=('helvetica', 9, 'bold'))
    b_label.grid(row=2, column=0,pady=4, padx = 4)
    b_text=StringVar(window,value='-1')
    e_b=Entry(window,textvariable=b_text,width=50)
    e_b.grid(row=2,column=1)

    f_label=Label(window,text="Enter a function: ",font=('helvetica', 9, 'bold'))
    f_label.grid(row=3, column=0,pady=4, padx = 4)
    f_text=StringVar(window,value='1/(1+x**2)')
    e_f=Entry(window,textvariable=f_text,width=50)
    e_f.grid(row=3,column=1)

    x_label=Label(window,text="xLabel: ",font=('helvetica', 9, 'bold'))
    x_label.grid(row=4, column=0,pady=4, padx = 4)
    x_text=StringVar(window,value='x')
    e_x=Entry(window,textvariable=x_text,width=50)
    e_x.grid(row=4,column=1)

    fx_label=Label(window,text="yLabel: ",font=('helvetica', 9, 'bold'))
    fx_label.grid(row=5, column=0,pady=4, padx = 4)
    fx_text=StringVar(window,value='f(x)')
    e_fx=Entry(window,textvariable=fx_text,width=50)
    e_fx.grid(row=5,column=1)

    f= lambda x: eval(e_f.get())

    button_generate = Button(window, text = "   Generate   ",command=lambda: sim(int((float(e_a.get()))),int((float(e_b.get()))),e_N.get(),f,c,e_x.get(),e_fx.get()),
    bg='brown', fg='white', font=('helvetica', 9, 'bold'))
    button_generate.grid(row=8, column=1,pady=4, padx = 4)


l1=Label(root,text="Welcome to our App :) ",bg="light blue")
l1.grid(column=1,row=0, pady=20, padx=75, sticky="wens")
l1.config(font=("Courier", 20,))

l2=Label(root,text="Enter your function and see the results !")
l2.grid(column=1,row=1, pady=5, padx=90, sticky="wens")
l2.config(font=("helvetica", 12,))

l3=Label(root,text="Would you like to proceed?")
l3.grid(column=1,row=2, pady=5, padx=90, sticky="wens")
l3.config(font=("helvetica", 12,))

b1 = Button(root, text = "Proceed", command=newWindow,
 bg='brown', fg='white', font=('helvetica', 9, 'bold'))
b1.grid(row=3, column=1,pady=4, padx = 4) 

b2 = Button(root, text = "  Cancel  ", command=root.destroy,
 bg='grey', fg='white', font=('helvetica', 9, 'bold'))
b2.grid(row=4, column=1,pady=4, padx = 4) 

l4=Label(root,text="Created by: Nada Ben Slimen & Hazem Mejri")
l4.grid(row=5, column=1,pady=60, padx = 4) 

root.mainloop()