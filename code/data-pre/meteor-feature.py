#coding=utf-8
import argparse
from itertools import islice
import sys
from nltk.corpus import wordnet as wn
import math
import numpy

reload(sys)
sys.setdefaultencoding('utf-8')

synsets = {}

def init(syn_dict_path):
    fr = open(syn_dict_path)
    dataset = fr.readlines()
    fr.close()

    for str_line in dataset:
        line = str_line.decode("utf-8").strip()
        field = line.split("\t")
        cur = field[1].split(",")
        wd = field[0]
        synsets[wd] = cur

    return synsets

def exact_word_matches(h, ref):
    bitvec_ref = [False for _ in ref]
    bitvec_h = [False for _ in h]
    count = 0
    for index, word in enumerate(h):
        for ref_index, ref_word in enumerate(ref):
            if not bitvec_ref[ref_index] and word == ref_word:
                count += 1
                bitvec_ref[ref_index] = True
                bitvec_h[index] = True
                break
    return (count, bitvec_h, bitvec_ref)

# def synonyms(arr):
#     syn_arr = []
#     for word in arr:
#         syn_arr.append([lst for ss in wn.synsets(word) for lst in ss.lemma_names()])
#     return syn_arr

def synonyms(arr):
    syn_arr = []
    for wd in arr:
        if wd in synsets.keys():
            syn_arr.append(synsets[wd])
        else:
            syn_arr.append([])
    return syn_arr

def wordnet_word_matches(h, ref, bitvec_h, bitvec_ref):
    count = 0
    for i, syns in enumerate(h):
        if not bitvec_h[i]:
            for j, ref_syn in enumerate(ref):
                if not bitvec_ref[j]:
                    if check_syns(syns, ref_syn):
                        count += 1
                        bitvec_ref[j] = True
                        bitvec_h[i] = True
                        break
    return (count, bitvec_h, bitvec_ref)

def check_syns(h, ref):
    for synset in h:
        if synset in ref:
            return True
    return False

def calc_chunks(h, ref, h_syn, ref_syn):
    chunk = 0
    bitvec = [False for _ in ref]
    i = 0
    j = 0
    changed = False
    while i < len(h):
        j = 0
        changed = False
        while j < len(ref):
            if i < len(h) and j < len(ref) and (h[i] == ref[j] or check_syns(h_syn[i], ref_syn[j])) and not bitvec[j]:
                while i < len(h) and j < len(ref) and (h[i] == ref[j] or check_syns(h_syn[i], ref_syn[j])) and not bitvec[j]:
                    bitvec[j] = True
                    changed = True
                    i += 1
                    j += 1
                chunk += 1
            else:
                j += 1
        i = i + 1 if not changed else i
    return chunk

def main():
    parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
    parser.add_argument('-i', '--input', default='../../ETL-data/check-data/zhihu/out-test.dat', help='input file (default data/hyp1-hyp2-ref)')
    parser.add_argument('-n', '--num_sentences', default=None, type=int, help='Number of hypothesis pairs to evaluate')
    parser.add_argument('-a', '--alpha', default=0.82, type=float, help='Balances precision and recall')
    parser.add_argument('-b', '--beta', default=1.0, type=float, help='METEOR penalty parameter')
    parser.add_argument('-g', '--gamma', default=0.21, type=float, help='METEOR penalty parameter')

    opts = parser.parse_args()
    fr = open(opts.input)

    syn_dict_path = "./dict/cowSyn.dat"
    init(syn_dict_path)
    while 1:
        str_line = fr.readline().decode("utf-8")
        if not str_line:
            break

        if str_line == "":
            continue

        field = str_line.replace('\n','').replace('\r','').replace('.','').replace(',','').replace(':','').replace('?','').replace('"','').replace('\'','').split("\t")
        h1 = field[1].split(" ")
        ref = field[2].split(" ")

        # print(h1)
        # print(ref)

        (h1_exact_matches, bitvec_h1, bitvec_ref1) = exact_word_matches(h1, ref)
        # synsets wordnet:
        h1_syn = synonyms(h1)
        ref_syn = synonyms(ref)

        (h1_wn_matches, bitvec_h1, bitvec_ref1) = wordnet_word_matches(h1_syn, ref_syn, bitvec_h1, bitvec_ref1)

        h1_num_matches = h1_exact_matches + h1_wn_matches

        precision1 = h1_num_matches / float(len(h1))

        recall1 = h1_num_matches / float(len(ref))

        h1_score = (precision1 * recall1) / float(((1 - opts.alpha) * recall1) + (opts.alpha * precision1) + 1)
        # meteor penalty:
        chunk1 = calc_chunks(h1, ref, h1_syn, ref_syn)

        frag1 = chunk1 / float(h1_num_matches) if h1_num_matches != 0 else 0

        penalty1 = opts.gamma * (frag1 ** opts.beta)

        h1_match = (1 - penalty1) * h1_score

        #print("meteor_score" + "\t" + str(h1_match))
        print(str(h1_match))
if __name__ == '__main__':
    main()
