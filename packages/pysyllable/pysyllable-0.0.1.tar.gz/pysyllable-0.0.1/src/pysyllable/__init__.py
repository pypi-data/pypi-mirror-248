import re
from pluralizer import Pluralizer
# from normalize_strings import normalize

from .problematic import problematic

pluralizer = Pluralizer()

# own = {}.hasOwnProperty

# Two expressions of occurrences which normally would be counted as two
# syllables, but should be counted as one.
# EXPRESSION_MONOSYLLABIC_ONE = re.compile(
#     r'awe($|d|so)|cia(?:l|$)|tia|cius|cious|[^aeiou]giu|[aeiouy][^aeiouy]ion|iou|sia$|eous$|[oa]gue$|.[^aeiuoycgltdb]{2,}ed$|.ely$|^jua|uai|eau|^busi$|(?:[aeiouy](?:[bcfgklmnprsvwxyz]|ch|dg|g[hn]|lch|l[lv]|mm|nch|n[cgn]|r[bcnsv]|squ|s[chkls]|th))ed$|(?:[aeiouy](?:[bdfklmnprstvy]|ch|g[hn]|lch|l[lv]|mm|nch|nn|r[nsv]|squ|s[cklst]|th))es$',
#     re.MULTILINE
# )

# const 
EXPRESSION_MONOSYLLABIC_ONE = re.compile(
  '|'.join([
    'awe($|d|so)',
    'cia(?:l|$)',
    'tia',
    'cius',
    'cious',
    '[^aeiou]giu',
    '[aeiouy][^aeiouy]ion',
    'iou',
    'sia$',
    'eous$',
    '[oa]gue$',
    '.[^aeiuoycgltdb]{2,}ed$',
    '.ely$',
    '^jua',
    'uai',
    'eau',
    '^busi$',
    '(?:[aeiouy](?:' +
      "|".join([
        '[bcfgklmnprsvwxyz]',
        'ch',
        'dg',
        'g[hn]',
        'lch',
        'l[lv]',
        'mm',
        'nch',
        'n[cgn]',
        'r[bcnsv]',
        'squ',
        's[chkls]',
        'th'
      ]) +
      ')ed$)',
    '(?:[aeiouy](?:' +
      '|'.join([
        '[bdfklmnprstvy]',
        'ch',
        'g[hn]',
        'lch',
        'l[lv]',
        'mm',
        'nch',
        'nn',
        'r[nsv]',
        'squ',
        's[cklst]',
        'th'
      ]) +
      ')es$)'
  ]),
  re.MULTILINE 
)


# EXPRESSION_MONOSYLLABIC_TWO = re.compile(
#     r'[aeiouy](?:[bcdfgklmnprstvyz]|ch|dg|g[hn]|l[lv]|mm|n[cgns]|r[cnsv]|squ|s[cklst]|th)e$',
#     re.MULTILINE
# )

# const 
EXPRESSION_MONOSYLLABIC_TWO = re.compile(
  '[aeiouy](?:' +
    "|".join([
      '[bcdfgklmnprstvyz]',
      'ch',
      'dg',
      'g[hn]',
      'l[lv]',
      'mm',
      'n[cgns]',
      'r[cnsv]',
      'squ',
      's[cklst]',
      'th'
    ]) +
    ')e$',
  re.MULTILINE
)

# Four expression of occurrences which normally would be counted as one
# syllable, but should be counted as two.
# const 
EXPRESSION_DOUBLE_SYLLABIC_ONE = re.compile(
  '(?:' +
    '|'.join([
      '([^aeiouy])\\1l',
      '[^aeiouy]ie(?:r|s?t)',
      '[aeiouym]bl',
      'eo',
      'ism',
      'asm',
      'thm',
      'dnt',
      'snt',
      'uity',
      'dea',
      'gean',
      'oa',
      'ua',
      'react?',
      'orbed', # Cancel `'.[^aeiuoycgltdb]{2,}ed$',`
      'shred', # Cancel `'.[^aeiuoycgltdb]{2,}ed$',`
      'eings?',
      '[aeiouy]sh?e[rs]'
    ]) +
    ')$',
  re.MULTILINE
)

#const 
EXPRESSION_DOUBLE_SYLLABIC_TWO = re.compile(
  '|'.join([
    'creat(?!u)',
    '[^gq]ua[^auieo]',
    '[aeiou]{3}',
    '^(?:ia|mc|coa[dglx].)',
    '^re(app|es|im|us)',
    '(th|d)eist'
  ]),
  re.MULTILINE 
)

# const 
EXPRESSION_DOUBLE_SYLLABIC_THREE = re.compile(
  '|'.join([
    '[^aeiou]y[ae]',
    '[^l]lien',
    'riet',
    'dien',
    'iu',
    'io',
    'ii',
    'uen',
    '[aeilotu]real',
    'real[aeilotu]',
    'iell',
    'eo[^aeiou]',
    '[aeiou]y[aeiou]'
  ]),
  re.MULTILINE
)

