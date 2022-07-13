#### PREAMBLE LOADS LIBRAIRES, DATA FILES, AND SETS PATH TO LOCAL MACHINE ####
import numpy as np
import pandas as pd
import matplotlib
#matplotlib.rcParams['text.usetex'] = True #For LATEX labels in line 44. Comment out if LATEX not available
import matplotlib.pyplot as plt
import seaborn as sns

#LIBRARIES FOR SECOND EXAMPLE
import matplotlib.lines as mlines
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Rectangle
from matplotlib.patches import Patch
from scipy.spatial import distance

path = "/Users/jairgarcia/Documents/CESAR/" #Local path were data files reside

# %%codecell #Loads datafiles for the plots
coeff = pd.read_csv(path + "power_disc_function_red.csv") #Reads .CSV file containing the posterior distributions of coefficients and radom terms for a power function describing colour discrimination as a function of colour differences (Figure 1)
data = pd.read_csv(path + "wrigth.csv") #Reads data corresponding to the likelihood of discriminating colour differences of various wavelengths by a bird observer obtained during a behavioural experiment (Figure 1)

knaut_fly = pd.read_csv(path + "fly_knautia_PDF_CDF.csv", header = 0,
names = ["x_prime","y_prime","PDF","CDF"]) # Simulated colour loci for Knautia longifolia a rewarding flower species (Figure 2)

scab_fly = pd.read_csv(path + "fly_scabiola_PDF_CDF.csv", header = 0,
names = ["x_prime","y_prime","PDF","CDF"]) #Simulated colour loci for Scabiola lucida a rewarding flower species (Figure 2)

trauns_fly = pd.read_csv(path + "fly_trauns_PDF_CDF.csv", header = 0,
names = ["x_prime","y_prime","PDF","CDF"])# Simulated colour loci for Trausteinera globosa a non rewarding mimic of Knautia and Scabiola (Figure 2)

n = 200 #RESOLUTION OF GRID USED TO SAMPLE THE FITTED DISTRIBUTION DO NOT CHANGE ! AS IT WAS PRODUCED IN R
fly_scab_x = np.linspace(0.444, 0.686, num = n) #Defines the sampling grid
fly_scab_y = np.linspace(1.02, 1.09, num = n)
fly_scab_Z = np.genfromtxt(path + "scabiola_Z_fly_distribution_2021.csv", delimiter = ",") #Reads colour loci probability density simulated for Scabiola

fly_knautia_x = np.linspace(0.470, 0.700, num = n)
fly_knautia_y = np.linspace(1.01, 1.11, num = n)
fly_knautia_Z = np.genfromtxt(path + "knaut_Z_fly_distribution_2021.csv", #Reads colour loci probability density simulated for Knautia
delimiter = ",")

fly_trauns_x = np.linspace(0.478, 0.735, num = n)
fly_trauns_y = np.linspace(0.985, 1.08, num = n)
fly_trauns_Z = np.genfromtxt(path + "traunsteinera_Z_fly_distribution_2021.csv", #Reads colour loci probability density simulated for Traunsteinera
delimiter = ",")
#### END OF PREAMBLE PLOTTING CODE FROM HERE ONWARDS ####



#### EXAMPLE 1: GRAPHICAL REPRESENTATION OF A NON-LINEAR FUNCTION DESCRIBING
# LIKELIHOOD OF DISCRIMINATION BASED ON COLOUR DIFFERENCE FOR 4 DIFFERENT
# STIMULI. POSTERIOR DISTRIBUTION OF FIXED AND RANDOM  COEFFICIENTS WERE
#ESTIMATED USING BAYESIAN MODELLING IN R USING THE LIBRARY BRMS ####

