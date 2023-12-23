# This file is copied and modified from https://github.com/MicrosoftResearch/Azimuth
# This code was modified to use with python 3 and needed for percent and position scoring
# was removed to simplify code
# Azimuth license applies to this file

from math import exp
from re import findall
import pandas as pd
import Bio.Seq as Seq
import numpy as np
import itertools
import Bio.SeqUtils.MeltingTemp as Tm

def countGC(s, length_audit=True):
    '''
    GC content for only the 20mer, as per the Doench paper/code
    '''
    if length_audit:
        assert len(s) == 30, "seems to assume 30mer"
    return len(s[4:24].replace('A', '').replace('T', ''))


def nucleotide_features(s, order, include_pos_independent, max_index_to_use, prefix="", feature_type='all',
                        raw_alphabet=['A', 'T', 'C', 'G']):
    '''
    compute position-specific order-mer features for the 4-letter alphabet
    (e.g. for a sequence of length 30, there are 30*4 single nucleotide features
          and (30-1)*4^2=464 double nucleotide features
    '''
    assert feature_type in ['all', 'pos_independent', 'pos_dependent']
    if max_index_to_use <= len(s):
        # print "WARNING: trimming max_index_to use down to length of string=%s" % len(s)
        max_index_to_use = len(s)
    if max_index_to_use is not None:
        s = s[:max_index_to_use]
    # assert(len(s)==30, "length not 30")
    # s = s[:30] #cut-off at thirty to clean up extra data that they accidentally left in, and were instructed to ignore in this way
    alphabet = get_alphabet(order, raw_alphabet=raw_alphabet)
    features_pos_dependent = np.zeros(len(alphabet) * (len(s) - (order - 1)))
    features_pos_independent = np.zeros(np.power(len(raw_alphabet), order))

    index_dependent = []
    index_independent = []

    for position in range(0, len(s) - order + 1, 1):
        for l in alphabet:
            index_dependent.append('%s%s_%d' % (prefix, l, position))

    for l in alphabet:
        index_independent.append('%s%s' % (prefix, l))

    for position in range(0, len(s) - order + 1, 1):
        nucl = s[position:position + order]
        features_pos_dependent[alphabet.index(nucl) + (position * len(alphabet))] = 1.0
        features_pos_independent[alphabet.index(nucl)] += 1.0

        # this is to check that the labels in the pd df actually match the nucl and position
        assert index_dependent[alphabet.index(nucl) + (position * len(alphabet))] == '%s%s_%d' % (
        prefix, nucl, position)
        assert index_independent[alphabet.index(nucl)] == '%s%s' % (prefix, nucl)

    # index_independent = ['%s_pi.Order%d_P%d' % (prefix, order,i) for i in range(len(features_pos_independent))]
    # index_dependent = ['%s_pd.Order%d_P%d' % (prefix, order, i) for i in range(len(features_pos_dependent))]

    if np.any(np.isnan(features_pos_dependent)):
        raise Exception("found nan features in features_pos_dependent")
    if np.any(np.isnan(features_pos_independent)):
        raise Exception("found nan features in features_pos_independent")

    if feature_type == 'all' or feature_type == 'pos_independent':
        if feature_type == 'all':
            res = pd.Series(features_pos_dependent, index=index_dependent), pd.Series(features_pos_independent,
                                                                                      index=index_independent)
            assert not np.any(np.isnan(res.values))
            return res
        else:
            res = pd.Series(features_pos_independent, index=index_independent)
            assert not np.any(np.isnan(res.values))
            return res

    res = pd.Series(features_pos_dependent, index=index_dependent)
    assert not np.any(np.isnan(res.values))
    return res


def Tm_feature(data, pam_audit=True, learn_options=None):
    '''
    assuming '30-mer'is a key
    get melting temperature features from:
        0-the 30-mer ("global Tm")
        1-the Tm (melting temperature) of the DNA:RNA hybrid from positions 16 - 20 of the sgRNA, i.e. the 5nts immediately proximal of the NGG PAM
        2-the Tm of the DNA:RNA hybrid from position 8 - 15 (i.e. 8 nt)
        3-the Tm of the DNA:RNA hybrid from position 3 - 7  (i.e. 5 nt)
    '''
    if learn_options is None or 'Tm segments' not in learn_options.keys():
        segments = [(19, 24), (11, 19), (6, 11)]
    else:
        segments = learn_options['Tm segments']
    sequence = data['30mer'].values
    featarray = np.ones((sequence.shape[0], 4))
    for i, seq in enumerate(sequence):
        if seq[25:27] != "GG":
            raise Exception("expected GG but found %s" % seq[25:27])
        rna = False
        featarray[i, 0] = Tm.Tm_NN(seq)  # 30mer Tm
        featarray[i, 1] = Tm.Tm_NN(seq[segments[0][0]:segments[0][1]], )  # 5nts immediately proximal of the NGG PAM
        featarray[i, 2] = Tm.Tm_NN(seq[segments[1][0]:segments[1][1]])  # 8-mer
        featarray[i, 3] = Tm.Tm_NN(seq[segments[2][0]:segments[2][1]])  # 5-mer

    feat = pd.DataFrame(featarray, index=data.index,
                        columns=["Tm global_%s" % rna, "5mer_end_%s" % rna, "8mer_middle_%s" % rna,
                                 "5mer_start_%s" % rna])

    return feat


