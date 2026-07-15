#!/usr/bin/env python
# coding: utf-8

# In[60]:


get_ipython().run_line_magic('pip', 'install numpy matplotlib ipympl astropy photutils ltsfit')


# In[61]:


import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt


# # Obtaining data for ALMA, Spitzer and GALEX

# In[62]:


M100_data = '/Users/jacobjones/Downloads/M100_combine_CO_cube.image.mom0.pbcor.fits'
hdul = fits.open(M100_data)
hdul.info()


# In[63]:


data = hdul[0].data
header = hdul[0].header
data = data.squeeze()  ##removes the unnecessary dimensions of array of data
print(data.shape) 


# In[64]:


print(header)
from astropy.wcs import WCS 
wcs = WCS(header, naxis=2)


# In[65]:


def onclick(event):
    x, y = event.xdata, event.ydata  
    plt.plot(x, y, "r+")  
    xy.append((x, y))



# In[66]:


get_ipython().run_line_magic('matplotlib', 'widget')
plt.imshow(data, norm='log')


plt.show()


# In[67]:


plt.title("Click on CO emission regions")
xy = [] # Initializes coordinates
plt.connect("button_press_event", onclick)


# In[68]:


plt.close()
get_ipython().run_line_magic('matplotlib', 'inline')


# In[69]:


print(f"Total clicks: {len(xy)}")
print(f"Pixel coordinates: {xy}")


# In[70]:


xy_array = np.array(xy)
ra, dec = wcs.all_pix2world(xy_array[:, 0], xy_array[:, 1], 0)
CO_data = np.vstack([ra, dec])
np.savetxt('CO_emission_regions.txt', CO_data)


# In[71]:


def onclick(event):
    x, y = event.xdata, event.ydata  
    plt.plot(x, y, "r+")  
    xy.append((x, y))



# In[72]:


get_ipython().run_line_magic('matplotlib', 'widget')
plt.imshow(data, norm='log')


plt.show()


# In[73]:


plt.title("Click on CO background emission regions")
xy = [] # Initializes coordinates
plt.connect("button_press_event", onclick)


# In[74]:


plt.close()
get_ipython().run_line_magic('matplotlib', 'inline')


# In[75]:


print(f"Total clicks: {len(xy)}")
print(f"Pixel coordinates: {xy}")


# In[76]:


xy_array = np.array(xy)
ra, dec = wcs.all_pix2world(xy_array[:, 0], xy_array[:, 1], 0)
CO_background_data = np.vstack([ra, dec])
np.savetxt('CO_background_emission_regions.txt', CO_background_data)


# ### Calculating the reduced mass of the CO molecule

# In[77]:


m_C = 1.99248e-26  # kg
m_O = 2.65654e-26  # kg

mu = m_C * m_O / (m_C + m_O)
print(f"Reduced mass = {mu:.5e} kg")


# ### Calculating the frequency displacement in the CO for M100

# In[78]:


f0 = 115e9   # Hz (frequency in source's rest frame)
z = 0.00524  # redshift of M100

delta_f = z * f0
print(f"Frequency displacement = {delta_f:.4e} Hz")
print(f"Frequency displacement = {delta_f/1e6:.2f} MHz")


# In[79]:


hdul_spitzer = fits.open('/Users/jacobjones/Downloads/NGC_4321_I_MIPS24_bgm2012.fits')
data_spitzer = hdul_spitzer[0].data
header_spitzer = hdul_spitzer[0].header
data_spitzer = data_spitzer.squeeze()
wcs_spitzer = WCS(header_spitzer, naxis=2)
print(data_spitzer.shape)


# In[80]:


def onclick(event):
    x, y = event.xdata, event.ydata  
    plt.plot(x, y, "r+")  
    xy.append((x, y))



# In[81]:


get_ipython().run_line_magic('matplotlib', 'widget')
plt.imshow(data_spitzer, norm='log')


plt.show()


# In[82]:


plt.title("Click on background emission regions")
xy = [] # Initializes coordinates
plt.connect("button_press_event", onclick)
#Larger radii to ensure we are selecting regions of emission due to the dust and not the stars
#Hard to distinguish between dust and gas near centre where the star density is high


# In[83]:


plt.close()
get_ipython().run_line_magic('matplotlib', 'inline')


# In[84]:


print(f"Total clicks: {len(xy)}")
print(f"Pixel coordinates: {xy}")


# In[85]:


