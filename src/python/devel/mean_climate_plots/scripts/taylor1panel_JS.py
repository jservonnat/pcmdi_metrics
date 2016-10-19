#!/usr/bin/env python

import numpy as NP
import matplotlib.pyplot as PLT
import json
import sys, os
import string
import getopt
import pcmdi_metrics
from pcmdi_metrics.mean_climate_plots import TaylorDiagram
import argparse
from argparse import RawTextHelpFormatter

test = False
#test = True

P = argparse.ArgumentParser(
    description='Runs PCMDI Metrics Computations',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

P.add_argument("-j", "--json",
                      type = str,
                      dest = 'json',
                      help = "Path to json file")
P.add_argument("-aj", "--aux_json_path",
                      type = str,
                      dest = 'aux_json_path',
                      default = '',
                      help = "Path to auxillary json file")
P.add_argument("-v", "--variable",
                      type = str,
                      dest = 'variable',
                      default = '',
                      help = "(Case Insensitive)")
P.add_argument("-s", "--stat",
                      type = str,
                      default = 'rms',
                      help = "Statistic:\n"
                             "- Available options: bias, cor, rms")
P.add_argument("-seas", "--season",
                      type = str,
                      dest = 'season',
                      default = 'all',
                      help = "Season\n"
                             "- Available options: DJF (default), MAM, JJA, SON or all")
P.add_argument("-r", "--reference",
                      type = str,
                      dest = 'reference',
                      default = 'defaultReference',
                      help = "Reference against which the statistics are computed\n"
                             "- Available options: defaultReference (default), alternate1, alternate2")
P.add_argument("-e", "--experiment",
                      type = str,
                      dest = 'experiment',
                      default = 'historical',
                      help = "AMIP, historical or picontrol")
P.add_argument("-d", "--domain",
                      type = str,
                      dest = 'domain',
                      default = 'global',
                      help = "put options here")
P.add_argument("-p", "--parameters",
                      type = str,
                      dest = 'parameters',
                      default = '',
                      help = "")
P.add_argument("-ffs", "--figure_font_size",
                      type = str,
                      dest = 'figure_font_size',
                      default = '10',
                      help = "Font and dots size in the plots; Should remain between 10 and 15 ")
P.add_argument("-t", "--title",
                      type = str,
                      dest = 'title',
                      default = '',
                      help = "Main title (top of the page)")
P.add_argument("-yax", "--yaxis_label",
                      type = str,
                      dest = 'yaxis_label',
                      default = '',
                      help = "Label of the Y axis")
P.add_argument("-o", "--outpath",
                      type = str,
                      dest = 'outpath',
                      default = '.',
                      help = "")
P.add_argument("-hi", "--highlights",
                      type = str,
                      dest = 'highlights',
                      default = '',
                      help = "Names of the simulations (as they appear on the plot) that will be highlighted\n"
                             "with a different color than the default color (blue).\n"
                             "The user can provide a list of colors with -cl; otherwise, they will appear in green.")
P.add_argument("-cn", "--customname",
                      type = str,
                      dest = 'customname',
                      default = '',
                      help = "Custom name for the name of the simulation(s) in the plot\n"
                             "- the user can pass one customname by auxillary json file \n"
                             "  separated by commas (,) and no space => Ex: Sim1,Sim2")
P.add_argument("-kp", "--keywords",
                      type = str,
                      dest = 'keywords',
                      default = '',
                      help = "Keywords to build the name of the simulation in the plot\n"
                             "- Available options: SimulationModel, Model_period, Realization\n"
                             "- the user can pass two keywords separated by commas (), \n"
                             "  and no space => Realization,Model_period")
P.add_argument("-cl", "--colors",
                      type = str,
                      dest = 'colors',
                      default = 'g',
                      help = "Colors for the simulations in the auxillary json files\n"
                             "The user can pass either one color for all auxillary simulations or\n"
                             "or one color per json file (separated by commas=> Ex: g,b,r)")


args = P.parse_args(sys.argv[1:])

json_path = args.json
aux_json_path = args.aux_json_path
variable = args.variable
domain = args.domain
experiment = args.experiment
stat = args.stat
outpath = args.outpath
customname = args.customname
reference = args.reference
season = args.season
colors = args.colors
keywords = args.keywords
title = args.title
yaxis_label = args.yaxis_label
highlights = args.highlights
figure_font_size = args.figure_font_size

# -- Load the parameter file
if args.parameters:
   pth, fnm = os.path.split(args.parameters)
   if pth != "":
      sys.path.append(pth)
   if fnm.lower()[-3:] == ".py":
      fnm = fnm[:-3]
      ext = ".py"
   else:
      ext = ""
   # We need to make sure there is no "dot" in filename or import will fail
   if fnm.find(".") > -1:
      raise ValueError(
          "Sorry input parameter file name CANNOT contain" +
          " 'dots' (.), please rename it (e.g: %s%s)" %
          (fnm.replace(
            ".",
            "_"),
            ext))
   sys.path.insert(0, os.getcwd())
   parameters = ""  # dummy so flake8 knows about parameters
   exec("import %s as parameters" % fnm)
   if pth != "":
      sys.path.pop(-1)
   #
   # -- Main json file (CMIP)
   if hasattr(parameters, 'json_path') and not args.json:
      json_path = parameters.json_path
   # -- Auxillary json files
   if hasattr(parameters, 'aux_json_path') and not args.aux_json_path:
      aux_json_path = parameters.aux_json_path
   # -- Variable
   if hasattr(parameters, 'variable') and not args.variable:
      variable = parameters.variable
   # -- Domain
   if hasattr(parameters, 'domain') and args.domain not in 'global':
      domain = parameters.domain
   # -- experiment
   if hasattr(parameters, 'experiment') and args.experiment not in 'historical':
      experiment = parameters.experiment
   # -- stat
   if hasattr(parameters, 'stat') and args.stat not in 'rms':
      stat = parameters.stat
   # -- outpath
   if hasattr(parameters, 'outpath') and args.outpath not in '.':
      outpath = parameters.outpath
   # -- customname
   if hasattr(parameters, 'customname') and not args.customname:
      customname = parameters.customname
   # -- reference
   if hasattr(parameters, 'reference') and args.reference not in 'defaultReference':
      reference = parameters.reference
   # -- season
   if hasattr(parameters, 'season') and args.season not in 'all':
      season = parameters.season
   # -- colors
   if hasattr(parameters, 'colors') and args.colors not in 'g':
      colors = parameters.colors
   # -- keywords
   if hasattr(parameters, 'keywords') and not args.keywords:
      keywords = parameters.keywords
   # -- title
   if hasattr(parameters, 'title') and not args.title:
      title = parameters.title
   # -- yaxis_label
   if hasattr(parameters, 'yaxis_label') and not args.yaxis_label:
      yaxis_label = parameters.yaxis_label
   # -- yaxis_label
   if hasattr(parameters, 'figure_font_size') and not args.figure_font_size:
      figure_font_size = parameters.figure_font_size
   # -- highlights
   if hasattr(parameters, 'highlights') and not args.highlights:
      highlights = parameters.highlights


print '-----------------------------'
print '--'
print '-- Working on:'
print '-> json_path (-j) : '+json_path
print '-> aux_json_path (-aj) : '+aux_json_path
print '-> stat (-s) : '+stat
print '-> outpath (-o): '+outpath
print '-> experiment (-e) : '+experiment
print '-> variable (-v) : '+variable
print '-> domain (-d) : '+domain
print '-> reference (-r) : '+reference
print '-> customname (-cn) : '+customname
print '-> season (-seas) '+season
print '-> colors (-cl) '+colors
print '-> keywords (-kp) '+keywords
print '-> parameters (-p) '+args.parameters
print '-> yaxis_label (-yax) '+yaxis_label
print '-> figure_font_size (-ffs) '+figure_font_size
print '-> highlights (-hi) '+highlights
print '-----------------------------'
 
print '==> Loading json file : '+json_path
print '...'
try:
 fj = open(json_path)
 dd = json.loads(fj.read())
 fj.close()
except:
 json_path = string.replace(json_path,'@VAR',variable)
 fj = open(json_path)
 dd = json.loads(fj.read())
 fj.close()
print '==> json file loaded'

# --> aux_json_path can be a path, a json_file;
# --> It could also be possible to pass a list of json files:
# -->   - via a list
# -->   - or a dictionary with a CustomName



# -- Exploring a way to handle an auxillary json file
if aux_json_path:
   print '==> Loading auxillary json file : '+aux_json_path
   print '...'
   # -- Case: aux_json_path contains multiple paths separated by commas (,)
   aux_jsons = str.split(aux_json_path,',')
   aux_dd = dict( RESULTS=dict() ) ; inc = 1
   # -- Replace @VAR by var (if var was passed by the user)
   if variable:
       for i in xrange(len(aux_jsons)): aux_jsons[i] = str.replace(aux_jsons[i],'@VAR',variable)
   # -- Loop on the files
   for aux_json in aux_jsons:
       #
       # -- add the results to aux_mods:
       # --   - 1. if we have a custom name, use it as the new name (new_mod_name)
       # --   - 2. use keywords if we have keywords to construct the new name
       # --   - 3. add an increment to the model name if this name is already in aux_dd
       # --   -->  if not in 1, 2 or 3, leave the dictionary as it is
       aux_fj = open(aux_json)
       tmp_dict = json.loads(aux_fj.read())
       aux_fj.close()
       mod_name = tmp_dict['RESULTS'].keys()[0]
       new_mod_name = ''
       if customname:
          # - 1. if we have a custom name, use it as the new name (new_mod_name)
          customnames = str.split(customname,',')
          new_mod_name = customnames[aux_jsons.index(aux_json)]
       elif keywords:
          # - 2. use keywords if we have keywords to construct the new name
          customname_kw = str.split(keywords,',')
          for kw in customname_kw:
              if not new_mod_name:
                 new_mod_name = tmp_dict['RESULTS'][mod_name]['SimulationDescription'][kw]
              else:
                 new_mod_name = new_mod_name+' '+tmp_dict['RESULTS'][mod_name]['SimulationDescription'][kw]
       elif mod_name in aux_dd:
          # - 3. add an increment to the model name if this name is already in aux_dd
          new_mod_name = mod_name+'_'+inc
          inc = inc + 1
       if new_mod_name:
          tmp_dict['RESULTS'][new_mod_name] = tmp_dict['RESULTS'][mod_name].copy()
          tmp_dict['RESULTS'].pop(mod_name)
          #
       # -- Add the results to the auxillary dictionary
       aux_dd['RESULTS'].update( tmp_dict['RESULTS'] )
       aux_mods = aux_dd['RESULTS'].keys()
   print '==> Auxillary json file loaded'
else:
   # -- If the user gave a list of simulations via 'numexpts' in the parameter file:
   if numexpts:
      aux_dd = dict( RESULTS=dict() ) ; inc = 1
      for numexp in numexpts:
         # -- First, we see if it is a dictionary (with customnames) or a list
         if isinstance(numexpts,dict):
            numexp_json = numexpts[numexp]
         else:
            numexp_json = numexp
         # -- Then, we try to open the json file
         try:
            numexp_fj = open(numexp_json)
         except:
            numexp_json = string.replace(numexp_json,'@VAR',variable)
            numexp_fj = open(numexp_json)
         #
         tmp_dict = json.loads(numexp_fj.read())
         mod_name = tmp_dict['RESULTS'].keys()[0]
         if isinstance(numexpts,dict) or mod_name in aux_dd['RESULTS'].keys():
            if isinstance(numexpts,dict):
               new_mod_name = numexp
            else:
               if mod_name in aux_dd:
                  new_mod_name = mod_name+'_'+inc
                  inc = inc + 1
            tmp_dict['RESULTS'][new_mod_name] = tmp_dict['RESULTS'][mod_name].copy()
            tmp_dict['RESULTS'].pop(mod_name)
         #
         # -- Add the results to the auxillary dictionary
         aux_dd['RESULTS'].update( tmp_dict['RESULTS'] )
         numexp_fj.close()
      aux_mods = aux_dd['RESULTS'].keys()


unit_adj = 1
if variable == 'pr':
    unit_adj = 28.
if variable == 'tauu':
    unit_adj = 1000.


mods = dd['RESULTS'].keys()
mods = sorted(mods, key=lambda s:s.lower())


seasons = [season]
if season == 'all':
  seasons = ['djf', 'mam', 'jja', 'son']
  #rects = {'djf':221, 'mam':222, 'jja':223, 'son':224} # subplot location
  #rects = {'djf':231, 'mam':232, 'jja':234, 'son':235} # subplot location
  rects = {'djf':321, 'mam':322, 'jja':323, 'son':324} # subplot location
  #fig = PLT.figure(figsize=(14,9)) # optimized figure size for four subplots
  fig = PLT.figure(figsize=(9,12)) # optimized figure size for four subplots
  fig_filename = variable + '_' + experiment + '_taylor_4panel_' + season + '_' + domain
else:
  rects = {}
  rects[season] = 111 # subplot location
  fig = PLT.figure(figsize=(11,8)) # optimized figure size for one subplot
  fig_filename = variable + '_' + experiment + '_taylor_1panel_' + season + '_' + domain

stdrefs = {}
source_ref = dd['RESULTS'][mods[0]]["defaultReference"]['source']



# -- Main title of the plot
if not title:
   title = variable.title()+', '+(experiment+', '+domain).upper()
fig.suptitle( title, size='x-large') # Giving title for the entire canvas


# -- Plot custom parameters
plot_params = dict()
if aux_json_path: plot_params.update( highlights=aux_mods )
if highlights:    plot_params.update( highlights=str.split(highlights,',') )
if colors:        plot_params.update( colors=colors )
if yaxis_label:   plot_params.update( yaxis_label=yaxis_label )
if figure_font_size:   plot_params.update( figure_font_size=figure_font_size )

print '==>'
print '==> Starting loop on the seasons'
print '==>'

# !!!!!!!!
tot_mods = mods
if aux_mods:
   tot_mods = mods + aux_mods
   dd['RESULTS'].update(aux_dd['RESULTS'])
# !!!!!!!!


for season in seasons:
    # Reference std from obs
    Realization     = dd['RESULTS'][mods[0]]['SimulationDescription']['Realization']
    stdrefs[season] = float(dd['RESULTS'][mods[0]]["defaultReference"][Realization][domain]['std-obs_xy_'+season])*unit_adj

    samples = {}
    all_mods = []

    # -- We put the highlighted simulations at the top
    if 'highlights' in plot_params:
       for highlight in plot_params['highlights']:
           tot_mods.pop(tot_mods.index(highlight))
       tot_mods = tot_mods + plot_params['highlights']
    #
    # -- Loop on the main json file results
    for mod in tot_mods:
        print '-> Computing cor and std on '+mod
        Realization     = dd['RESULTS'][mod]['SimulationDescription']['Realization']
        cor = float(dd['RESULTS'][mod]["defaultReference"][Realization][domain]['cor_xy_'+season])
        std = float(dd['RESULTS'][mod]["defaultReference"][Realization][domain]['std_xy_'+season])*unit_adj
        all_mods.append([std,cor,str(mod)])
    samples[season] = all_mods

    colors = PLT.matplotlib.cm.Set1(NP.linspace(0,1,len(samples[season])))

    # -- Colors
    pl_colors = PLT.matplotlib.cm.jet(NP.linspace(0,1,len(samples)))
    #
    # !!!!!!!!!!!!
    # JS: highlight the results
    if 'highlights' in plot_params:
        highlights = plot_params['highlights']
        pl_colors=['grey']*len(tot_mods)
        # -- Dealing with the colors
        if 'colors' in plot_params:
            colors = str.split(plot_params['colors'],',')
            if len(colors)!=len(highlights):
               if len(colors)==1:
                  # -- if we provide only one color, we will use it for every highlighted simulation
                  colors=colors*len(highlights)
               else:
                  # -- if we didn't provide enough colors (for the number of simulations),
                  #    we will use green as a default
                  #tmpcolors = ['g']*len(highlights)
                  tmpcolors = list(PLT.matplotlib.cm.jet(NP.linspace(0,1,len(highlights))))
                  print 'colors = ',colors
                  for i in xrange(len(colors)): tmpcolors[i] = colors[i]
                  colors = tmpcolors
        else:
            colors = ['g']*len(highlights)
        pl_colors[(len(pl_colors)-len(highlights)-1):(len(pl_colors)-1)] = colors
        print 'pl_colors = ',pl_colors
    #
    print 'pl_colors = ',pl_colors

    dia = TaylorDiagram(stdrefs[season], fig=fig, rect=rects[season],
                        label=source_ref)

    # Add samples to Taylor diagram
    for i,(stddev,corrcoef,name) in enumerate(samples[season]):
        if 'highlights' in plot_params:
           marker = ('o' if name in plot_params['highlights'] else '$%d$' % (i+1))
        dia.add_sample(stddev, corrcoef,
                       marker=marker, ms=figure_font_size, ls='',
                       mfc=pl_colors[i], mec=pl_colors[i], # Colors
                       label=name)

    # Add RMS contours, and label them
    contours = dia.add_contours(levels=5, colors='0.5') # 5 levels
    dia.ax.clabel(contours, inline=1, fontsize=figure_font_size, fmt='%.1f')
    # Tricky: ax is the polar ax (used for plots), _ax is the
    # container (used for layout)
    dia._ax.set_title(season.upper()) # Title for the subplot

# Add a figure legend and title. For loc option, place x,y tuple inside [ ].
# Can also use special options here:
# http://matplotlib.sourceforge.net/users/legend_guide.html

fig.legend(dia.samplePoints,
           [ p.get_label() for p in dia.samplePoints ],
           numpoints=1, prop=dict(size='small'), loc='lower center', ncol=4)

PLT.savefig(outpath + '/' + fig_filename + '.png')

if test:
    PLT.ion()
    PLT.show()


