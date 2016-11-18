#!/usr/bin/python

### python si-601-lab-5.py input-v2.txt

from mrjob.job import MRJob
import re

class BiGramFreqCount(MRJob):
  
  ### input: self, ignored_key, in_value
  def mapper(self, _, line):
    ### replace this part and use bigram (this word and its next word) as the key
    ### skip the last word because there is no word after it
    
  ### input: self, in_key from mapper, in_value from mapper
  def reducer(self, key, values):
    #### Put your code here

if __name__ == '__main__':
  BiGramFreqCount.run()