xy_array = np.array(xy)
ra, dec = wcs.all_pix2world(xy_array[:, 0], xy_array[:, 1], 0)
Spitzer_data = np.vstack([ra, dec])
np.savetxt('Spitzer_background_emission_regions.txt', Spitzer_data)


# In[86]:


hdul_galex = fits.open('/Users/jacobjones/Downloads/NGC_4321_GALEX_NUV_bms2014.fits')
data_galex = hdul_galex[0].data
header_galex = hdul_galex[0].header
data_galex = data_galex.squeeze()
print(data_galex.shape)
wcs_spitzer = WCS(header_galex, naxis=2)


# In[87]:


def onclick(event):
    x, y = event.xdata, event.ydata  
    plt.plot(x, y, "r+")  
    xy.append((x, y))



# In[88]:


get_ipython().run_line_magic('matplotlib', 'widget')
plt.imshow(data_galex, norm='log')


plt.show()


# In[89]:


plt.title("Click on galex background emission regions")
xy = [] # Initializes coordinates
plt.connect("button_press_event", onclick)


# In[90]:


plt.close()
get_ipython().run_line_magic('matplotlib', 'inline')


# In[91]:


print(f"Total clicks: {len(xy)}")
print(f"Pixel coordinates: {xy}")


# In[92]:


xy_array = np.array(xy)
ra, dec = wcs.all_pix2world(xy_array[:, 0], xy_array[:, 1], 0)
Galex_data = np.vstack([ra, dec])
np.savetxt('Galex_background_emission_regions.txt', Galex_data)


# ### Comparing the Spitzer image with the GALEX

# Similarities:
# Same spiral arms observed from both telescopes as both measure the same stellar populations.
# Where there are lots of young stars, a large amount of UV will be emitted but there will also be 
# a large amount of gas and dust since these are what form young stars. UV heats up neaby gas, and this gas emits in the MIR range so a large amount of MIR will also be emitted
# 
# Differences:
# GALEX images of M100 appears smoother, whereas Spitzer's image is sharper and clumpier. This is likely due to there being high concentrations of and gas in clouds as compared to other areas hence making the image appear clumpy.

# # Measuring the Emission

# Assign each region a position in the sky and an aperture of a certain radius.
# Sum up all of the emissions in these apertures to get a measure of the flux in each region

# In[93]:


ra, dec = np.loadtxt('/Users/jacobjones/Downloads/CO_emission_regions.txt')
ra_bg, dec_bg = np.loadtxt('/Users/jacobjones/Downloads/CO_background_emission_regions.txt')
#RA values are the 1st row, DEC values are the 2nd


# In[94]:


from astropy.coordinates import SkyCoord
from photutils.aperture import SkyCircularAperture
import astropy.units as u


# In[95]:


#assign positions to CO emission regions
positions = SkyCoord(ra=ra*u.degree, dec=dec*u.degree) 
#create circular apertures of radius 10 arcseconds
aperture = SkyCircularAperture(positions, r=10*u.arcsec)
print(aperture)


# In[96]:


#assign positions to background CO emissions
positions_bg = SkyCoord(ra=ra_bg*u.degree, dec=dec_bg*u.degree)

#create circular apertures of radius 10 arcseconds
aperture_bg = SkyCircularAperture(positions_bg, r=10*u.arcsec)
print(aperture_bg)


# In[97]:


#Masking blank pixels
mask = np.isnan(data)
print(f"Mask shape: {mask.shape}")
print(f"Number of masked pixels: {np.sum(mask)}")
print(f"Number of valid pixels: {np.sum(~mask)}") #flips boolean values


# In[106]:


from photutils.aperture import aperture_photometry
#Summing up the pixels 

#Run aperture photometry on CO emission regions
phot_table = aperture_photometry(data, aperture, mask=mask, wcs=wcs)
print(phot_table)

CO_flux = np.array(phot_table)
print(f"CO flux values: {CO_flux}")


# In[102]:


#Run aperture photometry on background regions
phot_table_bg = aperture_photometry(data, aperture_bg, mask=mask, wcs=wcs)

#Extract background flux sums
CO_flux_bg = np.array(phot_table_bg['aperture_sum'])
#print(f"Background flux values: {CO_flux_bg}")


# In[110]:


#Calculate mean background and subtract this from each of the emission fluxes
bg_mean = np.mean(CO_flux_bg)
print(f"Mean background: {bg_mean}")

CO_flux_bgsub = CO_flux - bg_mean


# In[135]:


#Poisson noise - square root of the flux in each region
poisson_noise = np.sqrt(np.abs(CO_flux_bgsub))

