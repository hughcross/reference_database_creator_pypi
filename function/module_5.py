#! /usr/bin/env python3

## import modules
import collections
import numpy as np
from collections import Counter
from itertools import islice
from matplotlib import pyplot as plt

## functions: visualizations
def split_db_by_taxgroup(file_in, tax_level):
    ranks = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    count = 1
    tax_group_list = []
    uniq_tax_group_list = []
    species_dict = collections.defaultdict(list)
    for item in ranks:
        count = count + 1
        if item == tax_level:
            break
    with open(file_in, 'r') as f_in:
        for line in f_in:
            taxgroup = line.split('\t')[count].split(',')[2]
            species = line.split('\t')[8].split(',')[2]
            tax_group_list.append(taxgroup)
            species_dict[taxgroup].append(species)
            if taxgroup not in uniq_tax_group_list:
                uniq_tax_group_list.append(taxgroup)
    
    return tax_group_list, uniq_tax_group_list, species_dict

def num_spec_seq_taxgroup(uniq_tax_group_list, species_dict, sequence_counter):
    dict_list = []
    for group in uniq_tax_group_list:
        for k, v in species_dict.items():
            if k == group:
                for item in sequence_counter.most_common():
                    if item[0] == k:
                        seq = item[1]
                        dict_list.append({'key' : k, 'species' : len(v), 'sequence' : seq})
    
    return dict_list

def horizontal_barchart(sorted_info):
    tax_group = []
    tax_species = []
    tax_sequence = []
    for item in sorted_info:
        tax_group.append(item['key'])
        tax_species.append(item['species'])
        tax_sequence.append(item['sequence'])
    width = 0.5
    y_indexs = np.arange(len(tax_group))
    plt.barh(y_indexs, tax_species, width, edgecolor = 'black', alpha = 0.75, label = '# species')
    plt.barh(y_indexs + width, tax_sequence, width, edgecolor = 'black', alpha = 0.75, label = '# sequences')
    plt.title('Diversity in reference database')
    plt.xlabel('Number of sequences/species')
    plt.yticks(ticks = y_indexs + width / 2, labels = tax_group)
    plt.legend()
    plt.tight_layout()
    plt.show()

def get_amp_length(file_in, tax_level):
    ranks = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    count = 1
    for item in ranks:
        count = count + 1
        if item == tax_level:
            break
    amplength_dict = collections.defaultdict(list)
    with open(file_in, 'r') as f_in:
        for line in f_in:
            l = line.rstrip('\n')
            seq_len = len(l.rsplit('\t', 1)[1])
            taxgroup = l.split('\t')[count].split(',')[2]
            amplength_dict['overall'].append(seq_len)
            amplength_dict[taxgroup].append(seq_len)
    sorted_dict = sorted(amplength_dict.items(), key = lambda item: len(item[1]), reverse = True)
    final_dict = {}
    for item in islice(sorted_dict, 6):
        length = sorted(Counter(item[1]).most_common(), key = lambda tup: tup[0])
        final_dict[item[0]] = length
    
    return final_dict

def amplength_figure(amp_length_dict):
    for item in amp_length_dict.items():
        amplicon_size = []
        frequency = []
        for i in item[1]:
            amplicon_size.append(i[0])
            frequency.append(i[1])
        label = str(item[0]) + '; ' + str(sum(frequency)) + ' seqs'
        if item[0] == 'overall':
            plt.plot(amplicon_size, frequency, color = '#444444', linestyle = '--', linewidth = 0)
            plt.fill_between(amplicon_size, frequency, color = '#444444', interpolate = True, alpha = 0.25, label = label)
        else:
            plt.plot(amplicon_size, frequency, label = label)

    plt.legend()
    plt.title('Amplicon size distribution')
    plt.xlabel('amplicon size')
    plt.ylabel('number of sequences')

    plt.show()