# %%codecell #Evaluates 100,000 discrimination functions from the coefficients' posterior distributions. May take up to 1.5 mins to execute please be patient!
r_effect = []
X = np.linspace(0.005, 0.992, 100) #Function domain: Colour differences between 0.005 and 0.992 units.
for j in range(4, 8):
    f = np.empty([100000, 100])
    for ii in np.arange(100000):
        f[ii,:] = (coeff.iloc[ii,0] + coeff.iloc[ii,j]) * (X ** (coeff.iloc[ii,1])) #The non-linear power function describing the realtionship between likelihood of colour discrimination and colour difference for four different wavelengths
    r_effect.append(f)

# %%codecell #Plots the median discrimination function and its 95 % credibility intervals
lwave = data['wave_ref'].unique() #Recover the values of the wavelength stimuli tested
pltte = sns.color_palette("hls", 4) #selects 4 colours of the HLS palette to represent the different stimuli tested
lett = [chr(x) for x in range(65, 69)] #Generates letters for labelling figure panels
wlenght = np.arange(470, 510, 10)
fig, axes = plt.subplots(2,2, figsize = (10,10), sharex = True, sharey = True) #Creates figure axis in a format suitable for looping.
for ii, ax in enumerate (axes.flatten()):
    rand_ci = np.quantile(r_effect[ii], [0.025, 0.975],axis = 0).transpose() #Calculates 95 % credibiility bounds for the discrimination function
    rand_median = np.median(r_effect[ii], axis = 0) #The median discrimination function
    ax.plot(X,rand_median, lw = 3, color = "steelblue") #Plots the median function
    ax.fill_between(X, rand_ci[:,0], rand_ci[:,1],  alpha = 0.5,
    color = "slategrey") #Plots the credibility bounds as a uncertainty region around the median discrimination function
    ax.scatter(data[data['wave_ref']==lwave[ii]]['dc'],
    data[data['wave_ref']==lwave[ii]]['d_prime'], color = pltte[ii]) #Plots the observations for each tested stimuli used to fit the power function
    ax.text(-0.2, 12.5, lett[ii], weight = "bold", fontsize = 18) #Labels each panel using uppercase letters
    #ax.text(0.05, 12, r'$\lambda_{\mathrm{ref}} =\,$' + str(wlenght[ii]) + " nm", fontsize = 15) #Plot annnotations using LATEX comment out if LATEX is not available
    if (ii == 0) or (ii == 2): #Axis labels for panels in first coloumn
        ax.set_ylabel("d'", fontsize = 18)
    if (ii == 2) or (ii == 3): #Axis labels for panels second row
        ax.set_xlabel("Colour difference", fontsize = 18)

#fig.show()
#fig.savefig(path  + "random_effects_reduced.jpg",bbox_inches= 'tight', dpi = 300) #Saves figure as .jpg in local path

# %%codecell

#### EXAMPLE 2: GRAPHICAL REPRESENTATION OF BIVARIATES COPULAS MODELLING 2-D
# DENSITY DISTRIBUTIONS REPRESENTING FLOWER COLOUR VARIABILITY FOR THREE FLOWER
# SPECIES CONSIDERING FLY COLOUR VISION ####

# %%codecell LOADS COLOUR LOCI FROM DISTRIBUTIONS FITTED IN R AVAILABLE AS .CSV
knaut_fly_thresh = knaut_fly[(knaut_fly['CDF'] > 0.25) & (knaut_fly['CDF'] <= 0.75)] #Calculates the first and third quantile of colour loci distribution for each species representing the colours more often displayed by each species
scab_fly_thresh = scab_fly[(scab_fly['CDF'] > 0.25) & (scab_fly['CDF'] <= 0.75)]
trauns_fly_thresh = trauns_fly[(trauns_fly['CDF'] > 0.25) & (trauns_fly['CDF'] < 0.75)]

# %%codecell CALCULATES COLOUR DIFFERENCE BETWEEN TYPICAL COLOUR (MEAN) AND SIMULATED COLOURS AS EUCLIDEAN DISTANCE
knaut_fly_typical_dc = distance.cdist(np.array([[0.587, 1.06]]), knaut_fly_thresh.iloc[:,0:2])
scab_fly_typical_dc = distance.cdist(np.array([[0.541, 1.06]]), scab_fly_thresh.iloc[:,0:2])
trauns_fly_typical_dc = distance.cdist(np.array([[0.509, 1.01]]), trauns_fly_thresh.iloc[:,0:2])