# const 
EXPRESSION_DOUBLE_SYLLABIC_FOUR = re.compile('[^s]ia')

# Expression to match single syllable pre- and suffixes.
# const 
EXPRESSION_SINGLE = re.compile(
  '|'.join([
    '^(?:' +
      '|'.join([
        'un',
        'fore',
        'ware',
        'none?',
        'out',
        'post',
        'sub',
        'pre',
        'pro',
        'dis',
        'side',
        'some'
      ]) +
      ')',
    '(?:' +
      '|'.join([
        'ly',
        'less',
        'some',
        'ful',
        'ers?',
        'ness',
        'cians?',
        'ments?',
        'ettes?',
        'villes?',
        'ships?',
        'sides?',
        'ports?',
        'shires?',
        '[gnst]ion(?:ed|s)?'
      ]) +
      ')$'
  ]),
  re.MULTILINE
)

# Expression to match double syllable pre- and suffixes.
# const 
EXPRESSION_DOUBLE = re.compile(
  '|'.join([
    '^' +
      '(?:' +
      '|'.join([
        'above',
        'anti',
        'ante',
        'counter',
        'hyper',
        'afore',
        'agri',
        'infra',
        'intra',
        'inter',
        'over',
        'semi',
        'ultra',
        'under',
        'extra',
        'dia',
        'micro',
        'mega',
        'kilo',
        'pico',
        'nano',
        'macro',
        'somer'
      ]) +
      ')',
    '(?:fully|berry|woman|women|edly|union|((?:[bcdfghjklmnpqrstvwxz])|[aeiou])ye?ing)$'
  ]),
  re.MULTILINE
)

# Expression to match triple syllable suffixes.
# const 
EXPRESSION_TRIPLE = re.compile('(creations?|ology|ologist|onomy|onomist)$',re.MULTILINE)

# /**
#  * Count syllables in `value`.
#  *
#  * @param {string} value
#  *   Value to check.
#  * @returns {number}
#  *   Syllables in `value`.
#  */
def syllable(value):
    # Lower case
    # Remove apostrophes.
    # Split on word boundaries.

    values = re.sub(r"['’]", '', str(value).lower()) # FIXME: .split(r'\b')
    values = re.split('[-.;:,| ]', values)
    index = 0
    sum = 0
    while index < len(values):
        sum += one(re.sub(r'[^a-z]', '', values[index]))
        index += 1
    return sum

# /**
#  * Get syllables in a word.
#  *
#  * @param {string} value
#  * @returns {number}
#  */
def one(value):
    global count
    count = 0

    if len(value) == 0:
        return count

    # Return early when possible.
    if len(value) < 3:
        return 1

    # If `value` is a hard to count, it might be in `problematic`.
    if value in problematic:
        return problematic[value]

    # Additionally, the singular word might be in `problematic`.
    singular = pluralizer.pluralize(value, 1)

    if singular in problematic:
        return problematic[singular]

    add_one = return_factory(1)
    subtract_one = return_factory(-1)

    # Count some prefixes and suffixes, and remove their matched ranges.
    value = re.sub(EXPRESSION_TRIPLE, count_factory(3), value)
    value = re.sub(EXPRESSION_DOUBLE, count_factory(2), value)
    value = re.sub(EXPRESSION_SINGLE, count_factory(1), value)

    # Count multiple consonants.
    parts = re.split(r'[^aeiouy]+', value)
    index = -1
    
    while index + 1 < len(parts):
        if parts[index] != '':
            count += 1
        index += 1
    
    # Subtract one for occurrences which should be counted as one (but are
    # counted as two).
    value = re.sub(EXPRESSION_MONOSYLLABIC_ONE, subtract_one, value)
    value = re.sub(EXPRESSION_MONOSYLLABIC_TWO, subtract_one, value)
    
    # Add one for occurrences which should be counted as two (but are counted as
    # one).
    value = re.sub(EXPRESSION_DOUBLE_SYLLABIC_ONE, add_one, value)
    value = re.sub(EXPRESSION_DOUBLE_SYLLABIC_TWO, add_one, value)
    value = re.sub(EXPRESSION_DOUBLE_SYLLABIC_THREE, add_one, value)
    value = re.sub(EXPRESSION_DOUBLE_SYLLABIC_FOUR, add_one, value)

    # Make sure at least one is returned.
    return count or 1

def count_factory(addition):
    def counter(value):
        global count
        count += addition
        return ''

    return counter

def return_factory(addition):
    def returner(value):
        global count
        count += addition
        return value.group(0)

    return returner

