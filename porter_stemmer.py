def check_aeiou(letter):
    if letter == 'a' or letter == 'e' or letter == 'i' or letter == 'o' or letter == 'u':
        return False
    else:
        return True


def check_consonant(word, i):
    letter = word[i]
    if check_aeiou(letter):
        if letter == 'y' and check_aeiou(word[i-1]):
            return False
        else:
            return True
    else:
        return False


def check_vowel(word, i):
    return not(check_consonant(word, i))




def check_ending_letter(stem, letter):
    if stem.endswith(letter):
        return True
    else:
        return False




def have_vowel(stem):
    for i in stem:
        if not check_aeiou(i):
            return True
    return False



def check_last_2_digits(stem):
    if len(stem) >= 2:
        if check_consonant(stem, -1) and check_consonant(stem, -2):
            return True
        else:
            return False
    else:
        return False


def check_form(word):

    form = []
    formStr = ''
    for i in range(len(word)):
        if check_consonant(word, i):
            if i != 0:
                prev = form[-1]
                if prev != 'C':
                    form.append('C')
            else:
                form.append('C')
        else:
            if i != 0:
                prev = form[-1]
                if prev != 'V':
                    form.append('V')
            else:
                form.append('V')
    for j in form:
        formStr += j
    return formStr


def count_vowel_consonant(word):
    form = check_form(word)
    m = form.count('VC')
    return m



def check_last_digit_wxy(word):
    if len(word) >= 3:
        f = -3
        s = -2
        t = -1
        third = word[t]
        if check_consonant(word, f) and check_vowel(word, s) and check_consonant(word, t):
            if third != 'w' and third != 'x' and third != 'y':
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def replace(orig, rem, rep):
    result = orig.rfind(rem)
    base = orig[:result]
    replaced = base + rep
    return replaced


def replace_vc0(orig, rem, rep):
    result = orig.rfind(rem)
    base = orig[:result]
    if count_vowel_consonant(base) > 0:
        replaced = base + rep
        return replaced
    else:
        return orig


def replace_vc1(orig, rem, rep):
    result = orig.rfind(rem)
    base = orig[:result]
    if count_vowel_consonant(base) > 1:
        replaced = base + rep
        return replaced
    else:
        return orig


def step1(word):
    if word.endswith('sses'):
        word = replace(word, 'sses', 'ss')
    elif word.endswith('ies'):
        word = replace(word, 'ies', 'i')
    elif word.endswith('ss'):
        word = replace(word, 'ss', 'ss')
    elif word.endswith('s'):
        word = replace(word, 's', '')
    else:
        pass

    flag = False
    if word.endswith('eed'):
        result = word.rfind('eed')
        base = word[:result]
        if count_vowel_consonant(base) > 0:
            word = base
            word += 'ee'
    elif word.endswith('ed'):
        result = word.rfind('ed')
        base = word[:result]
        if have_vowel(base):
            word = base
            flag = True
    elif word.endswith('ing'):
        result = word.rfind('ing')
        base = word[:result]
        if have_vowel(base):
            word = base
            flag = True
    if flag:
        if word.endswith('at') or word.endswith('bl') or word.endswith('iz'):
            word += 'e'
        elif check_last_2_digits(word) and not check_ending_letter(word, 'l') and not check_ending_letter(word, 's') and not check_ending_letter(word, 'z'):
            word = word[:-1]
        elif count_vowel_consonant(word) == 1 and check_last_digit_wxy(word):
            word += 'e'
        else:
            pass
    else:
        pass
    
    if word.endswith('y'):
        result = word.rfind('y')
        base = word[:result]
        if have_vowel(base):
            word = base
            word += 'i'
    
    return word

