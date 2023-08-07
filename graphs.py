# Run this code alone before using the rest of the code to connect to Google Drive:
# from google.colab import drive
# drive.mount('/content/drive')

import csv
import numpy as np
import matplotlib.pyplot as plt


file_pre = '/content/drive/MyDrive/IC_LabTel_LAIoT/Sensor_de_Nivel/Testes/05-06/'
files_t  = f'{file_pre}1x58b/t_'
files_d  = f'{file_pre}1x144b/d_'
files_m  = f'{file_pre}1x256b/m_'
files_t5 = f'{file_pre}5x58b/t5_'
files_m5 = f'{file_pre}5x256b/m5_'

file_names = [files_t, files_d, files_m, files_t5, files_m5]
files_num = 20
# files_folders = 5

Rs = 0.88
VR_values = []
power = []
consumption = []
current = []
time_values = []

# VR Function:
def calculate_VR(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)

        # Skip the first two rows as headers
        next(reader)
        next(reader)

        # Skip the next 3 rows that are empty
        next(reader)
        next(reader)
        next(reader)

        file_VR_values = []
        file_power_values = []
        file_consumption_values = []
        file_current_values = []
        file_time_values = []
        file_xmin = 0
        file_xmax = None

        media = []

        for row in reader:
            # if current_idx == 0 and i > 80 and i<= 90:
            #     print(row[0])]

            file_xmax = float(row[0])
            
            if file_xmin == 0:
                file_xmin = float(row[0])

            if len(row) >= 3 and row[1] and row[2]:
                # Shunt Resistor Voltage Drop (V)
                VR = float(row[1]) - float(row[2])
                file_VR_values.append(VR)
                
                # I(A) = V / Rs
                current_value_A = VR / Rs
                current_value_mA = 1000.0 * current_value_A
                file_current_values.append(current_value_mA)
                
                # P(W) = U * I
                power_value_W = float(row[2]) * current_value_A   # P = V * I
                power_value_mW = 1000.0 * power_value_W
                file_power_values.append(power_value_mW)

                # if current_idx == 0 and i > 80 and i<= 90:
                #   print(power_value)
                if current_idx == 0 and float(row[0]) >= 8.6 and float(row[0]) <= 13.5:
                  media.append(power_value_mW)

                # Q(J) = P * dt  =>  Q = R * i^2 * dt
                consumption_value_J = power_value_W * 0.001302
                consumption_value_mJ = 1000.0 * consumption_value_J
                file_consumption_values.append(consumption_value_mJ)

                file_time_values.append(float(row[0]))

        VR_values.append(file_VR_values)
        power.append(file_power_values)
        consumption.append(file_consumption_values)
        current.append(file_current_values)
        time_values.append(file_time_values)

        # Plot the subtracted values for each file
        # if current_idx < 10:
        #   axes[0,current_idx].plot(file_time_values, file_current_values)
        # else:
        #   axes[1,(current_idx-10)].plot(file_time_values, file_current_values)

        if current_idx == 0:
            # print(np.mean(media))
            plt.figure(figsize=(10,4))
            plt.plot(file_time_values, file_power_values)
            # plt.plot(file_time_values, file_current_values)
            plt.tick_params(axis='both', which='major', labelsize=12)
            plt.xticks(np.arange(4,16,1))
            plt.xticks(np.arange(4,16,0.2), minor=True)
            plt.yticks(np.arange(0,201,50))
            plt.yticks(np.arange(0,201,10), minor=True)
            plt.xlim(xmin=file_xmin)
            plt.xlim(xmax=file_xmax)
            plt.ylim(ymax=200)
            plt.ylim(ymin=0)
            plt.xlabel('Time (s)', fontsize=12)
            plt.ylabel('Power (mW)', fontsize=12)
            # plt.ylabel('Current (mA)', fontsize=12)
            plt.show()




sum_consumption_mean_files = []
sum_consumption_std_files = []
mean_power_mean_files = []
mean_power_std_files = []
x_labels = []
file_idx = 0
current_idx = 0

