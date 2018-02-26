import matplotlib.pyplot as plt
import pandas as pd
import os



def plotAccData(file, df): 
	# Plot ACC data
	df = pd.DataFrame(df, columns=('Time', 'ACC X raw', 'ACC Y raw', 'ACC Z raw'))
	plt.clf()  #  clears data and axes
	plt.scatter(df['Time'],df['ACC X raw'], label='ACC X raw', s=1, color='C0')
	plt.scatter(df['Time'],df['ACC Y raw'], label='ACC Y raw', s=1, color='Green')  
	plt.scatter(df['Time'],df['ACC Z raw'], label='ACC Z raw', s=1, color='Orange')

	plt.title('ACC' )
	plt.ylabel('Acceleration [m/s^2]')
	plt.xlabel('Time [s]')
	plt.legend(shadow=True, fontsize=8)

	plt.grid()

	OUTPUT_FOLDER='./Output/%s/' % (file[:-5])
	if not os.path.exists(OUTPUT_FOLDER): os.makedirs(OUTPUT_FOLDER)
	plt.savefig(OUTPUT_FOLDER+str(file[:-5])+'_ACC.png',dpi = 500)


def plotGyrData(file, df): 
	# Plot GYR data
	df = pd.DataFrame(df, columns=('Time', 'GYR angle X degree', 'GYR angle Y degree', 'GYR angle Z degree'))
	plt.clf()  #  clears data and axes
	plt.scatter(df['Time'],df['GYR angle X degree'], label='GYR angle X degree', s=1, color='C0')
	plt.scatter(df['Time'],df['GYR angle Y degree'], label='GYR angle Y degree', s=1, color='Green')  
	plt.scatter(df['Time'],df['GYR angle Z degree'], label='GYR angle Z degree', s=1, color='Orange')
	plt.title('GYR' )
	plt.ylabel('Angle [deg]')
	plt.xlabel('Time [s]')
	plt.legend(shadow=True, fontsize=8)

	plt.grid()

	OUTPUT_FOLDER='./Output/%s/' % (file[:-5])
	if not os.path.exists(OUTPUT_FOLDER): os.makedirs(OUTPUT_FOLDER)
	plt.savefig(OUTPUT_FOLDER+str(file[:-5])+'_GYR.png',dpi = 500)
