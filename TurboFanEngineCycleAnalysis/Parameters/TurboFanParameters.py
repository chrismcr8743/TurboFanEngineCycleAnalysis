import sys
sys.path.append(".")
import numpy as np 

# Thermo properties / specific heats
gamma_c = 1.4     # Specific Heat Ratio core 
gamma_h = 1.333   # Specific Heat Ratio hot section
c_pg    = 1.148   # Specific Heat combustion gas, [kJ/kgK]
c_pa    = 1.005   # Specific Heat air, [kJ/kgK]
c_p     = 1005    # Specific Heat air, [J/kgK]
R       = 287.05  # Universal Gas Constant, [J/kgK]

# Componenet efficiencies 
n_inft  = 0.90   # Polytropic turbine 
n_inff  = 0.89   # Polytropic fan
n_infc  = 0.90   # Polytropic compressor 
n_b     = 0.99   # Burner
n_i     = 0.98   # Intake 
n_m     = 0.99   # Mechanical
n_j     = 0.99   # Nozzle 

# Total pressure ratio
pi_b    = 0.96   # Pressure loss combustor
pa      = 0.227  # Ambient Pressure, [bar]
p7      = pa     # [bar]
p8      = pa     # [bar]
T0      = 216.8  # Ambient Temperature, [K]
T04     = 1560.  # Turbine Inlet Temperature, [K]

# Aircraft and flight characteristics 
W_TO    = 370000. # Max Takeoff Weight [lbf]
W       = 0.8 * W_TO
S_W     = 285.    # Wing Surface Area, [m^2]
h_fuel  = 43100   # Heating Value of the Fuel [kJ/kg]
M0      = 0.85    # Freestream Mach 
a       = round(np.sqrt(gamma_c * R * T0 ),1)  # Speed of sound, [m/s]