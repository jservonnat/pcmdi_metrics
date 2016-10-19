def varlongname(variable):
   """
   Returns the long name of variable
   """
   longvarname = variable
   # -- ATMOSPHERE VARIABLES
   if variable=='tas':
        longvarname  = '2M Temperature'
        shortvarname = '2M Temp.'
   if variable=='pr':
        longvarname  = 'Precipitation'
        shortvarname = 'Precip.'
   if variable=='psl':
        longvarname  = 'Sea Level Pressure'
        shortvarname = 'Sea Level Pres.'
   if variable=='ua':
        longvarname  = 'Zonal Wind'
        shortvarname = 'U-Wind'
   if variable=='va':
        longvarname  = 'Meridional Wind'
        shortvarname = 'V-Wind'
   if variable=='ta':
        longvarname  = 'Air Temperature'
        shortvarname = 'Air Temp.'
   if variable=='hus':
        longvarname  = 'Specific Humidity'
        shortvarname = 'Sp. Humidity'
   if variable=='huss':
        longvarname  = 'Specific Humidity at Surface'
        shortvarname = 'Sp. Humidity (surf)'
   if variable=='rstt':
        longvarname  = 'Rad SW Total TOA'
        shortvarname = 'Rad SW Total TOA'
   if variable=='rsts':
        longvarname  = 'Total SW rad surface'
        shortvarname = 'Total SW rad surf.'
   if variable=='rtt':
        longvarname  = 'Total Radiation TOA'
        shortvarname = 'Total Rad. TOA'
   if variable=='crelt':
        longvarname  = 'Longwave Cloud Radiative Effect TOA'
        shortvarname = 'LW CRE TOA'
   if variable=='crest':
        longvarname  = 'Shortwave Cloud Radiative Effect TOA'
        shortvarname = 'SW CRE TOA'
   if variable=='crett':
        longvarname  = 'Total CRE TOA'
        shortvarname = 'Total CRE TOA'
   if variable=='hfls':
        longvarname  = 'Latent Heat Flux'
        shortvarname = 'Latent HF'
   if variable=='hfss':
        longvarname  = 'Sensible Heat Flux'
        shortvarname = 'Sensible HF'
   if variable=='hfns':
        longvarname  = 'Surface Total Heat Flux'
        shortvarname = 'Surf. Tot. HF'
   if variable=='zg500':
        longvarname  = '500mb geopotential height'
        shortvarname = ''
   if variable=='rsut':
        longvarname  = 'Upward SW rad TOA'
        shortvarname = ''
   if variable=='rlut':
        longvarname  = 'Outgoing Long Wave Radiation'
        shortvarname = 'OLR'
   if variable=='rlutcs':
        longvarname  = 'Clear Sky OLR'
        shortvarname = 'Clear sky OLR'
   if variable=='albs':
        longvarname  = 'Surface albedo'
        shortvarname = ''
   if variable=='albt':
        longvarname  = 'Planetary albedo'
        shortvarname = ''
   if variable=='cress':
        longvarname  = 'SW CRE surface'
        shortvarname = ''
   if variable=='crels':
        longvarname  = 'LW CRE surface'
        shortvarname = ''
   if variable=='crets':
        longvarname  = 'Total CRE surface'
        shortvarname = ''
   if variable=='rts':
        longvarname  = 'Total radiation surface'
        shortvarname = ''
   if variable=='rah':
        longvarname  = 'Atm. Rad. Heat.'
        shortvarname = ''
   if variable=='rahcs':
        longvarname  = 'Atm. Rad. Heat. - clear sky'
        shortvarname = ''
   if variable=='rahcre':
        longvarname  = 'Atm. rad. Heat. - CRE'
        shortvarname = ''
   if variable=='rsah':
        longvarname  = 'Atm. SW Heat.'
        shortvarname = ''
   if variable=='rsahcs':
        longvarname  = 'Atm. SW Heat. - Clear sky'
        shortvarname = ''
   if variable=='rsahcre':
        longvarname  = 'Atm. SW Heat. - CRE'
        shortvarname = ''
   if variable=='rlah':
        longvarname  = 'Atm. LW Heat.'
        shortvarname = ''
   if variable=='rlahcs':
        longvarname  = 'Atm. LW Heat. - Clear sky'
        shortvarname = ''
   if variable=='rlahcre':
        longvarname  = 'Atm. LW Heat. - CRE'
        shortvarname = ''
   if variable=='cltcalipso':
        longvarname  = 'Total Cloud Cover'
        shortvarname = ''
   if variable=='cllcalipso':
        longvarname  = 'Low Cloud Cover'
        shortvarname = ''
   if variable=='clmcalipso':
        longvarname  = 'Medium Cloud Cover'
        shortvarname = ''
   if variable=='clhcalipso':
        longvarname  = 'High Cloud Cover'
        shortvarname = ''
   if variable=='rlds':
        longvarname  = 'Downward LW rad at Surface'
        shortvarname = ''
   if variable=='rldscs':
        longvarname  = 'Upward LW rad at Surface - Clear Sky'
        shortvarname = ''
   if variable=='hurs':
        longvarname  = 'Relative Humidity at Surface'
        shortvarname = ''
   if variable=='rlus':
        longvarname  = 'Upward SW rad at Surface'
        shortvarname = ''
   if variable=='rsdscs':
        longvarname  = 'Downward SW rad at Surface - Clear Sky'
        shortvarname = ''
   if variable=='rsds':
        longvarname  = 'Downward SW rad at Surface'
        shortvarname = ''
   if variable=='rsucs':
        longvarname  = 'Upward SW rad at Surface - Clear Sky'
        shortvarname = ''
   if variable=='rsutcs':
        longvarname  = 'Upward SW rad at TOA - Clear Sky'
        shortvarname = ''
   #
   # -- OCEAN VARIABLES
   if variable=='tos':
        longvarname  = 'Sea Surface Temperature'
   if variable=='sos':
        longvarname  = 'Sea Surface Salinity'
   if variable=='zos':
        longvarname  = 'Sea Surface Height'
   if variable=='to200':
        longvarname  = 'Potential Temperature at 200m'
   if variable=='to1000':
        longvarname  = 'Potential Temperature at 1000m'
   if variable=='to2000':
        longvarname  = 'Potential Temperature at 2000m'
   if variable=='so200':
        longvarname  = 'Salinity at 200m'
   if variable=='so1000':
        longvarname  = 'Salinity at 1000m'
   if variable=='so2000':
        longvarname  = 'Salinity at 2000m'
   if variable=='mlotst':
        longvarname  = 'MLD (SigmaT 0.03)'
   if variable=='wfo':
        longvarname  = 'E-P Budget'
   if variable=='tauu':        
        longvarname  = 'Zonal Wind Stress'
   if variable=='tauv':        
        longvarname  = 'Meridional Wind Stress'
   if variable=='hfls':        
        longvarname  = 'Latent Heat Flux'
   if variable=='hfss':        
        longvarname  = 'Sensible Heat Flux'
   if variable=='sic':        
        longvarname  = 'Sea Ice Concentration'
   if variable=='sit':
        longvarname  = 'Sea Ice Thickness'
   if variable=='thetao':
        longvarname  = 'Potential Temperature'
   if variable=='so':
        longvarname  = 'Salinity'
   if variable.lower()=='moc':
        longvarname  = 'Merid. Overturning Circulation'

   #
   return longvarname



