import os
import pandas as pd
import numpy as np

def rozdel_dataset_na_tretiny(nd):   # len zisti celkovú dlzku ds
    third_len = len(nd) // 3
    first_part = nd.iloc[:third_len]
    second_part = nd.iloc[third_len:2*third_len]
    third_part = nd.iloc[2*third_len:]
    return first_part, second_part, third_part, third_len

selected_dir = input("Zadejte ID (nápoveda:2-198): ")

db_path = r'C:\Users\hlava\OneDrive\Počítač\BP\PARAMETRE\spiralTrim'
iDir = os.path.join(db_path, selected_dir)

#  raw string treba bo mi to hadze ptm blbosti v terminale
main_output_dir = r'C:\Users\hlava\OneDrive\Počítač\BP\PARAMETRE' 
zmeny_output_file_path = os.path.join(main_output_dir, "VsetkyZmeny.xlsx")

if os.path.isdir(iDir):
  
    svc_file_path = os.path.join(iDir, "spiral.svc")
    
    if os.path.isfile(svc_file_path):
        # Načítanie dát zo súboru spiral.svc
        data_spiral = pd.read_csv(svc_file_path, delimiter=' ', skiprows=1, header=None, names=['X', 'Y', 'timestamp', 'on_surface', 'ir1', 'ir2', 'ir3'])
        
        #on-surface = 1
        nd = data_spiral[data_spiral['on_surface'] == 1].copy()

        nd.loc[:, 'delta_x'] = nd['X'].diff() 
        nd.loc[:, 'delta_y'] = nd['Y'].diff()  
        nd.loc[:, 'delta_time'] = nd['timestamp'].diff()

        # Výpočet rychlosti : Vzorec: Odmocnina rozdiel X2-X1 na 2 + rozdiel Y2-Y1 tiez na druhu----menovateľ rozdiel T2-T1
        nd.loc[:, 'velocity'] = np.sqrt(nd['delta_x']**2 + nd['delta_y']**2) / nd['delta_time']

        # Výpočet zrychlenIA
        nd.loc[:, 'acceleration'] = nd['velocity'].diff() / nd['delta_time']

        # Výpočet švihu
        nd.loc[:, 'jerk'] = nd['acceleration'].diff() / nd['delta_time']

        computed_data = nd[['delta_x', 'delta_y', 'delta_time', 'velocity', 'acceleration', 'jerk']].copy()
        computed_data.insert(0, 'ID', selected_dir)  
        

        # Rozdelenie dat do 3 částí pomocOu funkcie 
        first_part, second_part, third_part, third_len = rozdel_dataset_na_tretiny(nd)

        # Výpočet zmeny rychlosti # mean- priemer spraví
        change_in_velocity_first = first_part['velocity'].diff().mean()   
        change_in_velocity_middle = second_part['velocity'].diff().mean()
        change_in_velocity_last = third_part['velocity'].diff().mean()

        average_velocity_first = first_part['velocity'].mean()
        average_velocity_middle = second_part['velocity'].mean()
        average_velocity_last = third_part['velocity'].mean()

        average_acceleration_first = first_part['acceleration'].mean()
        average_acceleration_middle = second_part['acceleration'].mean()
        average_acceleration_last = third_part['acceleration'].mean()

        average_jerk_first = first_part['jerk'].mean()
        average_jerk_middle = second_part['jerk'].mean()
        average_jerk_last = third_part['jerk'].mean()

        #výsledky do DF
        results = pd.DataFrame({
            'ID': [selected_dir] * 3,
            'Section': ['Začiatok', 'Stred', 'Koniec'],
            'Change in Velocity': [change_in_velocity_first, change_in_velocity_middle, change_in_velocity_last],
            'Average Velocity': [average_velocity_first, average_velocity_middle, average_velocity_last],
            'Average Acceleration': [average_acceleration_first,average_acceleration_middle, average_acceleration_last],
            'Average Jerk': [average_jerk_first, average_jerk_middle, average_jerk_last]
        })

        # Uloženie výsledkov do excelovskej tabuľky
        output_file_path = os.path.join(iDir, "výsledky.xlsx")
        
        with pd.ExcelWriter(output_file_path) as writer:
            
            data_spiral.to_excel(writer, sheet_name='Pôvodné dáta', index=False)
            computed_data.to_excel(writer, sheet_name='Vypočítané dáta', index=False)
            results.to_excel(writer, sheet_name='Zmeny', index=False)

        # Uloženie výsledkov do "VsetkyZmeny.xlsx" 
        if os.path.exists(zmeny_output_file_path):
            existing_df = pd.read_excel(zmeny_output_file_path, sheet_name='Zmeny')
            combined_df = pd.concat([existing_df, results], ignore_index=True)
        else:
            combined_df = results
        
        with pd.ExcelWriter(zmeny_output_file_path, mode='w') as writer:
            combined_df.to_excel(writer, sheet_name='Zmeny', index=False)

        print(f'Zmena rychlosti na začiatku: {change_in_velocity_first:.6f}')
        print(f'Zmena rychlosti v strede: {change_in_velocity_middle:.6f}')
        print(f'Zmena rychlosti na konci: {change_in_velocity_last:.6f}')
        print(f'Začiatok: od riadku {first_part.index[0]} do riadku {first_part.index[-1]}')
        print(f'Stred: od riadku {second_part.index[0]} do riadku {second_part.index[-1]}')
        print(f'Koniec: od riadku {third_part.index[0]} do riadku {third_part.index[-1]}')

    else:
        print(f'Súbor "spiral.svc" sa nepodarilo nájsť v adresári {selected_dir}.')
else:
    print(f'Adresár {selected_dir} neexistuje.')

