"""
This code defines a TurboFan class that calculates and displays real performance metrics for a turbofan engine.
The class initializes with default parameters for the Bypass Ratio (BPR), Fan Pressure Ratio (pi_f), and Compressor Pressure Ratio (pi_c).
The class includes methods for each component of the turbofan such as the inlet, fan, compressor, combustor, HP Turbine, LP Rotor, 
cold and hot nozzles, and a method for calculating flight metrics. It also provides methods to run all calculations and display the 
results in a table. 
"""
import sys
sys.path.append(".")
import numpy as np 
from Tools.Eqns import *
import math 
from scipy.optimize import fsolve
from Parameters.TurboFanParameters import *
import pandas as pd
import sympy as sp


class TurboFan:
    def __init__(self, BPR=10, pi_f=1.5, pi_c=36.):
        self.BPR  = BPR  # Bypass ratio 
        self.pi_f = pi_f # Fan pressure ratio 
        self.pi_c = pi_c # Compressor pressure ratio 

    def inlet(self):
        self.p0a_pa = round(pressure_ratio(M0), 4) # Stagnation pressure ratio (p0a/pa)
        self.p01_pa = round(pressure_ratio_n(M0, n_i), 4) # Pressure loss ratio (p01/pa)
        self.p0a    = round(self.p0a_pa * pa, 3) # Stagnation pressure, [bar]
        self.p01    = round(self.p01_pa * pa, 3) # Pressure after loss, [bar] 
        self.T0a    = round(total_temperature(M0, T0, gamma_c), 3) # Stagnation temperature of flow just before it enters the fan, [K]

    def fan(self):
        self.T01 = self.T0a # Stagnation temperature of flow just before it enters the fan, [K]
        self.n   = n1_n(n_inff) # Polytropic exponent 
        self.T02 = round(self.T01 * T02_T01(self.pi_f, self.n), 3) # Temperature after fan, [K]
        self.p02 = round(self.pi_f * self.p01, 3) # Pressure after fan, [bar] 
        self.DeltaT012 = round(self.T02 - self.T01, 2) # Temp change in fan, [K]

    def coldNozzle(self):
        p02_p8 = self.p02/p8 # Pressure ratio
        g1_g   = ((gamma_c-1)/gamma_c) # Calculating the gamma ratio for calculation below 
        self.DeltaT028 = round( n_j * self.T02 * (1 - (1/(p02_p8))**g1_g), 2) # Temperature change in nozzle, [K] 
        self.C8        = round(np.sqrt(2 * c_p * self.DeltaT028), 3) # Velocity at nozzle exit, [m/s]

    def compressor(self):
        self.p03 = round(self.pi_c * self.p02, 3) # Pressure after the compressor, [bar]
        self.nc  = n1_n(n_infc)
        self.DeltaT023 = round(self.T02 * (self.pi_c**self.nc -1), 1) # Temperature change in compressor, [K] 
        self.T03 = round(self.T02 + self.DeltaT023, 2) # Temperature at compressor exit, [K]
        self.wc  = round(c_p * self.DeltaT023 / 1000, 3) # Specific work done, [kJ/kg]
    
    def combustor(self): 
        self.DeltaT034 = round(T04 - self.T03, 2) # Temperature change across combustor, [K] 
        self.p04       = round(self.p03 * (1 - (1 - pi_b)), 3) # Pressure change across the combustor, [bar]
        f = sp.symbols('f')
        solve_f = (1 + f)*c_pg*(T04 - 298) + (f * -h_fuel) + (c_pa * (298 - self.T03))
        f_ideal = sp.solve(solve_f, f)
        f_ideal = round(float(f_ideal[0]), 5) # Ideal fuel flow fraction
        f_ideal = round(( (c_pg*T04) - (c_pa*self.T03) ) / ( h_fuel - (c_pg*T04) ), 6) # Actual fuel flow fraction   
        self.f_act   = round(f_ideal / n_b , 5) # Actual fuel flow fraction

    def hpTurbine(self):
        self.B   = self.BPR 
        self.DeltaT045 = round(( 1/n_m * ((1/(self.B+1)) * c_pa * self.DeltaT023) ) / ((1/(self.B+1) + self.f_act) * c_pg) , 3) # Temperature change across the HP Turbine, [K]
        self.T05 = round(T04 - self.DeltaT045, 3) # Temperature after the HP Turbine
        self.m   = round(m1_m(n_inft, gamma_h), 3) # Polytropic exponent 
        self.p05 = round(self.p04 * (self.T05/T04)**(1/self.m), 3) # Pressure after the HP Turbine, [bar]

    def lpRotor(self):
        self.DeltaT056 = round( (1/n_m * (c_pa * self.DeltaT012) ) / ((1/(self.B+1) + self.f_act) * c_pg), 3) # Temperature change across the LP Rotor, [K]
        self.T06       = self.T05 - self.DeltaT056 # Temperature after the LP Rotor, [K]
        self.p06       = round(( self.p05 * (self.T06/self.T05)**(1/self.m) ), 3) # Pressure after the LP Rotor, [bar]
    
    def hotNozzle(self): 
        pr = self.p06/p7
        self.DeltaT067 = round( n_j * self.T06 * (1 - ((1/(pr)))**((gamma_h-1)/gamma_h)), 2) # Temperature change in the hot nozzle, [K]
        self.C7 = round( np.sqrt(2 * c_pg*1000 * self.DeltaT067), 2) # Velocity at the exit of the hot nozzle, [m/s]
      
    def calculate_flight_metrics(self):
        self.Ca    = round( M0 * (np.sqrt(gamma_c * R * T0)), 3) # Velocity at ambient conditions, [m/s]
        self.q_bar = round( gamma_c/2 * pa * M0**2, 5) # Dynamic pressure, [bar]
        self.q     = self.q_bar*10**5 # Dynamic pressure, [Pa]
        self.C_L   = round( (W * 4.448) / (self.q * S_W), 4) # Lift coefficient
        self.C_D   = round( 0.056*self.C_L**2 - 0.004*self.C_L +0.014, 5) # Drag coefficient
        self.D     = round(self.C_D * self.q * S_W, 2) # Drag force, [N]
        def equation(mDota, C7, Ca, B, f_act, C8): # Define equation and solve for mass flow rate of air
            return self.D - (C7 - Ca) * (mDota / (B + 1) + f_act * mDota) - (C8 - Ca) * (mDota * B / (B + 1))
        mDota_initial_guess = 400. # Use fsolve to solve for mDota
        mDota_solution, = fsolve(equation, mDota_initial_guess, args=(self.C7, self.Ca, self.B, self.f_act, self.C8))
        self.mDota = round(mDota_solution, 2) # Storing the solution for mDota, [kg/s]
        Ta = T0
        self.d = round( np.sqrt((4*self.mDota*R*Ta) / (pa*10**5 * self.Ca * np.pi)), 3) # Calculating fan diameter, [m]


    def run_all_calculations(self):
        self.inlet()
        self.fan()
        self.coldNozzle()
        self.compressor()
        self.combustor()
        self.hpTurbine()
        self.lpRotor()
        self.hotNozzle()
        self.calculate_flight_metrics()


    def display_results(self):
        # Dictionary to hold results from each component
        data = {
            'Component':                    ['Inlet', 'Fan', 'Cold Nozzle', 'Compressor', 'Combustor', 'HP Turbine', 'LP Rotor', 'Hot Nozzle', 'Flight Metrics'],
            'Stagnation Pressure (bar)':    [self.p0a, self.p02, None, self.p03, self.p04, self.p05, self.p06, None, None],
            'Stagnation Temperature (K)':   [self.T0a, self.T02, None, self.T03, T04, self.T05, self.T06, None, None],
            'Pressure Change (bar)':        [self.p01_pa, None, None, None, self.p04, None, None, None, None],
            'Temperature Change (K)':       [None, self.DeltaT012, self.DeltaT028, self.DeltaT023, self.DeltaT034, self.DeltaT045, self.DeltaT056, self.DeltaT067, None],
            'Velocity (m/s)':               [None, None, self.C8, None, None, None, None, self.C7, self.Ca],
            'Specific Work (kJ/kg)':        [None, None, None, self.wc, None, None, None, None, None],
            'Fuel Flow Fraction':           [None, None, None, None, self.f_act, None, None, None, None],
            'Lift Coefficient':             [None, None, None, None, None, None, None, None, self.C_L],
            'Drag Coefficient':             [None, None, None, None, None, None, None, None, self.C_D],
            'Drag Force (N)':               [None, None, None, None, None, None, None, None, self.D],
            'Mass Flow Rate (kg/s)':        [None, None, None, None, None, None, None, None, self.mDota],
            'Fan Diameter (m)':             [None, None, None, None, None, None, None, None, self.d]
        }
        df = pd.DataFrame(data) # Converting to a pandas dataframe
        
        return df.to_string() # Return data as a string 


    def performance(self):
        self.run_all_calculations() # Call components to set up the performance calculations
        mDotc = mdotCold(self.mDota, self.BPR) # Massflow through cold section, [kg/s]
        mDoth = mdotHot(self.mDota, self.BPR) # Massflow through hot section, [kg/s]
        F_m0  = self.D / self.mDota # Thrust to mass flow rate of air, [N/(kg/s)]  
        TSFC  = get_TSFC(self.f_act, self.D, self.mDota) # Thrust specific fuel consumption, [g/kN-s]
        f     = self.f_act # Fuel air ratio
        eta_T = eta_Thermal(self.BPR, self.C8, self.f_act, self.C7, self.Ca, h_fuel) # Thermal efficiency
        eta_P = eta_Propulsive(self.Ca, mDotc, self.C8, mDoth, self.C7, self.mDota) # Propulsive efficiency
        eta_O = eta_T * eta_P # Overall efficiency

        return F_m0, TSFC, f, eta_T, eta_P, eta_O