# -*- coding: utf-8 -*-
"""EnglishTN and ITN for Cardinals and Ordinals.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oePNHPClT_01Xh4b_r3K1gkl78vdcM90
"""

# Commented out IPython magic to ensure Python compatibility.
### WARNING: This notebook will not work in a Colab environment. 

BRANCH= 'main'

!git clone -b $BRANCH https://github.com/NVIDIA/NeMo
# %cd NeMo
!./reinstall.sh

import pynini
import nemo_text_processing

from pynini.lib import pynutil

from nemo_text_processing.text_normalization.en.graph_utils import GraphFst, NEMO_DIGIT, delete_space, NEMO_SIGMA, NEMO_NOT_QUOTE, delete_extra_space, NEMO_NON_BREAKING_SPACE
from nemo_text_processing.text_normalization.normalize import Normalizer

from nemo_text_processing.inverse_text_normalization.fr.taggers.cardinal import CardinalFst
from nemo_text_processing.inverse_text_normalization.fr.taggers.decimal import DecimalFst
from nemo_text_processing.inverse_text_normalization.fr.taggers.money import MoneyFst
from nemo_text_processing.inverse_text_normalization.fr.taggers.ordinal import OrdinalFst
from nemo_text_processing.inverse_text_normalization.fr.taggers.punctuation import PunctuationFst
from nemo_text_processing.inverse_text_normalization.fr.taggers.time import TimeFst
from nemo_text_processing.inverse_text_normalization.fr.taggers.whitelist import WhiteListFst
from nemo_text_processing.inverse_text_normalization.fr.taggers.word import WordFst
from nemo_text_processing.inverse_text_normalization.fr.verbalizers.cardinal import CardinalFst
from nemo_text_processing.inverse_text_normalization.fr.verbalizers.decimal import DecimalFst
from nemo_text_processing.inverse_text_normalization.fr.verbalizers.money import MoneyFst
from nemo_text_processing.inverse_text_normalization.fr.verbalizers.ordinal import OrdinalFst
from nemo_text_processing.inverse_text_normalization.fr.verbalizers.time import TimeFst
from nemo_text_processing.inverse_text_normalization.fr.verbalizers.whitelist import WhiteListFst
from nemo_text_processing.inverse_text_normalization.fr.verbalizers.word import WordFst

LANGUAGE= "MY_LANGUAGE" # Change this to your desired language

# Commented out IPython magic to ensure Python compatibility.
# %cd nemo_text_processing/inverse_text_normalization/
!mkdir {LANGUAGE}
!mkdir "{LANGUAGE}/taggers"
!mkdir "{LANGUAGE}/verbalizers"
!mkdir "{LANGUAGE}/data"
# %cd {LANGUAGE}
!pwd && ls

!cp ../../text_normalization/en/graph_utils.py .
!cp ../../text_normalization/en/utils.py .
! cd ../../..

from pynini.lib import pynutil

def apply_fst(text, fst):
  """ Given a string input, returns the output string
  produced by traversing the path with lowest weight.
  If no valid path accepts input string, returns an
  error.
  """
  try:
     print(pynini.shortestpath(text @ fst).string())
  except pynini.FstOpError:
    print(f"Error: No valid output with given input: '{text}'")

zeroE= pynini.string_map([("zero", "0")])
digitsE= pynini.string_map([("one", "1"),("two", "2"),("three", "3"),("four", "4"), ("five", "5"), ("six", "6"), 
                          ("seven", "7"), ("eight", "8"), ("nine", "9")])

teensE= pynini.string_map ([("eleven", "11"),
                            ("twelve", "12"),
                            ("thirteen", "13"),
                            ("fourteen", "14"),
                            ("fifteen", "15"),
                            ("sixteen", "16"),
                            ("seventeen", "17"),
                            ("eighteen", "18"), 
                            ("nineteen", "19"),
                            ])

tensE= pynini.string_map([("twenty", "2"),
                            ("thirty", "3"), 
                            ("fourty", "4"), 
                            ("sixty", "6"), 
                            ("seventy", "7"), 
                            ("eighty", "8"), 
                            ("ninety", "9"),
                            ("hundred", "10")])

