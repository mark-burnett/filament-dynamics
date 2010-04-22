import itertools
import csv

def write_summary(f, summary_data):
    data_titles = []
    names = []
    for k in summary_data.keys():
        if 'time' == k:
            continue
        names.append(k)
        data_titles.append(k + '_avg')
        data_titles.append(k + '_std')

    w = csv.writer(f, delimiter=' ')

    # Write titles
    w.writerow(['time'] + data_titles)
    
    full_data = [summary_data['time']]
    for n in names:
        full_data.append(summary_data[n][0])
        full_data.append(summary_data[n][1])

    w.writerows(itertools.izip(*full_data))
