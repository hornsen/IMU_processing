import numpy as np
import pandas as pd
from scipy import integrate


def calcAccNorm( row ):
	# Calculate norm for ACC

	accNorm = np.sqrt( row['ACC X raw']**2  + row['ACC Y raw']**2 + row['ACC Z raw']**2 )
	accNorm = accNorm.round(decimals=2)

	return accNorm, row['Time'] 


def calcGyrAngle( dfRaw ):
	# This function calculates the angles from the gyroscope sensors in deg.
	
	# Some preperations before calculating
	dfPreperation = pd.DataFrame()
	dfPreperation = dfRaw[ ['Time', 'GYR X raw', 'GYR Y raw', 'GYR Z raw'] ]

	# Time interval where bias will be calculated
	bias = dfPreperation.query('0 <= Time <= 10')

	# Calculate bias for each coordinate
	biasGyrX = bias['GYR X raw'].mean()
	biasGyrY = bias['GYR Y raw'].mean()
	biasGyrZ = bias['GYR Z raw'].mean()


	# Create dfGyr frame. This will be the result
	dfGYR = pd.DataFrame()

	# Interval that will be used in calculations
	calculate = dfPreperation[dfPreperation['Time'] > 10]

	# GYR angle in degree
	dfGYR['GYR angle X degree'] = integrate.cumtrapz(calculate['GYR X raw']-biasGyrX,calculate['Time'])
	dfGYR['GYR angle Y degree'] = integrate.cumtrapz(calculate['GYR Y raw']-biasGyrY,calculate['Time'])
	dfGYR['GYR angle Z degree'] = integrate.cumtrapz(calculate['GYR Z raw']-biasGyrZ,calculate['Time'])    

	# The first time point is lost because of integration
	dfGYR['Time'] = calculate['Time'][1:].copy().reset_index(drop=True) 

	# Change round to 2 decimals
	dfGYR=dfGYR.round(decimals=2)

	return dfGYR


