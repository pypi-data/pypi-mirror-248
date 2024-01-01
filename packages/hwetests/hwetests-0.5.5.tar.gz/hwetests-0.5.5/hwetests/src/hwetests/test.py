import asta

path = 'data.csv'
p, _, _ = asta.full_algorithm(file_path=path,
                              cutoff_value=4.0,
                              should_save_csv='simulation_with_dict.csv')
print(p)