np.quantile(knaut_fly_typical_dc, (0.025, 0.5, 0.975)) # 95 % CI, minimum and maximum colour difference between the rewarding and mimic species
knaut_fly_typical_dc.min()
knaut_fly_typical_dc.max()

np.quantile(scab_fly_typical_dc, (0.025, 0.5, 0.975))
scab_fly_typical_dc.min()
scab_fly_typical_dc.max()


# %%codecell CONTOUR MAP REPRESENTING THE DISTRIBUTION OF COLOUR LOCI
# AND THE FREQUENCY DISTRIBUTION OF COLOUR DIFFERENCES PRODUCED BY COLOUR VARIABILITY FOR EACH SPECIES AS HISTOGRAMS
fig = plt.figure(figsize = (12,15))
ax = fig.add_subplot(3,2,1)

#PANEL A: CONTOUR MAP REPRESENTING COLOUR LOCI DISTRIBUTION FOR KNAUTIA FLOWERS
ax.scatter(knaut_fly["x_prime"], knaut_fly["y_prime"], c = "magenta", marker = "D", alpha = 0.05)
knaut_cont_F = ax.contour(fly_knautia_x, fly_knautia_y, fly_knautia_Z,
colors = "black", alpha = 0.7)
ax.scatter(0.588, 1.05, marker = "D", s = 80, c = 'red')
ax.set_xlim(0.35, 0.95)
ax.set_ylim(0.975, 1.16)
leg_fly_elem1 = [mlines.Line2D([],[], color = "magenta", marker = "D", alpha = 0.2,
ls = 'None', label = 'Knautia colour loci', markersize = 9),
mlines.Line2D([],[], color = "red", marker = "D", markersize = 9,
ls = 'None', label = 'Typical Knautia\ncolour (mode)'),
mlines.Line2D([],[], color = "black", ls = "-", label = 'Knautia colour density')]
ax.legend(handles = leg_fly_elem1, loc = "upper right")
ax.set_xlabel("x'", fontsize = 13)
ax.set_ylabel("y'", fontsize = 13)
ax.text(0.225, 1.155, "a.", fontsize = 18, weight = "bold")

#PANEL B: HISTOGRAM REPRESENTING FREQUENCY DISTRIBUTION OF COLOUR DIFFERENCES PRODUCED BY KNAUTIA COLOUR VARIABILITY
ax2 = fig.add_subplot(3,2,2)
ax2.hist(knaut_fly_typical_dc.reshape(735,1), color = "magenta", density = False,
bins = 20, alpha = 0.25)
ax2.vlines(np.median(knaut_fly_typical_dc), 0, 150, ls = "--", lw = 2, colors = 'red')
ax2.set_xlim(0, 0.42)
ax2.set_ylim(0, 100)
ax2.set_xlabel("Colour distance from a typical Knautia\nto its more frequent colour variants")
ax2.set_ylabel("Ocurrences")
ax2.text(-0.07, 97, "b.", fontsize = 18, weight = 'bold')


#PANEL C: CONTOUR MAP REPRESENTING COLOUR LOCI DISTRIBUTION FOR SCABIOLA FLOWERS
ax3 = fig.add_subplot(3,2,3)
ax3.scatter(scab_fly["x_prime"], scab_fly["y_prime"], c = "blue", marker = "D", alpha = 0.05)
scab_fly_contour = ax3.contour(fly_scab_x, fly_scab_y, fly_scab_Z,
colors = "black", alpha = 0.7)
ax3.scatter(0.493, 1.05, marker = "D", s = 80, c = 'red')
ax3.set_xlim(0.35, 0.95)
ax3.set_ylim(0.975, 1.16)
leg_fly_elem2 = [mlines.Line2D([],[], color = "blue", marker = "D", alpha = 0.2,
ls = 'None', label = 'Scabiosa colour loci', markersize = 9),
mlines.Line2D([],[], color = "red", marker = "D", markersize = 9,
ls = 'None', label = 'Typical Scabiosa\ncolour (mode)'),
mlines.Line2D([],[], color = "black", ls = "-", label = 'Scabiosa colour density')]
ax3.legend(handles = leg_fly_elem2, loc = "upper right")
ax3.set_xlabel("x'", fontsize = 13)
ax3.set_ylabel("y'", fontsize = 13)
ax3.text(0.225, 1.155, "c.", fontsize = 18, weight = "bold")