def step2(word):
    if word.endswith('ational'):
        word = replace_vc0(word, 'ational', 'ate')
    elif word.endswith('tional'):
        word = replace_vc0(word, 'tional', 'tion')
    elif word.endswith('enci'):
        word = replace_vc0(word, 'enci', 'ence')
    elif word.endswith('anci'):
        word = replace_vc0(word, 'anci', 'ance')
    elif word.endswith('izer'):
        word = replace_vc0(word, 'izer', 'ize')
    elif word.endswith('abli'):
        word = replace_vc0(word, 'abli', 'able')
    elif word.endswith('alli'):
        word = replace_vc0(word, 'alli', 'al')
    elif word.endswith('entli'):
        word = replace_vc0(word, 'entli', 'ent')
    elif word.endswith('eli'):
        word = replace_vc0(word, 'eli', 'e')
    elif word.endswith('ousli'):
        word = replace_vc0(word, 'ousli', 'ous')
    elif word.endswith('ization'):
        word = replace_vc0(word, 'ization', 'ize')
    elif word.endswith('ation'):
        word = replace_vc0(word, 'ation', 'ate')
    elif word.endswith('ator'):
        word = replace_vc0(word, 'ator', 'ate')
    elif word.endswith('alism'):
        word = replace_vc0(word, 'alism', 'al')
    elif word.endswith('iveness'):
        word = replace_vc0(word, 'iveness', 'ive')
    elif word.endswith('fulness'):
        word = replace_vc0(word, 'fulness', 'ful')
    elif word.endswith('ousness'):
        word = replace_vc0(word, 'ousness', 'ous')
    elif word.endswith('aliti'):
        word = replace_vc0(word, 'aliti', 'al')
    elif word.endswith('iviti'):
        word = replace_vc0(word, 'iviti', 'ive')
    elif word.endswith('biliti'):
        word = replace_vc0(word, 'biliti', 'ble')
    return word


def step3(word):
    if word.endswith('icate'):
        word = replace_vc0(word, 'icate', 'ic')
    elif word.endswith('ative'):
        word = replace_vc0(word, 'ative', '')
    elif word.endswith('alize'):
        word = replace_vc0(word, 'alize', 'al')
    elif word.endswith('iciti'):
        word = replace_vc0(word, 'iciti', 'ic')
    elif word.endswith('ful'):
        word = replace_vc0(word, 'ful', '')
    elif word.endswith('ness'):
        word = replace_vc0(word, 'ness', '')
    return word


def step4(word):
    if word.endswith('al'):
        word = replace_vc1(word, 'al', '')
    elif word.endswith('ance'):
        word = replace_vc1(word, 'ance', '')
    elif word.endswith('ence'):
        word = replace_vc1(word, 'ence', '')
    elif word.endswith('er'):
        word = replace_vc1(word, 'er', '')
    elif word.endswith('ic'):
        word = replace_vc1(word, 'ic', '')
    elif word.endswith('able'):
        word = replace_vc1(word, 'able', '')
    elif word.endswith('ible'):
        word = replace_vc1(word, 'ible', '')
    elif word.endswith('ant'):
        word = replace_vc1(word, 'ant', '')
    elif word.endswith('ement'):
        word = replace_vc1(word, 'ement', '')
    elif word.endswith('ment'):
        word = replace_vc1(word, 'ment', '')
    elif word.endswith('ent'):
        word = replace_vc1(word, 'ent', '')
    elif word.endswith('ou'):
        word = replace_vc1(word, 'ou', '')
    elif word.endswith('ism'):
        word = replace_vc1(word, 'ism', '')
    elif word.endswith('ate'):
        word = replace_vc1(word, 'ate', '')
    elif word.endswith('iti'):
        word = replace_vc1(word, 'iti', '')
    elif word.endswith('ous'):
        word = replace_vc1(word, 'ous', '')
    elif word.endswith('ive'):
        word = replace_vc1(word, 'ive', '')
    elif word.endswith('ize'):
        word = replace_vc1(word, 'ize', '')
    elif word.endswith('ion'):
        result = word.rfind('ion')
        base = word[:result]
        if count_vowel_consonant(base) > 1 and (check_ending_letter(base, 's') or check_ending_letter(base, 't')):
            word = base
        word = replace_vc1(word, '', '')
    return word


def step5(word):
    if word.endswith('e'):
        base = word[:-1]
        if count_vowel_consonant(base) > 1:
            word = base
        elif count_vowel_consonant(base) == 1 and not check_last_digit_wxy(base):
            word = base
    
    if count_vowel_consonant(word) > 1 and check_last_2_digits(word) and check_ending_letter(word, 'l'):
        word = word[:-1]
    return word



def stem(word):
    word = step1(word)
    word = step2(word)
    word = step3(word)
    word = step4(word)
    word = step5(word)
    return word