graph_digitsE = digitsE | pynutil.insert("0")
delete_space = pynutil.delete(pynini.union("-", " "))
graph_tensE = tensE + graph_digitsE | tensE + delete_space + graph_digitsE
graph_allE = zeroE | graph_digitsE | teensE | graph_tensE

apply_fst("two", graph_allE)
apply_fst("thirty-three", graph_allE)
apply_fst("sixty", graph_allE)
apply_fst("eighteen", graph_allE)
apply_fst("sixteen", graph_allE)
apply_fst("twelve", graph_allE)
apply_fst("one", graph_allE)
apply_fst("twenty", graph_allE)
apply_fst("twenty-one", graph_allE)
apply_fst("hundred", graph_allE)
apply_fst("zero", graph_allE)
apply_fst("ninety-eight", graph_allE)
apply_fst("sixty nine", graph_allE)

zeroE= pynini.string_map([("0", "zero")])
digitsE= pynini.string_map( [("1", "one"),("2", "two"),("3", "three"),("4", "four"), ("5", "five"), ("6", "six"), 
                          ("7", "seven"), ("8", "eight"), ("9", "nine") ])

teensE= pynini.string_map ([("11", "eleven"),
                            ("12", "twelve"),
                            ("13", "thirteen"),
                            ("14", "fourteen"),
                            ("15", "fifteen"),
                            ("16", "sixteen"),
                            ("17", "seventeen"),
                            ("18", "eighteen"), 
                            ("19", "nineteen"),
                            ])

tens_plusE= pynini.string_map([("2", "twenty"),
                            ("3", "thirty"), 
                            ("4", "fourty"), 
                            ("6", "sixty"), 
                            ("7", "seventy"), 
                            ("8", "eighty"), 
                            ("9", "ninety")])

tensE= pynini.string_map([("20", "twenty"),
                            ("30", "thirty"), 
                            ("40", "fourty"), 
                            ("60", "sixty"), 
                            ("70", "seventy"), 
                            ("80", "eighty"), 
                            ("90", "ninety"),
                          ("100", "hundred")])

graph_digitsE = digitsE
insert_space = pynutil.insert("-")
graph_tens_plusE = tens_plusE + insert_space + graph_digitsE
graph_allE = zeroE | graph_digitsE | teensE | tensE |graph_tens_plusE

apply_fst("2", graph_allE)
apply_fst("33", graph_allE)
apply_fst("60", graph_allE)
apply_fst("18", graph_allE)
apply_fst("16", graph_allE)
apply_fst("12", graph_allE)
apply_fst("1", graph_allE)
apply_fst("20", graph_allE)
apply_fst("21", graph_allE)
apply_fst("100", graph_allE)
apply_fst("0", graph_allE)

ordinals= pynini.string_map([("1st", "first"),
                             ("2nd", "second"),
                             ("3rd", "third")])

strip_th = pynutil.delete("th")
graph_strip_th = NEMO_SIGMA + strip_th

apply_fst("33th", graph_strip_th)

add_th= pynutil.insert("th")
graph_add_th= NEMO_SIGMA + add_th

apply_fst("fife", graph_add_th)
apply_fst("33", graph_add_th)

graph_cardinals=  (graph_allE + graph_strip_th)
cardinal_to_ordinal= graph_cardinals + graph_add_th
graph_c_to_o = ordinals | cardinal_to_ordinal

apply_fst("second", inversion)

apply_fst("33th", graph_cardinals)

apply_fst("33th", cardinal_to_ordinal)

apply_fst("33th", cardinal_to_ordinal)

apply_fst("2nd", graph_c_to_o)
apply_fst("34th", graph_c_to_o)
apply_fst("60th", graph_c_to_o)
apply_fst("18th", graph_c_to_o)
apply_fst("16th", graph_c_to_o)
apply_fst("12th", graph_c_to_o)
apply_fst("1st", graph_c_to_o)
apply_fst("20th", graph_c_to_o)
apply_fst("3rd", graph_c_to_o)

inversion= pynini.invert(graph_c_to_o)

apply_fst("second", inversion)
apply_fst("thirty-fourth", inversion)
apply_fst("sixtyth", inversion)
apply_fst("eighteenth", inversion)
apply_fst("sixteenth", inversion)
apply_fst("twelveth", inversion)
apply_fst("first", inversion)
apply_fst("twentyth", inversion)
apply_fst("third", inversion)