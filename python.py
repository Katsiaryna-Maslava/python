from luminol.anomaly_detector import AnomalyDetector
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
_df = pd.read_csv('article_sample.csv')
_ts = _df[_df.apply(lambda x: x['location'] == 'Belarus' and x['quater'] == 4 and x['keyword'] in ['КАМАЗ'], axis=1)]
_ts = _ts[_ts['date'].apply(lambda x: '2018' in x)]
ts1 = _ts[['date','polarity']]
ts1['date'] = ts1['date'].apply(lambda x: [int(_) for _ in x.split('-')[1:]])
ts1['date'] = ts1['date'].apply(lambda x: (x[0]-10)*30+x[1])
_ts1 = ts1.groupby('date')['polarity'].mean().reset_index().set_index('date').sort_index()
ts1 = _ts1.to_dict()['polarity']
my_detector = AnomalyDetector(ts1, score_threshold=1)
score = my_detector.get_all_scores()
anomalies = my_detector.get_anomalies()
fig = plt.figure(figsize=(15,10))
ax = fig.subplots(1)
ax.plot(_ts1, linestyle='--', marker='o')
for _index, _ano in enumerate(anomalies):
    _c = np.random.rand(1,3)[0]
    _width = _ano.end_timestamp - _ano.start_timestamp
    rect = patches.Rectangle((_ano.start_timestamp,-1.5),_width,3,linewidth=2,edgecolor=_c,facecolor='none', label='Anomaly #{}'.format(_index))
    ax.add_patch(rect)
    
ax.legend()
ax.set_ylim([-1.5,1.5])
fig.tight_layout()
fig.savefig('temp.png')
fig.show()
