# -*- coding: utf-8 -*-
"""GermanTN & ITN for Cardinals and Ordinals.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ELMv8xHru6E8n7ntjbmY1sbWidPTqi5L
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

LANGUAGE= "German" # Change this to your desired language

# Commented out IPython magic to ensure Python compatibility.
# %cd nemo_text_processing/inverse_text_normalization/
!mkdir {LANGUAGE}
!mkdir "German/taggers"
!mkdir "German/verbalizers"
!mkdir "German/data"
# %cd {German}
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

# pynini function that creates explicit input-output mappings for a WFST
zeroG = pynini.string_map([("0", "null")]) 
digitsG = pynini.string_map([
				("1", "eins"),
				("2", "zwei"),
				("3", "drei"),
				("4", "vier"),
				("5", "f??nf"),
				("6", "sechs"),
				("7", "sieben"),
				("8", "acht"),
				("9","neun")
])

digits_plusG = pynini.string_map([
				("2", "zwei"),
				("3", "drei"),
				("4", "vier"),
				("5", "f??nf"),
				("6", "sechs"),
				("7", "sieben"),
				("8", "acht"),
				("9","neun")
])

teensG= pynini.string_map ([("11", "elf"),
                            ("12", "zw??lf"),
                            ("13", "dreizehn"),
                            ("14", "vierzehn"),
                            ("15", "f??nfzehn"),
                            ("16", "sechzehn"),
                            ("17", "siebzehn"),
                            ("18", "achtzehn"), 
                            ("19", "neunzehn"),
                            ])

tensG= pynini.string_map([("20", "zwanzig"),
                            ("30", "drei??ig"), 
                            ("40", "vierzig"), 
                            ("50", "f??nfzig"),
                            ("60","sechzig"), 
                            ("70", "siebzig"), 
                            ("80", "achtzig"), 
                            ("90", "neunzig"),
                            ("100","(ein)hundert")])

tens_plusG= pynini.string_map([("1","ein"),
                            ("2","zwanzig"),
                            ("3", "drei??ig"), 
                            ("4", "vierzig"), 
                            ("5", "f??nfzig"),
                            ("6","sechzig"), 
                            ("7", "siebzig"), 
                            ("8", "achtzig"), 
                            ("9", "neunzig")])

graph_digitsG = digitsG
insert_and = pynutil.insert("und")
graph_tens_plusG = digits_plusG + insert_and + tens_plusG
graph_allG = zeroG | digitsG | teensG | tensG | graph_tens_plusG

apply_fst("2", graph_allG)
apply_fst("33", graph_allG)
apply_fst("60", graph_allG)
apply_fst("18", graph_allG)
apply_fst("16", graph_allG)
apply_fst("12", graph_allG)
apply_fst("1", graph_allG)
apply_fst("20", graph_allG)
apply_fst("21", graph_allG)
apply_fst("100", graph_allG)
apply_fst("0", graph_allG)

inversion= pynini.invert(graph_allG)

apply_fst("zwei", inversion)
apply_fst("dreiunddrei??ig", inversion)
apply_fst("sechzig", inversion)
apply_fst("achtzehn", inversion)
apply_fst("sechzehn", inversion)
apply_fst("zw??lf", inversion)
apply_fst("zw??lf", inversion)
apply_fst("eins", inversion)
apply_fst("zwanzig", inversion)
apply_fst("(ein)hundert", inversion)
apply_fst("null", inversion)

#ordinals= pynini.string_map([("1st", "first"),
                             #("2nd", "second"),
                             #("3rd", "third")])

strip_dot = pynutil.delete(".")
graph_strip_dot = NEMO_SIGMA + strip_dot

apply_fst("21.", graph_strip_dot)

add_te= pynutil.insert("te")
graph_add_te= NEMO_SIGMA + add_te

add_ste= pynutil.insert("ste")
graph_add_ste= NEMO_SIGMA + add_ste

apply_fst("21.", graph_add_te)

_digit19 = pynini.union("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19")

graph_digit19=  graph_strip_dot @ _digit19 @ graph_allG @ graph_add_te

apply_fst("2.", graph_digit19)

graph_20=   graph_strip_dot @ graph_allG @ graph_add_ste

graph_c_to_o= graph_digit19 | graph_20

apply_fst("2.", graph_c_to_o)
apply_fst("34.", graph_c_to_o)
apply_fst("60.", graph_c_to_o)
apply_fst("18.", graph_c_to_o)
apply_fst("16.", graph_c_to_o)
apply_fst("12.", graph_c_to_o)
apply_fst("1.", graph_c_to_o)
apply_fst("2.", graph_c_to_o)
apply_fst("3.", graph_c_to_o)

inversion= pynini.invert(graph_c_to_o)

apply_fst("zweiste", inversion)
apply_fst("dreiundvierzigste", inversion)
apply_fst("sechzigste", inversion)
apply_fst("achtzehnste", inversion)
apply_fst("sechzehnste", inversion)
apply_fst("zw??lfste", inversion)
apply_fst("einsste", inversion)
apply_fst("zweiste", inversion)
apply_fst("dreiste", inversion)