"""
This code evaluate and plot the real performance metrics of a TurboFan engine. 
The metrics are calculated based on varying parameters such as Bypass Ratio (BPR), Fan Pressure Ratio (FPR), and Compressor Pressure Ratio (CPR). 
The results of the engine's component calculations are written to a file named "ComponentResults.txt".
It also stores the calculated metrics in Pandas DataFrames and writes these data to a file named "PerformanceResults.txt".
Finally, it utilizes a Plotter class to visualize the calculated metrics on figures.

    The performance metrics considered include:
        - Thrust to mass flow rate ratio of air
        - Thrust Specific Fuel Consumption
        - Fuel to air ratio 
        - Turbine efficiency
        - Propulsive efficiency
        - Overall efficiency

"""
import sys
sys.path.append(".")
import numpy as np
from CycleAnalysis.TurboFan import TurboFan
from Plotter.Plotter import Plotter
import pandas as pd

# Function to calculate performance metrics 
def performance_metrics(engine, param_val, idx):
    engine.performance()
    F_m0, TSFC, f, eta_T, eta_P, eta_O, = engine.performance()

    # Store calculated metrics in dictionary
    metrics = {
        'BPRs': BPR if idx == 0 else pi_f if idx == 1 else pi_c,
        'F_m0s': F_m0,
        'TSFCs': TSFC,
        'fs': f,
        'etas_T': eta_T,
        'etas_P': eta_P,
        'etas_O': eta_O
    }
    return metrics


# Initializing lists to store the calculated metrics
BPRs, pi_fs, pi_cs = [], [], []
F_m0s, TSFCs, fs, etas_T, etas_P, etas_O = [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]]
# Overwrite file when running so previous data is removed 
open('ComponentResults.txt', 'w').close()



# Calculating and storing metrics for varying BPR
for BPR in np.linspace(5, 20, 16): # BPR from 5 to 20 in steps of 1
    engine = TurboFan(BPR, pi_f=1.5, pi_c=36.)
    engine.run_all_calculations()
    # Write component results to a file named "ComponentResults.txt" 
    with open('ComponentResults.txt', 'a') as file: # Append file and add BPR data
        file.write(f"\nResults for BPR = {BPR}\n")
        results = engine.display_results()
        file.write(results + '\n')

    # Store variables and metrics for later plotting
    metrics = performance_metrics(engine, BPR, 0)
    BPRs.append(metrics['BPRs'])
    F_m0s[0].append(metrics['F_m0s'])
    TSFCs[0].append(metrics['TSFCs'])
    etas_T[0].append(metrics['etas_T'])
    etas_P[0].append(metrics['etas_P'])
    etas_O[0].append(metrics['etas_O'])
    fs[0].append(metrics['fs'])


# Calculating and storing metrics for varying FPR
for pi_f in np.linspace(1.2, 2.0, 9): # FPR from 1.2 to 2.0 in steps of 0.1
    engine = TurboFan(10, pi_f, 36.)
    engine.run_all_calculations()
    # Write component results to a file named "ComponentResults.txt" 
    with open('ComponentResults.txt', 'a') as file: # Append file and add CPR data
        file.write(f"\nResults for pi_f = {pi_f}\n")
        results = engine.display_results()
        file.write(results + '\n')

    # Store variables and metrics for later plotting
    metrics = performance_metrics(engine, pi_f, 1)
    pi_fs.append(metrics['BPRs'])
    F_m0s[1].append(metrics['F_m0s'])
    TSFCs[1].append(metrics['TSFCs'])
    etas_T[1].append(metrics['etas_T'])
    etas_P[1].append(metrics['etas_P'])
    etas_O[1].append(metrics['etas_O'])
    fs[1].append(metrics['fs'])


# Calculating and storing metrics for varying CPR
for pi_c in np.linspace(20, 40, 21): # CPR from 20 to 40 in steps of 1
    engine = TurboFan(10, 1.5, pi_c)
    engine.run_all_calculations()
    # Write component results to a file named "ComponentResults.txt" 
    with open('ComponentResults.txt', 'a') as file: # Append file and add CPR data
        file.write(f"\nResults for pi_c = {pi_c}\n")
        results = engine.display_results()
        file.write(results + '\n')

    # Store variables and metrics for later plotting
    metrics = performance_metrics(engine, pi_c, 2)
    pi_cs.append(metrics['BPRs'])
    F_m0s[2].append(metrics['F_m0s'])
    TSFCs[2].append(metrics['TSFCs'])
    etas_T[2].append(metrics['etas_T'])
    etas_P[2].append(metrics['etas_P'])
    etas_O[2].append(metrics['etas_O'])
    fs[2].append(metrics['fs'])

# Creating DataFrames for Performacne data for each case 
df_bpr = pd.DataFrame({
    'BPR': BPRs,
    'F_m0': F_m0s[0],
    'TSFC': TSFCs[0],
    'f': fs[0],
    'eta_T': etas_T[0],
    'eta_P': etas_P[0],
    'eta_O': etas_O[0]
})
df_pi_f = pd.DataFrame({
    'pi_f': pi_fs,
    'F_m0': F_m0s[1],
    'TSFC': TSFCs[1],
    'f': fs[1],
    'eta_T': etas_T[1],
    'eta_P': etas_P[1],
    'eta_O': etas_O[1]
})
df_pi_c = pd.DataFrame({
    'pi_c': pi_cs,
    'F_m0': F_m0s[2],
    'TSFC': TSFCs[2],
    'f': fs[2],
    'eta_T': etas_T[2],
    'eta_P': etas_P[2],
    'eta_O': etas_O[2]
})
# Write performance data to a .txt file named "PerformanceResults.txt" 
with open('PerformanceResults.txt', 'w') as file:
    file.write("Data for varying BPR:\n")
    file.write(df_bpr.to_string())
    file.write("\n\nData for varying pi_f:\n")
    file.write(df_pi_f.to_string())
    file.write("\n\nData for varying pi_c:\n")
    file.write(df_pi_c.to_string())


# Initializing plotting class and plotting the data on two figures 
PlotData = Plotter(BPRs, F_m0s, TSFCs, fs, etas_T, etas_P, etas_O, pi_fs, pi_cs)
PlotData.plot_3()