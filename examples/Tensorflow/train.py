#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import numpy as np
import tflearn

import gzip
import os
from six.moves import urllib
import argparse
import csv

inputfile='all.csv'
work_directory='./'
to_ignore=[2]
vendors = []
models = []

def check_inputfile():
    if not os.path.exists(work_directory):
        os.mkdir(work_directory)
    filepath = os.path.join(work_directory, inputfile)
    if not os.path.exists(filepath):
        print(':::file', filepath, ' does not exist')
        os.exit(1)
    statinfo = os.stat(filepath)
    print(filepath, statinfo.st_size, 'bytes.')

def to_categorical(y, nb_classes):
    y = np.asarray(y, dtype='int32')
    if not nb_classes:
        nb_classes = np.max(y)+1
    Y = np.zeros((len(y), nb_classes))
    for i in range(len(y)):
        Y[i, y[i]] = 1.
    return Y

def load_csv(filepath, target_column=-1, columns_to_ignore=None,
             has_header=True, categorical_labels=False, n_classes=None):
    from tensorflow.python.platform import gfile
    with gfile.Open(filepath) as csv_file:
        data_file = csv.reader(csv_file)
        if not columns_to_ignore:
            columns_to_ignore = []
        if has_header:
            header = next(data_file)
        data, target = [], []
        # Fix column to ignore ids after removing target_column
        for i, c in enumerate(columns_to_ignore):
            if c > target_column:
                columns_to_ignore[i] -= 1
        for i, d in enumerate(data_file):
            target.append(d.pop(target_column))
            data.append([_d for j, _d in enumerate(d) if j not in columns_to_ignore])
        if categorical_labels:
            assert isinstance(n_classes, int), "n_classes not specified!"
            target = to_categorical(target, n_classes)
        return data, target

def readnames(fn):
    names = {}
    namenum = 1
    with open(fn) as f:
        lines = f.readlines()
        for l in lines:
            l = l.rstrip()
            names[l] = namenum
            namenum = namenum + 1
    return names

def preprocess(data, columns_to_ignore):
    # Sort by descending id and delete columns
    for id in sorted(columns_to_ignore, reverse=True):
        [r.pop(id) for r in data]
    for i in range(len(data)):
        vend = data[i][0]
        if vend in vendors.keys():
            data[i][0]= vendors[vend]
        else:
            print('::: vendor ' , vend,'does not exist')
        model= data[i][1]
        if model in models.keys():
            data[i][1]=models[model]
        else:
            print('::: model ', model,'does not exist')
    return np.array(data, dtype=np.float32)

def make_model():
    net = tflearn.input_data(shape=[None, 7])
    net = tflearn.fully_connected(net, 32)
    net = tflearn.fully_connected(net, 32)
    net = tflearn.fully_connected(net, 2, activation='softmax')
    net = tflearn.regression(net)
    model = tflearn.DNN(net)
    return model

def train_model(modelfn):
    check_inputfile()
    data, labels = load_csv(inputfile, target_column=3,
                        categorical_labels=True, n_classes=2)
    data = preprocess(data, to_ignore)
    model = make_model()
    model.fit(data, labels, n_epoch=10, batch_size=16, show_metric=True)
    model.save(modelfn)

def predict(modelfn,data):
    model = make_model()
    model.load(modelfn)
    run_model(model,data)
    #test_model(model)

def run_model(model,data):
    dummy = ['Seagate','ST4000DM000',100,100,100,99,99 ]
    items = data.split(',')
    items[2]=float(items[2])
    items[3]=float(items[3])
    items[4]=float(items[4])
    items[5]=float(items[5])
    items[6]=float(items[6])
    dummy,items=preprocess([dummy,items],[])
    pred = model.predict([dummy,items])
    print(':::',pred[1])

def test_model(model):
    test1 = ['Seagate','ST4000DM000',4000787030016,100,100,100,99,99 ]
    test2 = [ 'WDC','WD800BB',80026361856,0,0,0,0,0]
    test1,test2= preprocess([test1,test2], to_ignore)

    pred = model.predict([test1,test2])
    print(':::test1 failure rate', pred[0])
    print(':::test2 failure rate', pred[1])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='train backblaze model')
    parser.add_argument('-f','--file', help='input file', required=False)
    parser.add_argument('-t','--train', help='train and save to file', required=False)
    parser.add_argument('-p','--predict', help='predict using model from file', required=False)
    parser.add_argument('-d','--data', help='data for prediction', required=False)
    args = vars(parser.parse_args())
    if args['file']:
        inputfile = args['file']
        print('>>>Using input file',inputfile)
    if args['predict'] and not args['data']:
            print('::: -d data required for prediction')
            os.exit(1)
    vendors = readnames('vendors.txt')
    models = readnames('models.txt')
    if  args['train']:
        train_model(args['train'])
    if args['predict']:
        predict(args['predict'],args['data'])