#PANEL D: HISTOGRAM REPRESENTING FREQUENCY DISTRIBUTION OF COLOUR DIFFERENCES PRODUCED BY SCABIOLA COLOUR VARIABILITY
ax4 = fig.add_subplot(3,2,4)
ax4.hist(scab_fly_typical_dc.reshape(839,1), color = "blue", density = False,
bins = 20, alpha = 0.25)
ax4.vlines(np.median(scab_fly_typical_dc), 0, 260, ls = "--", lw = 2, colors = "red")
ax4.set_xlim(0, 0.42)
ax4.set_ylim(0, 260)
ax4.set_xlabel("Colour distance from a typical Scabiosa\nto its more frequent colour variants")
ax4.set_ylabel("Occurrences")
ax4.text(-0.07, 252, "d.", fontsize = 18, weight = 'bold')

#PANEL E: CONTOUR MAP REPRESENTING COLOUR LOCI DISTRIBUTION FOR TRAUNSTEINERA FLOWERS
ax5 = fig.add_subplot(3,2,5)
ax5.set_xlim(0.35, 0.95)
ax5.set_ylim(0.975, 1.16)
trauns_cont_F = ax5.contour(fly_trauns_x, fly_trauns_y, fly_trauns_Z, colors = "black",
alpha = 0.7)
ax5.scatter(trauns_fly["x_prime"], trauns_fly["y_prime"], marker = "D",
c = "purple", alpha = 0.05)
ax5.scatter(0.508589, 1.009551, c = "red", marker = "D", s = 80)
ax5.set_xlabel("x'", fontsize = 13)
ax5.set_ylabel("y", fontsize = 13)
leg_fly_elem3 = [mlines.Line2D([],[], color = "purple", marker = "D", alpha = 0.2,
ls = 'None', label = 'Traunsteinera colour loci', markersize = 9),
mlines.Line2D([],[], color = "red", marker = "D", markersize = 9,
ls = 'None', label = 'Typical Traunsteinera\ncolour (mode)'),
mlines.Line2D([],[], color = "black", ls = "-", label = "Traunsteinera colour density")]
ax5.legend(handles = leg_fly_elem3, loc = "upper right")
ax5.text(0.225, 1.155, "e.", fontsize = 18, weight = "bold")

#PANEL F: HISTOGRAM REPRESENTING FREQUENCY DISTRIBUTION OF COLOUR DIFFERENCES PRODUCED BY TRAUNSTEINERA COLOUR VARIABILITY
ax6 = fig.add_subplot(3,2,6)
ax6.set_ylim(0, 100)
ax6.set_xlim(0, 0.40)
ax6.hist(trauns_fly_typical_dc.reshape(759,1), color = "purple", density = False,
bins = 20, alpha = 0.25)
ax6.vlines(np.median(trauns_fly_typical_dc), 0, 100, ls = "--", lw = 2, colors = 'red')
ax6.set_ylabel("Ocurrences")
ax6.set_xlabel("Colour distance from a typical Traunsteinera\nto its more frequent colour variants")
ax6.text(-0.07, 100, "f.", fontsize = 18, weight = 'bold')

#fig.savefig(path + "fly_colour_densities.jpg", dpi = 300, bbox_inches = 'tight') #Saves figure in path for local machine
