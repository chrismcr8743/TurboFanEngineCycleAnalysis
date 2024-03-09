"""
This code provides plotting class that is designed to visually represent various parameters.

"""

import sys
sys.path.append(".")
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


class Plotter:
    def __init__(self, BPRs, F_m0s, TSFCs, fs, etas_T, etas_P, etas_O, pi_fs, pi_cs):
        self.BPRs   = BPRs
        self.F_m0s  = F_m0s
        self.TSFCs  = TSFCs
        self.fs     = fs
        self.etas_T = etas_T
        self.etas_P = etas_P
        self.etas_O = etas_O
        self.pi_fs  = pi_fs
        self.pi_cs  = pi_cs

    def plot_3(self): # This method will display 3 figures, each with 4 plots 

        self.fig = plt.figure(figsize=(20, 10))
        gs = gridspec.GridSpec(2, 3)
        # First row, first column
        ax1 = plt.subplot(gs[0, 0])
        ax1.plot(self.BPRs, self.F_m0s[0], 'o-', color='black')
        ax1.set_title("Turbofan specific thrust")
        ax1.set_xlabel("BPR")
        ax1.set_ylabel(r'$F/m_0$' "[N/(kg/s)]")
        ax1.grid(True)
        # First row, second column
        ax2 = plt.subplot(gs[0, 1], sharex=ax1)
        ax2.plot(self.BPRs, self.TSFCs[0], 'o-', color='black')
        ax2.set_title("Turbofan thrust-specific fuel consumption")
        ax2.set_xlabel("BPR")
        ax2.set_ylabel("TSFC [g/(kN-s)]")
        ax2.grid(True)
        # First row, third column
        ax3 = plt.subplot(gs[0, 2], sharex=ax1)
        ax3.plot(self.BPRs, self.fs[0], 'o-', color='black')
        ax3.set_title("Turbofan fuel/air ratio")
        ax3.set_xlabel("BPR")
        ax3.set_ylabel("f")
        ax3.grid(True)
        # Second row, spanning all columns
        ax4 = plt.subplot(gs[1, :])
        ax4.plot(self.BPRs, self.etas_T[0], 'o-', color='black',label='ηT')
        ax4.plot(self.BPRs, self.etas_P[0], 's-', color='black',label='ηP')
        ax4.plot(self.BPRs, self.etas_O[0], 'd-', color='black',label='ηO')
        ax4.set_title("Turbofan thermal, propulsive, and overall efficiencies")
        ax4.set_xlabel("Bypass Ratio (BPR)")
        ax4.set_ylabel("Efficiency ")
        ax4.grid(True)
        ax4.legend()

        self.fig = plt.figure(figsize=(20, 10))
        gs = gridspec.GridSpec(2, 3)
        # First row, first column
        ax1 = plt.subplot(gs[0, 0])
        ax1.plot(self.pi_fs, self.F_m0s[1], 'o-', color='black')
        ax1.set_title("Turbofan specific thrust")
        ax1.set_xlabel(r"$\pi_{f}$")
        ax1.set_ylabel("F/m0 [N/(kg/s)]")
        ax1.grid(True)
        # First row, second column
        ax2 = plt.subplot(gs[0, 1], sharex=ax1)
        ax2.plot(self.pi_fs, self.TSFCs[1], 'o-', color='black')
        ax2.set_title("Turbofan thrust-specific fuel consumption")
        ax2.set_xlabel(r"$\pi_{f}$")
        ax2.set_ylabel("TSFC [g/(kN-s)]")
        ax2.grid(True)
        # First row, third column
        ax3 = plt.subplot(gs[0, 2], sharex=ax1)
        ax3.plot(self.pi_fs, self.fs[1], 'o-', color='black')
        ax3.set_title("Turbofan fuel/air ratio")
        ax3.set_xlabel(r"$\pi_{f}$")
        ax3.set_ylabel("f")
        ax3.grid(True)
        # Second row, spanning all columns
        ax4 = plt.subplot(gs[1, :])
        ax4.plot(self.pi_fs, self.etas_T[1], 'o-', color='black',label='ηT')
        ax4.plot(self.pi_fs, self.etas_P[1], 's-', color='black',label='ηP')
        ax4.plot(self.pi_fs, self.etas_O[1], 'd-', color='black',label='ηO')
        ax4.set_title("Turbofan thermal, propulsive, and overall efficiencies")
        ax4.set_xlabel(r"$\pi_{f}$")
        ax4.set_ylabel("Efficiency")
        ax4.legend()
        ax4.grid(True)

        self.fig = plt.figure(figsize=(20, 10))
        gs = gridspec.GridSpec(2, 3)
        # First row, first column
        ax1 = plt.subplot(gs[0, 0])
        ax1.plot(self.pi_cs, self.F_m0s[2], 'o-', color='black')
        ax1.set_title("Turbofan specific thrust")
        ax1.set_xlabel(r"$\pi_{c}$")
        ax1.set_ylabel("F/m0 [N/(kg/s)]")
        ax1.grid(True)
        # First row, second column
        ax2 = plt.subplot(gs[0, 1], sharex=ax1)
        ax2.plot(self.pi_cs, self.TSFCs[2], 'o-', color='black')
        ax2.set_title("Turbofan thrust-specific fuel consumption")
        ax2.set_xlabel(r"$\pi_{c}$")
        ax2.set_ylabel("TSFC [g/(kN-s)]")
        ax2.grid(True)
        # First row, third column
        ax3 = plt.subplot(gs[0, 2], sharex=ax1)
        ax3.plot(self.pi_cs, self.fs[2], 'o-', color='black')
        ax3.set_title("Turbofan fuel/air ratio")
        ax3.set_xlabel(r"$\pi_{c}$")
        ax3.set_ylabel("f")
        ax3.grid(True)
        # Second row, spanning all columns
        ax4 = plt.subplot(gs[1, :])
        ax4.plot(self.pi_cs, self.etas_T[2], 'o-', color='black',label='ηT')
        ax4.plot(self.pi_cs, self.etas_P[2], 's-', color='black',label='ηP')
        ax4.plot(self.pi_cs, self.etas_O[2], 'd-', color='black',label='ηO')
        ax4.set_title("Turbofan thermal, propulsive, and overall efficiencies")
        ax4.set_xlabel(r"$\pi_{c}$")
        ax4.set_ylabel("Efficiency ")
        ax4.legend()
        ax4.grid(True)
        
        plt.show()