def get_alphabet(order, raw_alphabet=['A', 'T', 'C', 'G']):
    alphabet = ["".join(i) for i in itertools.product(raw_alphabet, repeat=order)]
    return alphabet


def NGGX_interaction_feature(data, pam_audit=True):
    '''
    assuming 30-mer, grab the NGGX _ _ positions, and make a one-hot
    encoding of the NX nucleotides yielding 4x4=16 features
    '''
    sequence = data['30mer'].values
    feat_NX = pd.DataFrame()
    # check that GG is where we think
    for seq in sequence:
        if seq[25:27] != "GG":
            raise Exception("expected GG but found %s" % seq[25:27])
        NX = seq[24] + seq[27]
        NX_onehot = nucleotide_features(NX, order=2, feature_type='pos_dependent', max_index_to_use=2, prefix="NGGX")
        # NX_onehot[:] = np.random.rand(NX_onehot.shape[0]) ##TESTING RANDOM FEATURE
        feat_NX = pd.concat([feat_NX, NX_onehot], axis=1)
    return feat_NX.T


def apply_nucleotide_features(seq_data_frame, order, num_proc, include_pos_independent, max_index_to_use, prefix=""):
    if include_pos_independent:
        feat_pd = seq_data_frame.apply(nucleotide_features, args=(order, max_index_to_use, prefix, 'pos_dependent'))
        feat_pi = seq_data_frame.apply(nucleotide_features, args=(order, max_index_to_use, prefix, 'pos_independent'))
        assert not np.any(np.isnan(feat_pd)), "nans here can arise from sequences of different lengths"
        assert not np.any(np.isnan(feat_pi)), "nans here can arise from sequences of different lengths"
        return feat_pd, feat_pi
    else:
        feat_pd = seq_data_frame.apply(nucleotide_features, args=(order, max_index_to_use, prefix, 'pos_dependent'))
        assert not np.any(np.isnan(feat_pd)), "found nan in feat_pd"
        return feat_pd


def nucleotide_features(s, order, max_index_to_use, prefix="", feature_type='all', raw_alphabet=['A', 'T', 'C', 'G']):
    '''
    compute position-specific order-mer features for the 4-letter alphabet
    (e.g. for a sequence of length 30, there are 30*4 single nucleotide features
          and (30-1)*4^2=464 double nucleotide features
    '''
    assert feature_type in ['all', 'pos_independent', 'pos_dependent']
    if max_index_to_use <= len(s):
        # print "WARNING: trimming max_index_to use down to length of string=%s" % len(s)
        max_index_to_use = len(s)

    if max_index_to_use is not None:
        s = s[:max_index_to_use]
    # assert(len(s)==30, "length not 30")
    # s = s[:30] #cut-off at thirty to clean up extra data that they accidentally left in, and were instructed to ignore in this way
    alphabet = get_alphabet(order, raw_alphabet=raw_alphabet)
    features_pos_dependent = np.zeros(len(alphabet) * (len(s) - (order - 1)))
    features_pos_independent = np.zeros(np.power(len(raw_alphabet), order))

    index_dependent = []
    index_independent = []

    for position in range(0, len(s) - order + 1, 1):
        for l in alphabet:
            index_dependent.append('%s%s_%d' % (prefix, l, position))

    for l in alphabet:
        index_independent.append('%s%s' % (prefix, l))

    for position in range(0, len(s) - order + 1, 1):
        nucl = s[position:position + order]
        features_pos_dependent[alphabet.index(nucl) + (position * len(alphabet))] = 1.0
        features_pos_independent[alphabet.index(nucl)] += 1.0

        # this is to check that the labels in the pd df actually match the nucl and position
        assert index_dependent[alphabet.index(nucl) + (position * len(alphabet))] == '%s%s_%d' % (
        prefix, nucl, position)
        assert index_independent[alphabet.index(nucl)] == '%s%s' % (prefix, nucl)

    if np.any(np.isnan(features_pos_dependent)):
        raise Exception("found nan features in features_pos_dependent")
    if np.any(np.isnan(features_pos_independent)):
        raise Exception("found nan features in features_pos_independent")

    if feature_type == 'all' or feature_type == 'pos_independent':
        if feature_type == 'all':
            res = pd.Series(features_pos_dependent, index=index_dependent), pd.Series(features_pos_independent,
                                                                                      index=index_independent)
            assert not np.any(np.isnan(res.values))
            return res
        else:
            res = pd.Series(features_pos_independent, index=index_independent)
            assert not np.any(np.isnan(res.values))
            return res

    res = pd.Series(features_pos_dependent, index=index_dependent)
    assert not np.any(np.isnan(res.values))
    return res

