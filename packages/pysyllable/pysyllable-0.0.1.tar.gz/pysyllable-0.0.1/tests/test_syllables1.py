from __future__ import division
import re

import cmudict
import syllables

from pysyllable import syllable

x=syllable('pharyntial')


def test_estimate():
    EXPECTED_ACCURACY = 0.95
    hits = []
    misses = []

    dictionary = cmudict.dict()
    for word in dictionary:
        phones = dictionary[word][0]
        cmudict_syllables = 0
        for phone in phones:
            if re.match(r"\w*[012]$", phone):
                cmudict_syllables += 1
        # estimated_syllables = syllables.estimate(word)
        estimated_syllables = syllable(word)
        if cmudict_syllables == estimated_syllables: # or cmudict_syllables>=3 and estimated_syllables>=3:
            hits.append(word)
        else:
            print(f'{word} expected {cmudict_syllables} but received {estimated_syllables}')
            misses.append(word)

    hit = len(hits)
    miss = len(misses)
    # print(misses)
    total = hit + miss
    ACCURACY = hit / total
    print(f"syllables.estimate(): Expected accuracy of {EXPECTED_ACCURACY}, got {ACCURACY}.")


#     if ACCURACY < EXPECTED_ACCURACY:
#         raise AssertionError(
#             "syllables.estimate(): Expected accuracy of {0}, got {1}.".format(
#                 EXPECTED_ACCURACY, ACCURACY
#             )
#         )

test_estimate()
