from tkinter import *
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


class Application():
    """Main application class"""
    def __init__(self, master=None):
        """Class attributes"""
        self.fonteTitulo = ("Helvetica", "20", "bold")
        self.fonteTituloControle = ("Helvetica", "16", "bold")
        self.fonteLabels = ("Helvetica", "14", "bold")
        self.fonteEntry = ("Helvetica", "14")
        self.imagemFresadora = ImageTk.PhotoImage(Image.open("./resources/desenho_ferramenta.jpg").resize((309, 197),Image.ANTIALIAS))
        self.imagemGraficoHolder = ImageTk.PhotoImage(Image.open("./resources/grafico_holder.png").resize((559, 347),Image.ANTIALIAS))
        self.backgroundColor = "#EAE5E1"

        self.stdProporcional = 1.0
        self.stdDerivativo = 0.1
        self.stdIntegral = 2.5

        self.fig = Figure(figsize=(6, 5), dpi=80)
        self.fig.set_facecolor('#f6f2ee')
        self.plot1 = self.fig.add_subplot(111)

        # self.framePrincipal = Frame(master, bg=self.backgroundColor, width=800, height=600, borderwidth=2, relief=RIDGE)
        self.framePrincipal = Frame(master, bg=self.backgroundColor, width=800, height=600)
        self.framePrincipal.pack()

        # self.frameTituloPrincipal = Frame(self.framePrincipal, bg=self.backgroundColor, width=800, height=30, borderwidth=2, relief=RIDGE)
        self.frameTituloPrincipal = Frame(self.framePrincipal, bg=self.backgroundColor, width=800, height=30)
        self.frameTituloPrincipal.pack()
        self.labelTituloPrincipal = Label(self.frameTituloPrincipal, text="CONTROLE PID FRESADORA - ROTAÇÃO DA FERRAMENTA", font=self.fonteTitulo, bg=self.backgroundColor)
        self.labelTituloPrincipal.pack()

        # self.frameControlePrincipal = Frame(self.framePrincipal, bg=self.backgroundColor, width=300, height=570, borderwidth=2, relief=RIDGE)
        self.frameControlePrincipal = Frame(self.framePrincipal, bg=self.backgroundColor, width=300, height=570)
        self.frameControlePrincipal.pack(side=LEFT, padx=(40, 20))
        #
        # self.frameControleTitulo = Frame(self.frameControlePrincipal, bg=self.backgroundColor, borderwidth=2, relief=RIDGE)
        self.frameControleTitulo = Frame(self.frameControlePrincipal, bg=self.backgroundColor)
        self.frameControleTitulo.pack(pady=(36,30))
        self.labelControleTitulo = Label(self.frameControleTitulo, text="CONTROLE", font=self.fonteTituloControle, bg=self.backgroundColor)
        self.labelControleTitulo.pack()
        #
        # self.frameControleProporcional = Frame(self.frameControlePrincipal, bg=self.backgroundColor, borderwidth=2, relief=RIDGE)
        self.frameControleProporcional = Frame(self.frameControlePrincipal, bg=self.backgroundColor)
        self.frameControleProporcional.pack(anchor="w", pady=20)
        self.labelControleProporcional = Label(self.frameControleProporcional, text="Proporcional:", font=self.fonteLabels, bg=self.backgroundColor)
        self.labelControleProporcional.pack(side=LEFT)
        self.scaleControleProporcional = Scale(self.frameControleProporcional, from_=0.1, to=2, resolution=0.1, orient=HORIZONTAL, bg=self.backgroundColor, command=self.configurarProporcional)
        self.scaleControleProporcional.set("1.0")
        self.scaleControleProporcional.pack(side=RIGHT)
        #
        # self.frameControleIntegral = Frame(self.frameControlePrincipal, bg=self.backgroundColor, borderwidth=2, relief=RIDGE)
        self.frameControleIntegral = Frame(self.frameControlePrincipal, bg=self.backgroundColor)
        self.frameControleIntegral.pack(anchor="w", pady=20)
        self.labelControleIntegral = Label(self.frameControleIntegral, text="Integral:", font=self.fonteLabels, bg=self.backgroundColor)
        self.labelControleIntegral.pack(side=LEFT, padx=(0,36))
        self.scaleControleIntegral = Scale(self.frameControleIntegral, from_=0.1, to=10, resolution=0.1, orient=HORIZONTAL, bg=self.backgroundColor, command=self.configurarIntegral)
        self.scaleControleIntegral.set("2.5")
        self.scaleControleIntegral.pack(side=RIGHT)
        #
        # self.frameControleDerivativo = Frame(self.frameControlePrincipal, bg=self.backgroundColor, borderwidth=2, relief=RIDGE)
        self.frameControleDerivativo = Frame(self.frameControlePrincipal, bg=self.backgroundColor)
        self.frameControleDerivativo.pack(anchor="w", pady=(20, 20))
        self.labelControleDerivativo = Label(self.frameControleDerivativo, text="Derivativo:", font=self.fonteLabels, bg=self.backgroundColor)
        self.labelControleDerivativo.pack(side=LEFT, padx=(0,19))
        self.scaleControleDerivativo = Scale(self.frameControleDerivativo, from_=-10, to=10, resolution=0.1, orient=HORIZONTAL, bg=self.backgroundColor, command=self.configurarDerivativo)
        self.scaleControleDerivativo.pack(side=RIGHT)
        #
        self.btnReset = Button(self.frameControlePrincipal, text="Reset", command=self.resetarValores, bg=self.backgroundColor)
        self.btnReset.pack(pady=(0,200))

        # self.frameGraficoPrincipal = Frame(self.framePrincipal, bg=self.backgroundColor, width=300, height=570, borderwidth=2, relief=RIDGE)
        self.frameGraficoPrincipal = Frame(self.framePrincipal, bg=self.backgroundColor, width=300, height=570)
        self.frameGraficoPrincipal.pack(side=RIGHT)
        #
        # self.frameGraficoImagem = Frame(self.frameGraficoPrincipal, bg=self.backgroundColor, borderwidth=2, relief=RIDGE)
        self.frameGraficoImagem = Frame(self.frameGraficoPrincipal, bg=self.backgroundColor)
        self.frameGraficoImagem.pack()
        self.labelImagemFresadora = Label(self.frameGraficoImagem, image=self.imagemFresadora, bg=self.backgroundColor)
        self.labelImagemFresadora.image = self.imagemFresadora
        self.labelImagemFresadora.pack()
        #
        # self.frameGraficoPlot = Frame(self.frameGraficoPrincipal, bg=self.backgroundColor, borderwidth=2, relief=RIDGE)
        self.frameGraficoPlot = Frame(self.frameGraficoPrincipal, bg=self.backgroundColor)
        self.frameGraficoPlot.pack()
        # self.labelGraficoPlot = Label(self.frameGraficoPlot, image=self.imagemGraficoHolder, bg=self.backgroundColor)
        # self.labelGraficoPlot.image = self.imagemGraficoHolder
        # self.labelGraficoPlot.pack(padx=14, pady=(5,8))
        self.plotarGrafico()


    """Class functions"""
    def plotarGrafico(self):
        # process model
        # Kp = 1.0
        # taup = 2.5
        Kp = self.stdProporcional
        taup = self.stdIntegral

        def process(y, t, u, Kp, taup):
            # Kp = process gain
            # taup = process time constant
            dydt = -y / taup + Kp / taup * u
            return dydt

        # specify number of steps
        ns = 500
        # define time points
        t = np.linspace(0, ns / 10, ns + 1)
        delta_t = t[1] - t[0]

        # storage for recording values
        op = np.zeros(ns + 1)  # controller output
        pv = np.zeros(ns + 1)  # process variable
        e = np.zeros(ns + 1)  # error
        ie = np.zeros(ns + 1)  # integral of the error
        dpv = np.zeros(ns + 1)  # derivative of the pv
        P = np.zeros(ns + 1)  # proportional
        I = np.zeros(ns + 1)  # integral
        D = np.zeros(ns + 1)  # derivative
        sp = np.zeros(ns + 1)  # set point
        sp[25:] = 10

        # PID (starting point)
        Kc = 1.0/Kp
        tauI = taup
        # tauD = 0.0

        # Kc = self.stdProporcional
        # tauI = self.stdIntegral
        tauD = self.stdDerivativo

        # PID (tuning)
        # Kc = Kc * 2
        # tauI = tauI / 2
        # tauD = 1.0

        # Upper and Lower limits on OP
        op_hi = 10.0
        op_lo = 0.0

        # loop through time steps
        for i in range(0, ns):
            e[i] = sp[i] - pv[i]
            if i >= 1:  # calculate starting on second cycle
                dpv[i] = (pv[i] - pv[i - 1]) / delta_t
                ie[i] = ie[i - 1] + e[i] * delta_t
            P[i] = Kc * e[i]
            I[i] = Kc / tauI * ie[i]
            D[i] = - Kc * tauD * dpv[i]
            op[i] = op[0] + P[i] + I[i] + D[i]
            if op[i] > op_hi:  # check upper limit
                op[i] = op_hi
                ie[i] = ie[i] - e[i] * delta_t  # anti-reset windup
            if op[i] < op_lo:  # check lower limit
                op[i] = op_lo
                ie[i] = ie[i] - e[i] * delta_t  # anti-reset windup
            y = odeint(process, pv[i], [0, delta_t], args=(op[i], Kp, taup))
            pv[i + 1] = y[-1]
        op[ns] = op[ns - 1]
        ie[ns] = ie[ns - 1]
        P[ns] = P[ns - 1]
        I[ns] = I[ns - 1]
        D[ns] = D[ns - 1]

        ## Plotando o gráfico
        # self.fig = Figure(figsize=(6, 5), dpi=80)
        # self.fig.set_facecolor('#f6f2ee')
        # self.plot1 = self.fig.add_subplot(111)
        # self.plot1.clear()
        self.plot1.plot(t,sp,'k-',linewidth=2)
        self.plot1.plot(t,pv,'b--',linewidth=3)
        self.plot1.legend(['Set Point (SP)','Saída (PV)'],loc='lower right')
        self.plot1.set_ylabel('Rotação (x100) rpm')
        self.plot1.set_ylim([-0.1,12])
        self.plot1.set_xlabel('Tempo (s)')
        self.plot1.set_facecolor('#f6f2ee')
        self.canvasGrafico = FigureCanvasTkAgg(self.fig, master=self.frameGraficoPlot)
        self.canvasGrafico.draw()
        self.canvasGrafico.get_tk_widget().pack(padx=28, pady=(5,8))

    def configurarProporcional(self, valor):
        self.stdProporcional = float(valor)
        self.plotarUpdate()

    def configurarIntegral(self, valor):
        self.stdIntegral = float(valor)
        self.plotarUpdate()

    def configurarDerivativo(self, valor):
        self.stdDerivativo = float(valor)
        self.plotarUpdate()

    def resetarValores(self):
        self.scaleControleProporcional.set("1.0")
        self.stdProporcional = 1.0
        self.scaleControleIntegral.set("2.5")
        self.stdIntegral = 2.5
        self.scaleControleDerivativo.set("0.0")
        self.stdDerivativo = 0.1
        self.plotarUpdate()
        # self.canvasGrafico.get_tk_widget().pack_forget()
        # self.plotarGrafico()
        # return

    def plotarUpdate(self):
        self.plot1.clear()
        self.canvasGrafico.get_tk_widget().pack_forget()
        self.plotarGrafico()


root = Tk()
root.title("Controle PID - Fresadora")
root.geometry("800x600")
Application(root)
root.mainloop()