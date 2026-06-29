import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from calculate_mass_dia import Composition

# change it to apropriate value for better fitting by Kurie-Weiss
TEMP_KURIE_CUTOFF = 150

folder = Path('./data') # Change the path if necessary
# If finds all .dat files in the folder and after 
dat_files = [str(file) for file in folder.rglob('*.dat')]
print("\n\n=============================== CHECK IN ===================================")
print("\n\n=============================== we found .dat files: ===================================")
print(*dat_files, sep="  ||  ")


def is_text_decode(file_path):
    try:
        with open(file_path, 'rb') as f:
            f.read(64).decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False


def check_header(name_dat):
    # check out for mass in header
    print(f"\n============== open new .dat file  -  {name_dat}  ==============")
    df_name = pd.read_csv(name_dat, skiprows=3, nrows=1,  header=None, delimiter="=")
    print(df_name)
    m_s_t = float(df_name.iloc[0,1].split()[0])
    m_b_t = float(df_name.iloc[0,2].split()[0])
    m_oil_t = float(df_name.iloc[0,3])

    df = pd.read_csv(name_dat, skiprows=8, nrows=6, header=None)
    
    print("======== checking mass in header=========")
    m_s = float(df.iloc[0, 2])
    m_b = float(df.iloc[1, 2])
    m_oil = float(df.iloc[2, 2])
    m_box = round(m_oil + m_b, 4)
    formula = str(df.iloc[3, 2])
    molM = str(df.iloc[4, 2]) 
    diacoef = str(df.iloc[5, 2]) 
    print(f"---- m_s = {m_s}, m_b = {m_b}, m_oil = {m_oil}, m_s + m_oil = {m_box} ----")
    
    if m_s != m_s_t:
        print("m_s is not correct in header")     
    if m_b != m_b_t:
        print("m_b is not correct in header")
    if m_oil != m_oil_t:
        print("m_oil is not correct in header")  

    print("======== checking mol mass and dia in header =========")
    print(f"---- formula = {formula}, molm = {molM}, dia = {diacoef} ----")
    print("======== Calculating molM and diacoef from the formula, make sure the formula is right, make change if need =========")
    print("======== You can type formula like 'H2O' or point on valence like 'H+12O' or with space 'H+1 2 O-2' to better find diacoef from the table =========")

    if formula == "nan":
        print("You did not write formula in header, so we will use molM and diacoeff from there, else molM=1 and dia=0")
        molM = float(molM) if molM != "nan" else 1.0
        diacoef = float(diacoef) if diacoef != "nan" else 0.0
        return m_s, m_box, molM, diacoef

    composition = Composition(formula)
    molm = float(composition.mass)
    dia = float(composition.dia)
    print(composition)

    if str(molm) != molM:
        print("molM is not correct in header, we will use the calculated value")     
    if str(dia) != diacoef:
        print("diacoef is not correct in header, we will use the calculated value")

    return m_s, m_box, molm, dia


def read_dat(name_dat):
    
    data =pd.read_csv(name_dat, header=30,)
    df_all = data[["Temperature (K)", "Magnetic Field (Oe)","Frequency (Hz)", "Amplitude (Oe)", 'M-DC (emu)', "M' (emu)", "M'' (emu)",]]
    # df = df_all[df_all['M-DC (emu)'].notna()].copy()
    # df = df_all.copy()
    return df_all


def fill_data(data, m_s, m_box, molm, dia):

    df = data
    # #df = df_all[df_all['M-DC (emu)'].notna()].copy()
    # It needs for grouping
    df['T, K'] = df['Temperature (K)'].round(1)
    df['H, Oe'] = df['Magnetic Field (Oe)'].round(0)
    
    df['bagPE'] = (1/np.tanh(2.38739*df['Temperature (K)'])-1/(2.38739*df['Temperature (K)']))*(-0.000220869)/0.0518*m_box
    df['Hi'] = (df['M-DC (emu)']-df['bagPE']*df['Magnetic Field (Oe)']/5000)/df['Magnetic Field (Oe)'] * molm / m_s+(dia/1000000)
    df['iHi'] = 1 / df['Hi']
    # df['mom'] = np.sqrt(8 * df['Hi'] * df['Temperature (K)'])
    # df['hiT'] = df['Temperature (K)']*df['Hi']
    df['emu'] = df['Hi']*df['Magnetic Field (Oe)']
    df["AC_Hi'"] = df["M' (emu)"]*molm / m_s
    df["AC_Hi''"] = df["M'' (emu)"]*molm / m_s
    return df


def draw_hloops(df, file_name):
    print("\n==============  Creating Temperature constant pictures  ==============\n")
    
    df = df[df['M-DC (emu)'].notna()].copy()
    counts_T = df['T, K'].value_counts()
    if counts_T.max() < 10:
        frequent_values_T = counts_T[counts_T == counts_T.max()].index.to_list()
    else:
        frequent_values_T = counts_T[counts_T > 10].index.to_list()
    
    for max_t in frequent_values_T:
        print(f"data for {max_t} K")
        filtered_df = df[df["T, K"] == max_t]

        # It finds the coercitive force like value
        closest_idx = (filtered_df['M-DC (emu)'] - 0).abs().idxmin()
        result = filtered_df.loc[closest_idx, "Magnetic Field (Oe)"]
        print(f"The closest to zero M-DC = {result}, is coercitive force like")
        
        m_name = f'hloop_{max_t}_K'
        df_to_hloops = filtered_df[["Magnetic Field (Oe)", 'M-DC (emu)',]]
        
        saving_pics(df_to_hloops, file_name, m_name)
        
        
