#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 21:40:40 2019

@author: zcgu
"""

import torch
import torch.utils.data as D

class ImagesDS(D.Dataset):
    # class to load training images
    def __init__(self, df, mode='train', channels=range(6), subsample=False, device='cpu'):
        self.records = df.to_records(index=False)
        self.channels = channels
        self.mode = mode
        self.device = device
        self.len = df.shape[0]
        
    @staticmethod
    def _load_img_as_tensor(file_name):
        return torch.load(file_name).float()/255. # torch.from_numpy(np.load(file_name)/255.).float() # normalize to [0,1]  

    def _get_img_path(self, index):
        return self.records[index].path

    # subsampling needed
    def __getitem__(self, index):
        # t0 = time()
        path = self._get_img_path(index)
        img = self._load_img_as_tensor(path)
        # t1 = time()
        img = torch.cat([img[i,...].unsqueeze(0) for i in self.channels])  #  img[self.channels,...]  # 
        if self.mode == 'train':
            return img.to(self.device), torch.tensor(self.records[index].sirna).long().to(self.device)
        else:
            return img.to(self.device), torch.tensor(self.records[index].plate).long().to(self.device)

    def __len__(self):
        return self.len