def check_feature_set(feature_sets):
    '''
    Ensure the # of people is the same in each feature set
    '''
    assert feature_sets != {}, "no feature sets present"

    N = None
    for ft in feature_sets.keys():
        N2 = feature_sets[ft].shape[0]
        if N is None:
            N = N2
        else:
            assert N >= 1, "should be at least one individual"
            assert N == N2, "# of individuals do not match up across feature sets"

    for set in feature_sets.keys():
        if np.any(np.isnan(feature_sets[set])):
            raise Exception("found Nan in set %s" % set)


def get_all_order_nuc_features(data, feature_sets, learn_options, maxorder, max_index_to_use, prefix="", quiet=False):
    for order in range(1, maxorder + 1):
        nuc_features_pd, nuc_features_pi = apply_nucleotide_features(data, order, learn_options["num_proc"],
                                                                     include_pos_independent=True,
                                                                     max_index_to_use=max_index_to_use, prefix=prefix)
        feature_sets['%s_nuc_pd_Order%i' % (prefix, order)] = nuc_features_pd
        if learn_options['include_pi_nuc_feat']:
            feature_sets['%s_nuc_pi_Order%i' % (prefix, order)] = nuc_features_pi
        check_feature_set(feature_sets)



def gc_features(data, audit=True):
    gc_count = data['30mer'].apply(lambda seq: countGC(seq, audit))
    gc_count.name = 'GC count'
    gc_above_10 = (gc_count > 10) * 1
    gc_above_10.name = 'GC > 10'
    gc_below_10 = (gc_count < 10) * 1
    gc_below_10.name = 'GC < 10'
    return gc_above_10, gc_below_10, gc_count


def normalize_features(data, axis):
    '''
    input: Pandas.DataFrame of dtype=np.float64 array, of dimensions
    mean-center, and unit variance each feature
    '''
    data -= data.mean(axis)
    data /= data.std(axis)
    # remove rows with NaNs
    data = data.dropna(1)
    if np.any(np.isnan(data.values)): raise Exception("found NaN in normalized features")
    return data


def normalize_feature_sets(feature_sets):
    '''
    zero-mean, unit-variance each feature within each set
    '''

    print("Normalizing features...")
    new_feature_sets = {}
    for set in feature_sets:
        new_feature_sets[set] = normalize_features(feature_sets[set], axis=0)
        if np.any(np.isnan(new_feature_sets[set].values)):
            raise Exception("found Nan feature values in set=%s" % set)
        assert new_feature_sets[set].shape[1] > 0, "0 columns of features"
    return new_feature_sets


def featurize_data(data, learn_options, Y, pam_audit=True, length_audit=True):
    '''
    data = Xdf
    assumes that data contains the 30mer
    returns set of features from which one can make a kernel for each one
    '''
    all_lens = data['30mer'].apply(len).values
    unique_lengths = np.unique(all_lens)
    num_lengths = len(unique_lengths)
    assert num_lengths == 1, "should only have sequences of a single length, but found %s: %s" % (
    num_lengths, str(unique_lengths))

    feature_sets = {}

    if learn_options["nuc_features"]:
        # spectrum kernels (position-independent) and weighted degree kernels (position-dependent)
        get_all_order_nuc_features(data['30mer'], feature_sets, learn_options, learn_options["order"],
                                   max_index_to_use=30, quiet=False)

    check_feature_set(feature_sets)

    if learn_options["gc_features"]:
        gc_above_10, gc_below_10, gc_count = gc_features(data, length_audit)
        feature_sets['gc_above_10'] = pd.DataFrame(gc_above_10)
        feature_sets['gc_below_10'] = pd.DataFrame(gc_below_10)
        feature_sets['gc_count'] = pd.DataFrame(gc_count)

    if learn_options["include_NGGX_interaction"]:
        feature_sets["NGGX"] = NGGX_interaction_feature(data)

    if learn_options["include_Tm"]:
        feature_sets["Tm"] = Tm_feature(data, pam_audit, learn_options=None)


    check_feature_set(feature_sets)

    reordered_feature_sets = {}
    keys = ['gc_count', '_nuc_pd_Order2', '_nuc_pd_Order1', 'gc_above_10', '_nuc_pi_Order1', '_nuc_pi_Order2', 'Tm',
            'gc_below_10', 'NGGX']
    for k in keys:
        reordered_feature_sets[k] = feature_sets[k]

    return reordered_feature_sets