def draw_temps(df, file_name):
    print("\n==============  Creating Field constant pictures  ==============\n")
    
    df = df[df['M-DC (emu)'].notna()].copy()
    counts_M = df['H, Oe'].value_counts()

    if counts_M.max() < 10:
        frequent_values_M = counts_M[counts_M == counts_M.max()].index.to_list()
    else:
        frequent_values_M = counts_M[counts_M > 10].index.to_list()
    
    for max_m in frequent_values_M:
        print(f"data for {max_m} Oe")
        filtered_df = df[df["H, Oe"] == max_m]
        m_name = f'DC_{max_m}_Oe'
        m_name_curie = f'iHi_{max_m}_Oe'
        df_to_temps = filtered_df[["Temperature (K)", 'M-DC (emu)',]]
        df_to_curie = filtered_df[["Temperature (K)", 'iHi',]]
        curie_calc(df_to_curie, file_name, m_name_curie)
        saving_pics(df_to_temps, file_name, m_name)
        

def saving_pics(filtered_df, file_name, m_name):

    if filtered_df.empty:
        print("There is nothing")
        return 
    x_label, y_label = filtered_df.columns
    print("\n==============  saving csv  ==============\n")
    filtered_df.to_csv(f'{file_name}_{m_name}.csv', index=False)

    print("\n==============  saving png  ==============\n")
    x5 = filtered_df[x_label]
    y5 = filtered_df[y_label]
               
    plt.plot(x5, y5, color='green', marker='o', markersize=7)
    plt.xlabel(x_label, fontsize=24, color='black')
    plt.ylabel(y_label, fontsize=24, color='black') 
    plt.title(f'{m_name}', fontsize=24, color='black') 
    plt.grid(True)
    plt.savefig(f'{file_name}_{m_name}.png', dpi=300, bbox_inches='tight', transparent=True)
    plt.close()


def curie_calc(df, file_name, m_name):
    if df.empty:
        print("There is nothing")
        return 
    print("\n==============  saving iHi csv  ==============\n")
    title = file_name[5:]
    df.to_csv(f'{file_name}_{m_name}.csv', index=False)

    x_label, y_label = df.columns
    print("\n==============  Performing Kurie-Weiss calculation  ==============\n")
    # 1. Filter x > 150 ---TEMP_KURIE_CUTOFF
    filtered_df = df[df[x_label] > TEMP_KURIE_CUTOFF]

    X_fit = filtered_df[x_label].values
    Y_fit = filtered_df[y_label].values
    a, b = np.polyfit(X_fit, Y_fit, 1)

    mu2 = 8 / a
    Thetta = - mu2 * b / 8
    mu = np.sqrt(mu2)

    plt.figure(figsize=(8, 5))
    plt.scatter(df[x_label], df[y_label], color='blue', label='Origin')
    plt.scatter(X_fit, Y_fit, color='orange', label='Calculated')
    
    plt.plot(X_fit, a * X_fit + b, color='red', label=f'Curie-Weiss law: mu={mu:.3f} mB, Thetta={Thetta:.1f}K')
    plt.axvline(TEMP_KURIE_CUTOFF, color='gray', linestyle='--',)
    
    plt.xlabel(x_label, fontsize=24, color='black')
    plt.ylabel(y_label, fontsize=24, color='black')
    plt.title(f'{title}_{m_name}', fontsize=24, color='black') #Название
    plt.legend()
    plt.grid(True)
    print("\n==============  saving iHi png  ==============\n")
    plt.savefig(f'{file_name}_{m_name}.png', dpi=300, bbox_inches='tight', transparent=True)
    plt.close()



def create_ac(df, file_name):
    print("\n==============  Creating AC data  ==============\n")
    df = df[["Temperature (K)", "Magnetic Field (Oe)","Frequency (Hz)", "Amplitude (Oe)", "AC_Hi'", "AC_Hi''",]]
    df = df[df["AC_Hi'"].notna()].copy()
    if df.empty:
        print("There is nothing")
        return 
    labels = df.columns
    title = file_name[5:]
    

    values_F = df["Frequency (Hz)"].value_counts().index.to_list()
    
    fig, ax = plt.subplots(figsize=(8, 5))

    for freq in values_F:
        print(f"data for {freq} Hz")
        filtered_df = df[df["Frequency (Hz)"] == freq]
        m_name = f'AC_{freq}_Hz'
        print("\n==============  saving AC csv  ==============\n")
        filtered_df.to_csv(f'{file_name}_{m_name}.csv', index=False)
        
        ax.plot(df[labels[0]], df[labels[4]], color='blue', linewidth=2)
        ax.plot(df[labels[0]], df[labels[5]], color='red', linewidth=2)

    
    # ax.set_title(f'{file_name} AC')
    ax.set_xlabel(labels[0], fontsize=24, color='black')
    ax.set_ylabel('AC (emu/mol)', fontsize=24, color='black')
    plt.title(f'{title}_AC', fontsize=24, color='black') 
    plt.grid(True)
    print("\n==============  saving AC png  ==============\n")
    plt.savefig(f'{file_name}_AC.png', dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
  
    


for file in dat_files:
    if is_text_decode(file):
        file_name = file[:-4]
        m_s, m_box, molm, dia = check_header(file)
        df = read_dat(file)
        cdf = fill_data(df, m_s, m_box, molm, dia)
        draw_hloops(cdf, file_name)
        draw_temps(cdf, file_name)
        create_ac(cdf, file_name)

    else:
        print(f"{file} - is bad")
       
    
    