for name in range(len(file_names)):
    # Provide the filenames of CSV files
    filenames = []
    for num in range(files_num):
        filenames.append(f'{file_names[name]}{num+1}.csv')
    
    if file_idx < 3:
      string_end = (len(file_names[file_idx]) - 4)
    else:
      string_end = (len(file_names[file_idx]) - 5)

    print()
    print("---------------------------------------------------------------------------")
    print(f"Tests of {file_names[file_idx][len(file_pre):string_end]} bytes:")

    # VR:
    VR_values = []
    power = []
    consumption = []
    current_idx = 0

    # fig, axes = plt.subplots(nrows=2, ncols=int(files_num/2), figsize=(18,5))
    # fig.suptitle(f'Withdrawn Current for test of {file_names[file_idx][len(file_pre):string_end]} bytes', fontsize=14, fontweight='bold', y=0.95)
    # fig.text(0.5, 0, 'Time (s)', ha='center', fontsize=12)

    for filename in filenames:
        calculate_VR(filename)
        current_idx = current_idx + 1
    
    # for i, ax in enumerate(axes.flat):
    #     # ax.set_xticks([])
    #     ax.set_ylim(0,120)

    #     if i % int(files_num/2) == 0:
    #         ax.set_yticks(np.arange(0, 121, 20))
    #         ax.set_ylabel('Current (mA)')
    #     else:
    #         ax.set_yticks([])
    
    # fig.tight_layout()
    # plt.show()

    # Calculate the mean value and standard deviation of mean_power
    mean_power_values = []
    for file_values in power:
        mean_power = np.mean(file_values)
        mean_power_values.append(mean_power)
    mean_power_mean = np.mean(mean_power_values)
    mean_power_std = np.std(mean_power_values)
    mean_power_mean_files.append(mean_power_mean)
    mean_power_std_files.append(mean_power_std)

    # Calculate the sum value and standard deviation of sum_consumption
    sum_consumption_values = []
    for file_values in consumption:
        sum_consumption = np.sum(file_values)
        sum_consumption_values.append(sum_consumption)
    sum_consumption_mean = np.mean(sum_consumption_values)
    sum_consumption_std = np.std(sum_consumption_values)
    sum_consumption_mean_files.append(sum_consumption_mean)
    sum_consumption_std_files.append(sum_consumption_std)

    # Print the mean value and standard deviation of mean_power and sum_consumption
    mean_power_mean_sci = "{:.5e}".format(mean_power_mean)
    mean_power_std_sci  = "{:.5e}".format(mean_power_std)
    sum_consumption_mean_sci   = "{:.5e}".format(sum_consumption_mean)
    sum_consumption_std_sci    = "{:.5e}".format(sum_consumption_std)

    print(f"Mean Power (mW): {mean_power_mean_sci}")
    print(f"StdDev Mean Power: {mean_power_std_sci}")
    print(f"Mean Consumption (mJ): {sum_consumption_mean_sci}")
    print(f"StdDev Mean Consumption: {sum_consumption_std_sci}")
    print()

    # Generate a bar graph for sum_consumption_values while maintaining mean_power values
    plt.bar(np.arange(len(sum_consumption_values)), sum_consumption_values)
    plt.xticks(np.arange(len(sum_consumption_values)), np.arange(1, len(sum_consumption_values) + 1))
    plt.xlabel('Test Number')
    plt.ylabel('Consumption (mWh)')
    plt.title(f'Power Consumption for each test of {file_names[file_idx][len(file_pre):string_end]} bytes')
    plt.show()

    x_labels.append(f'{file_names[file_idx][len(file_pre):string_end]} bytes')
    file_idx = file_idx + 1


print()
print("---------------------------------------------------------------------------")
print("Comparing the tests:")

# # Generate a bar graph comparing all sum_consumption_mean
print()
plt.bar(np.arange(len(mean_power_mean_files)), mean_power_mean_files, yerr=mean_power_std_files, capsize=5)
plt.xticks(np.arange(len(mean_power_mean_files)), x_labels)
plt.xlabel('Test type')
plt.ylabel('Dissipated Power (mW)')
plt.title('Comparison of Power ')
plt.show()

# Generate a bar graph comparing all sum_consumption_mean
print()
plt.figure(figsize=(10,4))
plt.bar(np.arange(len(sum_consumption_mean_files)), sum_consumption_mean_files, yerr=sum_consumption_std_files, capsize=5)
plt.tick_params(axis='both', which='major', labelsize=12)
plt.xticks(np.arange(len(sum_consumption_mean_files)), x_labels)
plt.yticks(np.arange(500,701,50))
plt.yticks(np.arange(500,701,10), minor=True)
plt.ylim(ymin=490)
plt.ylim(ymax=700)
plt.xlabel('Experiment', fontsize=12)
plt.ylabel('Consumption (mJ)', fontsize=12)
plt.show()

print()
print("Mean consumption per transmitted bytes:")
print(f"1x58  (58 bytes)   = {sum_consumption_mean_files[0]/58}")
print(f"1x144 (144 bytes)  = {sum_consumption_mean_files[1]/144}")
print(f"1x256 (256 bytes)  = {sum_consumption_mean_files[2]/256}")
print(f"5x58  (290 bytes)  = {sum_consumption_mean_files[3]/290}")
print(f"5x256 (1280 bytes) = {sum_consumption_mean_files[4]/1280}")
print()
print("Increase in consumption comparing to first experiment:")
print(f"1x144b = {100 * (sum_consumption_mean_files[1] - sum_consumption_mean_files[0]) / sum_consumption_mean_files[0]}")
print(f"1x256b = {100 * (sum_consumption_mean_files[2] - sum_consumption_mean_files[0]) / sum_consumption_mean_files[0]}")
print(f"5x58b  = {100 * (sum_consumption_mean_files[3] - sum_consumption_mean_files[0]) / sum_consumption_mean_files[0]}")
print(f"2x256b = {100 * (sum_consumption_mean_files[4] - sum_consumption_mean_files[0]) / sum_consumption_mean_files[0]}")
