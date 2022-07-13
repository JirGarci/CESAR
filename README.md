# CESAR
Data files and Python script required to produce two multi-panel figures graphically summarising results from two different data analysis.

The first example represents non-linear models describing the relationship between the likelihood of accurate discrimination and colour differences for four different stimuli. The stimuli consisted of lights with dominant wavelengths at 470, 480, 490 and 500 nm. The model was constructed based on observations recorded in a behavioural experiment with pigeons. Values for these observations are available in the file wright.csv

The model is described by a power function of the form y = (a + alpha) * x^b. Where a and b are fixed terms and alpha is a random term for each stimuli. Posterior distributions for the a, alpha and b coefficients were found using Bayesian techniques with the library brms for R and are stored in the file power_disc_finction_red.csv. The four panels of Figure 1 represents the functions. Figure 1 is a sample of the results presented in the open access paper “Colour Discrimination From Perceived Differences by Birds” by Jair E Garcia, Detlef H Rohr and Adrian G Dyer available at (https://www.frontiersin.org/articles/10.3389/fevo.2021.639513/full). Please follow the link for the publication.


Figure 2 are unpublished results from a simulation predicting the effect of colour variability in the ability of pollinating hover files to discriminate Knautia longifolia and Scabiola lucida 
 rewarding flowers from non-rewarding Traunsteinera globosa mimics. 

The figure depicts two sets of data. Panels on the left column represent predicted colours for each species from a bivariate distribution function fitted to colour measurements recorded for the three species. Histograms on the right column represents the distribution of colour differences between a mean flower of each species and its various colour alternatives. Distribution of flower colours for each species were modelled using bivariate copulas in R. Details on the fitting methodology are available in the manuscript “Fly pollination drives convergence of flower coloration” by Jair E Garcia, Leah Hannah, Mani Shrestha, Martin Burd and Adrian Dyer freely available at (https://onlinelibrary.wiley.com/doi/10.1111/nph.17696) 