#RMS scatter of background aperture sums
rms_bg = np.std(CO_flux_bg)
print(f"RMS background scatter: {rms_bg}")

#Calibration uncertainty (3% for ALMA) 
calibration_uncertainty = 0.03 * np.abs(CO_flux_bgsub) #given in section 6 of labscript

#Combine all three uncertainties in quadrature
CO_error = np.sqrt(poisson_noise**2 + rms_bg**2 + calibration_uncertainty**2)

print(f"Background subtracted fluxes: {CO_flux_bgsub}")
print(f"Total uncertainties: {co_error}")


# In[136]:


hdul_galex = fits.open('/Users/jacobjones/Downloads/NGC_4321_GALEX_NUV_bms2014.fits')
data_galex = hdul_galex[0].data
header_galex = hdul_galex[0].header
data_galex = data_galex.squeeze()
wcs_galex = WCS(header_galex, naxis=2)


#create mask
mask_galex = np.isnan(data_galex)

#Same emission apertures (positions already defined from CO)
phot_table_galex = aperture_photometry(data_galex, aperture, mask=mask_galex, wcs=wcs_galex)
galex_flux = np.array(phot_table_galex['aperture_sum'])


#Load GALEX background regions
bg_data_galex = np.loadtxt('/Users/jacobjones/Downloads/GALEX_background_emission_regions.txt')
ra_bg_galex = bg_data_galex[0]
dec_bg_galex = bg_data_galex[1]

#Create background apertures
positions_bg_galex = SkyCoord(ra=ra_bg_galex*u.degree, dec=dec_bg_galex*u.degree)
aperture_bg_galex = SkyCircularAperture(positions_bg_galex, r=10*u.arcsec)

#Measure background
phot_table_bg_galex = aperture_photometry(data_galex, aperture_bg_galex, mask=mask_galex, wcs=wcs_galex)
galex_flux_bg = np.array(phot_table_bg_galex['aperture_sum'])

#Background subtraction
galex_bg_mean = np.mean(galex_flux_bg)
galex_flux_bgsub = galex_flux - galex_bg_mean

#Error estimation (GALEX 3%)
galex_poisson = np.sqrt(np.abs(galex_flux_bgsub))
galex_rms = np.std(galex_flux_bg)
galex_cal = 0.03 * np.abs(galex_flux_bgsub)
galex_error = np.sqrt(galex_poisson**2 + galex_rms**2 + galex_cal**2)
print(f"GALEX fluxes: {galex_flux_bgsub}")
print(f"GALEX errors: {galex_error}")


# In[130]:


hdul_spitzer = fits.open('/Users/jacobjones/Downloads/NGC_4321_I_MIPS24_bgm2012.fits')
data_spitzer = hdul_spitzer[0].data
header_spitzer = hdul_spitzer[0].header

data_spitzer = data_spitzer.squeeze()
wcs_spitzer = WCS(header_spitzer, naxis=2)


#Create mask
mask_spitzer = np.isnan(data_spitzer)

#Sum to get flux
phot_table_spitzer = aperture_photometry(data_spitzer, aperture, mask=mask_spitzer, wcs=wcs_spitzer)
spitzer_flux = np.array(phot_table_spitzer['aperture_sum'])

#Load Spitzer background regions
bg_data_spitzer = np.loadtxt('/Users/jacobjones/Downloads/Spitzer_background_emission_regions.txt')
ra_bg_spitzer = bg_data_spitzer[0]
dec_bg_spitzer = bg_data_spitzer[1]

#Create background apertures
positions_bg_spitzer = SkyCoord(ra=ra_bg_spitzer*u.degree, dec=dec_bg_spitzer*u.degree)
aperture_bg_spitzer = SkyCircularAperture(positions_bg_spitzer, r=10*u.arcsec)

#Background flux
phot_table_bg_spitzer = aperture_photometry(data_spitzer, aperture_bg_spitzer, mask=mask_spitzer, wcs=wcs_spitzer)
spitzer_flux_bg = np.array(phot_table_bg_spitzer['aperture_sum'])

#Background subtraction
spitzer_bg_mean = np.mean(spitzer_flux_bg)
spitzer_flux_bgsub = spitzer_flux - spitzer_bg_mean

#Error (Spitzer calibration uncertainty = 4%)
spitzer_poisson = np.sqrt(np.abs(spitzer_flux_bgsub))
spitzer_rms = np.std(spitzer_flux_bg)
spitzer_cal = 0.04 * np.abs(spitzer_flux_bgsub)
spitzer_error = np.sqrt(spitzer_poisson**2 + spitzer_rms**2 + spitzer_cal**2)
print(f"Spitzer fluxes: {spitzer_flux_bgsub}")
print(f"Spitzer errors: {spitzer_error}")


