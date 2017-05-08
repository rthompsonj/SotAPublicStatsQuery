import sys
import json
import pandas as pd

from bokeh.plotting import figure, output_file, save
from bokeh.models import HoverTool

if len(sys.argv) < 2:
    print('please provide a json to parse!')
    sys.exit()

with open(sys.argv[1],'r') as f:
    data = json.loads(f.read())

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"    
    
df = pd.DataFrame(data)
df = df[df.LocationEvent == 'PlayerKilledByPlayer']

## PVP kd ratios per person ##
kd_ratios = []
for group in df.groupby(df.PlayerName):
    name     = group[0]
    if name == 'Anonymous': continue
    kd_ratios.append({
        'name':name,
        'victim': len(df[df.Victim == name]),
        'killer': len(df[df.Killer == name]),
        'kd': float(len(df[df.Killer == name]))/float(len(df[df.Victim == name])),
    })

kd_ratios = pd.DataFrame(kd_ratios)
kd_ratios = kd_ratios[['name', 'killer', 'victim', 'kd']]
kd_ratios = kd_ratios.sort_values(by='kd', ascending=False)
kd_ratios = kd_ratios.reset_index(drop=True)

TOOLTIPS = [
    ('Name:', '@name'),
    ('Killer:', '@killer'),
    ('Victim:', '@victim'),
    ('K/D Ratio:', '@kd')
]

p = figure(title='SotA KD Ratio',
           tools=[HoverTool(tooltips=TOOLTIPS), TOOLS])

maxval = max(kd_ratios.killer.max(), kd_ratios.victim.max())

p.line([0,maxval], [0,maxval], line_width=1, color='black', line_dash='dashed')
p.scatter('killer', 'victim', source=kd_ratios, size=8, fill_color='red')
p.xaxis.axis_label = 'N times a killer'
p.yaxis.axis_label = 'N times a victim'
output_file('kd_ratio.html')
save(p)
###########################
