import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Update the path if needed
df = pd.read_csv('base_agg.csv')
df['stage'] = df['Previous Version'] + '→' + df['Current Version']

# Compute human contribution
df['Word Alteration (%)'] = 100 - df['Word Retention (%)']
df['Sentence Alteration (%)'] = 100 - df['Sentence Retention (%)']
df['Paragraph Alteration (%)'] = 100 - df['Paragraph Retention (%)']

# 1) Human Editorial Impact
order = ["Draft→Refined", "Refined→Edited", "Edited→Final", "Draft→Final"]
vals = df.set_index('stage').loc[order, 'Word Alteration (%)']
colors = ['#64B5F6','#4CAF50','#388E3C','#CDDC39']
plt.figure(figsize=(8,5))
for i, st in enumerate(order):
    plt.barh(st, vals[st], color=colors[i])
    plt.text(vals[st]+1, i, f"{vals[st]:.0f}%")
plt.title("Human Editorial Impact")
plt.xlabel("Human Contribution (%)")
plt.tight_layout()
plt.show()

# 2) Content Transformation Types
stages = ["Refined","Edited","Final"]
metrics = ['Word Alteration (%)','Sentence Alteration (%)','Paragraph Alteration (%)']
colors = ['#1976D2','#388E3C','#F57C00']
x = np.arange(len(stages)); width=0.2
plt.figure(figsize=(8,5))
for i,m in enumerate(metrics):
    for j,stage in enumerate(stages):
        v = df.loc[df['Current Version']==stage, m].iloc[0]
        plt.bar(j+i*width, v, width, color=colors[i])
        plt.text(j+i*width, v+1, f"{v:.0f}%", ha='center')
plt.xticks(x+width, stages)
plt.title("Content Transformation Types")
plt.ylabel("Human Contribution (%)")
plt.legend([m.replace(' Alteration (%)','') for m in metrics])
plt.tight_layout()
plt.show()

# 3) Editorial Journey (Waterfall)
r1 = df.loc[df['stage']=='Draft→Refined','Word Retention (%)'].iloc[0]
r2 = r1 * df.loc[df['stage']=='Refined→Edited','Word Retention (%)'].iloc[0]/100
r3 = r2 * df.loc[df['stage']=='Edited→Final','Word Retention (%)'].iloc[0]/100
drops = [100-r1, r1-r2, r2-r3]
labels = ["Start","Draft→Refined","Refined→Edited","Edited→Final"]
cum = [100]
for d in drops: cum.append(cum[-1]-d)
plt.figure(figsize=(8,5))
plt.bar(0, 100, color='#2196F3', width=0.5)
for i, d in enumerate(drops,1):
    plt.bar(i, -d, bottom=cum[i-1], color='#4CAF50', width=0.5)
    plt.text(i, cum[i-1]-d/2, f"-{d:.0f}%", ha='center', va='center')
plt.xticks(range(len(labels)), labels)
plt.title("Editorial Journey")
plt.ylabel("Percentage of AI-Origin Content")
plt.tight_layout()
plt.show()

# 4) Summary Metric
overall = df.loc[df['stage']=='Draft→Final','Word Alteration (%)'].iloc[0]
mx = df.loc[df['Word Alteration (%)'].idxmax()]
plt.figure(figsize=(6,3))
plt.text(0.5,0.6,f"{overall:.0f}%",ha='center',va='center',fontsize=48,color='#4CAF50')
plt.text(0.5,0.3,f"Stage of most editing: {mx['stage']} ({mx['Word Alteration (%)']:.0f}%)",
         ha='center',va='center',fontsize=12)
plt.axis('off')
plt.title("Summary Metric")
plt.tight_layout()
plt.show()