# # Plotting Star Formation Rate against Mass of Molecular Gas

# In[131]:


#Converting from counts/sec to Janskys
galex_flux_jy = galex_flux_bgsub * 3.365e-5
galex_error_jy = galex_error * 3.365e-5
print(f"GALEX flux in Jy: {galex_flux_jy}")
print(f"GALEX error in Jy: {galex_error_jy}")


# In[132]:


#Convert Spitzer from MJy/sr to Jy/arcsec2
spitzer_flux_jy_arcsec = spitzer_flux_bgsub * 2.35e-5
spitzer_error_jy_arcsec = spitzer_error * 2.35e-5

#Convert from Jy/arcsec2 to Jy by multiplying by pixel area
pixel_area_spitzer = 2.25  # arcsec^2
spitzer_flux_jy = spitzer_flux_jy_arcsec * pixel_area_spitzer
spitzer_error_jy = spitzer_error_jy_arcsec * pixel_area_spitzer
print(f"Spitzer flux in Jy: {spitzer_flux_jy}")
print(f"Spitzer error in Jy: {spitzer_error_jy}")


# In[137]:


#Convert CO from Jy/beam km/s to Jy/arcsec2 km/s
beam_area = 10.78  # arcsec^2
pixel_area_CO = 0.25  # arcsec^2

CO_flux_jy = (CO_flux_bgsub / beam_area) * pixel_area_CO
CO_error_jy = (CO_error / beam_area) * pixel_area_CO
print(f"CO flux in Jy km/s: {CO_flux_jy}")
print(f"CO error in Jy km/s: {CO_error_jy}")


# In[141]:


#Calulating star formation rate

#Distance to M100 in Megaparsecs
D = 15.2  # Mpc

#Calculating the star formation rate for each region
SFR = 0.106 * (galex_flux_jy + 0.02013 * spitzer_flux_jy) * D**2 #measured in solar masses per year

print(f"Star formation rates (M_sun/yr): {SFR}")


# In[142]:


#Propagate errors through the SFR equation
#SFR = 0.106 * (NUV + 0.02013 * MIR) * D^2
#error on (NUV + 0.02013*MIR) found by combining in quadrature
SFR_error = 0.106 * D**2 * np.sqrt(galex_error_jy**2 + (0.02013 * spitzer_error_jy)**2)

print(f"SFR uncertainties (M_sun/yr): {SFR_error}")


# In[144]:


#Convert CO from Jy/beam km/s to Jy/arcsec2 km/s
beam_area = 10.78  # arcsec^2
pixel_area_CO = 0.25  # arcsec^2

CO_flux_jy = (CO_flux_bgsub / beam_area) * pixel_area_CO
CO_error_jy = (CO_error / beam_area) * pixel_area_CO

#Calculating the molecular gas mass
MassMolGas = 7860 * CO_flux_jy * D**2 #in solar masses
MassMolGas_error = 7860 * CO_error_jy * D**2

print(f"Molecular gas masses (solar masses): {MassMolGas}")
print(f"Molecular gas mass errors: {MassMolGas_error}")


# In[147]:


log_MassMolGas = np.log10(np.abs(MassMolGas))
log_SFR = np.log10(np.abs(SFR))

#Propagate errors into log
#error in log10(x) = error(x) / (x * ln(10))
log_MassMolGas_error = MassMolGas_error / (np.abs(MassMolGas) * np.log(10))
log_SFR_error = SFR_error / (np.abs(SFR) * np.log(10))

print(f"Log of molecular gas mass: {log_MassMolGas}")
print(f"Log of SFR: {log_SFR}")


# In[165]:


plt.figure(figsize=(8.5, 6))
plt.errorbar(log_MassMolGas, log_SFR, 
             xerr=log_MassMolGas_error, 
             yerr=log_SFR_error,fmt='o',capsize=4,color='purple', label='M100 regions')
plt.xlabel('log$_{10}$(Molecular Gas Mass) [M$_\odot$]')
plt.ylabel('log$_{10}$(Star Formation Rate) [M$_\odot$/yr]')
plt.title('Kennicutt-Schmidt Relation for M100')
plt.legend()
plt.grid(True)
plt.show()


