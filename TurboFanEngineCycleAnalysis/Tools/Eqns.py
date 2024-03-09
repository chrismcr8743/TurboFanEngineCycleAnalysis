"""
Various equations used by the TurboFan class
"""
import sympy as sp

import sys
sys.path.append(".")

# Calculate the ratio of total temperatures 
def T02_T01(ratio, n):
    return (ratio)**n

# Calculates (n-1)/n for a fan or compressor based on n_i and gamma
def n1_n(n_i, gamma = 1.4):
    return round(1/(n_i) * ((gamma-1)/gamma),4)

# Calculates (m-1)/m for a turbine based on n_t and gamma
def m1_m(n_i, gamma = 1.3333):
    return round((n_i) * ((gamma-1)/gamma),4)

# Calculate the pressure ratio P0/P1 for a given Mach number
def pressure_ratio(M, gamma=1.4):
    P0P1 = (1 + (gamma-1)/2.0*M**2.0)**(gamma/(gamma-1))
    return P0P1

# Calculate the pressure ratio P0/P1 for a given Mach number and efficiency
def pressure_ratio_n(M, ni, gamma=1.4):
    P0P1 = (1 + ni*(gamma-1)/2.0*M**2.0)**(gamma/(gamma-1))
    return P0P1

# Calculate total temperature T0 for a given Mach number and temperature T
def total_temperature(M, T, gamma=1.4):
    T0T1 = (1 + (gamma-1)/2.0*M**2.0)
    return T0T1*T

# Ideal fuel flow fraction
def solve_f_ideal( T_b4comb, T_afcomb, c_pa=1.005, c_pg=1.148, h_fuel=43100):
    f = sp.symbols('f')
    solve_f = (1 + f)*c_pg*(T_afcomb - 298) + (f * -h_fuel) + (c_pa * (298 - T_b4comb))
    f_ideal = sp.solve(solve_f, f)
    f_ideal = round(float(f_ideal[0]), 5)
    return f_ideal

# Calculate TSFC in units of g/kN-s
def get_TSFC(f, F, mDot0):
    F     = F * 0.001      # Convet thust from N to kN
    mDot0 = mDot0 * 1000   # Convert massflow from  kg/s to g/s
    return f / (F / mDot0) # [g / kN-s]

# Calculate mass flow cold section 
def mdotCold(mDota, BPR):
    return   ((mDota*BPR) / (BPR+1))

# Calculate mass flow hot section
def mdotHot(mDota, BPR):
    return   ( mDota  / (BPR+1))

# Calculate thermal efficiency
def eta_Thermal(BPR, C8, f_act, C7, Ca, h_fuel):
    num =  ( BPR*C8**2 + (1+f_act)*C7**2 - (1+BPR)*Ca**2 )
    den =  2* ( f_act * h_fuel * 1000)
    return num/den

# Calculate propulsive efficiency
def eta_Propulsive(C0, mDotc, C19, mDoth, C9, mDota):
    num = C0  * ((mDotc*(C19-C0)) + (mDoth*(C9-C0))) 
    den =  .5*(mDoth*C9**2 + mDotc*C19**2 - mDota*C0**2)
    return num/den