# Greatest source of uncertainty:
# For bright regions the calibration uncertainty dominates as it scales with the flux (larger flux hence larger calibration uncertainty)
# For dim regions, the background noise dominates as the signal is small so the average background noise becomes relatively large in comparison
# 
# 
# Effect of aperture size:
# Larger aperture: more total flux, lower percentage uncertainty, but risks including neighbouring emission regions.
# Narrower aperture:reduces flux from neighbours getting in the way, but may miss flux from extended sources and has fewer pixels so higher relative noise

# In[166]:


get_ipython().run_line_magic('pip', 'install ltsfit')


# # Statistical Significance 

# Null hypothesis: there is no correlatiopn between star formation rate and mass of molecular gas.
# Alternative hypothesis: there exists a relationship between STR and molecular mass 

# In[168]:


from ltsfit.lts_linefit import lts_linefit

#Run linear fit
fit = lts_linefit(log_MassMolGas, log_SFR, log_MassMolGas_error, log_SFR_error)


# In[170]:


print(fit.__dict__)


# In[176]:


print(f"Slope: {fit.ab[1]:.3f} +/- {fit.ab_err[1]:.3f}")
print(f"Intercept: {fit.ab[0]:.3f} +/- {fit.ab_err[0]:.3f}")
print(f"Pearson correlation coefficient with its p-value: {0.90}, 9.3e-11 ")
print(f"Spearman correlation coefficient with its p-value: {0.79}, 1.6e-17")


# The values of p = 9.3e-11 and p = 1.6e-17 are essentially zero meaning there is an almost negligible probability that the correlation between molecular gas mass and star formation rate in M100 is a coincidence. The Kennicutt-Schmidt relation is statistically significant and thus we reject the null hypothesis.

# In[192]:


#create the mask
mask_fit = fit.mask
print(f"Included in fit: {np.sum(mask_fit)}")
print(f"Clipped as outliers: {np.sum(~mask_fit)}")

CO_emissions_data = np.loadtxt('/Users/jacobjones/Downloads/CO_emission_regions.txt')
ra = CO_emissions_data[0]
dec = CO_emissions_data[1]

#separate RA/DEC into included and clipped groups
ra_included = ra[mask_fit]
dec_included = dec[mask_fit]
ra_outlier = ra[~mask_fit]
dec_outlier = dec[~mask_fit]


# ### Convert from wcs back to pixels

# In[193]:


# ALMA pixel coordinates
x_co_in, y_co_in = wcs.all_world2pix(ra_included, dec_included, 0)
x_co_out, y_co_out = wcs.all_world2pix(ra_outlier, dec_outlier, 0)

# GALEX pixel coordinates
x_galex_in, y_galex_in = wcs_galex.all_world2pix(ra_included, dec_included, 0)
x_galex_out, y_galex_out = wcs_galex.all_world2pix(ra_outlier, dec_outlier, 0)

# Spitzer pixel coordinates
x_spitzer_in, y_spitzer_in = wcs_spitzer.all_world2pix(ra_included, dec_included, 0)
x_spitzer_out, y_spitzer_out = wcs_spitzer.all_world2pix(ra_outlier, dec_outlier, 0)


# ### Plot on ALMA image

# In[202]:


fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(data, norm='log')
ax.scatter(x_co_in, y_co_in, marker='o', s=30, 
           facecolors='none', edgecolors='green', label='Included')
ax.scatter(x_co_out, y_co_out, marker='o', s=30, 
           facecolors='none', edgecolors='red', label='Outlier')
ax.set_title('ALMA CO image')
ax.legend()
plt.show()


# ### Plot on GALEX image

# In[201]:


fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(data_galex, norm='log')
ax.scatter(x_galex_in, y_galex_in, marker='o', s=30, 
           facecolors='none', edgecolors='green', label='Included')
ax.scatter(x_galex_out, y_galex_out, marker='o', s=30, 
           facecolors='none', edgecolors='red', label='Outlier')
ax.set_title('GALEX NUV image')
ax.legend()
plt.show()


# In[204]:


fig, ax = plt.subplots(figsize=(8, 8))
plt.imshow(data_spitzer, norm='log')
plt.scatter(x_spitzer_in, y_spitzer_in, marker='o', s=30, 
           facecolors='none', edgecolors='green', label='Included')
plt.scatter(x_spitzer_out, y_spitzer_out, marker='o', s=30, 
           facecolors='none', edgecolors='red', label='Outlier')
ax.set_title('Spitzer MIR image')
plt.legend()
plt.show()


# If it was found that p > 0.05 between two quantities, then we would accept the null hypothesis. This would imply that there would be very little/no overlap between regions of CO emission and NUV emissions. 

# In[ ]:




