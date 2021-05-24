from porter_stemmer import *

# validate query
def validate_query(terms, operators, query):
    if terms == []:
        return False
    elif operators == [] and len(terms) > 1:
        return False
    elif len(operators) > len(terms):
        return False
    else:
        return True

# checking operators
def check_term(term):
    if (term not in ['and', 'or', 'not']) and term[0] != '/':
        return True
    # endif
    return False


# processing / operator
def process_proximity_operator(index, term, terms, query, inverted_index):

    if (index-2 >= 0) and check_term(query[index - 1]) and check_term(query[index - 2]) and (terms[-1] in inverted_index) and (terms[-2] in inverted_index):

        combined_term = []
        combined_term.append(terms.pop(-2))
        combined_term.append(terms.pop(-1))
        combined_term.append(int(term[1:]))
        terms.append(combined_term)

    else:
        while terms != [] and check_term(terms[-1]):
            terms.pop()
        # endwhile

    # endif


# for AND of two terms
def intersection(list1, list2):
    list1 = set(list1)
    resultant = [docID for docID in list2 if docID in list1]
    return resultant


# for OR of two terms
def union(list1, list2):
    resultant = list(set().union(list1, list2))
    return sorted(resultant)


# for NOT of a term
def NOT(list1):
    resultant = []
    for docID in range(1, 51):
        if docID not in list1:
            resultant.append(docID)
        # endif
    # endfor
    return resultant


# for proximity queries
def proximity(docs, posting_list1, posting_list2, numOf_words_inBetween):
    resultant = []

    for docID in docs:  # 9,11
        if len(posting_list1[docID]) <= len(posting_list2[docID]):
            for position in posting_list1[docID]:
                if ((position-numOf_words_inBetween) >= 1) and ((position-numOf_words_inBetween) in posting_list2[docID]):
                    resultant.append(docID)
                    break
                elif (position+numOf_words_inBetween) in posting_list2[docID]:
                    resultant.append(docID)
                    break
                # endif
            # endfor
        else:
            for position in posting_list2[docID]:
                if ((position-numOf_words_inBetween) >= 1) and ((position-numOf_words_inBetween) in posting_list1[docID]):
                    resultant.append(docID)
                    break
                elif (position+numOf_words_inBetween) in posting_list1[docID]:
                    resultant.append(docID)
                    break
                # endif
            # endfor
        # endif
    # endfor
    return resultant


# processing a single query term during the process of searching the inverted_index
def process_single_term(term, inverted_index):
    if str(type(term)) == "<class 'list'>":
        if len(term) == 2:
            docs = NOT(inverted_index[term[1]])
        else:
            docs = intersection(
                inverted_index[term[0]], inverted_index[term[1]])

            docs = proximity(
                docs, inverted_index[term[0]], inverted_index[term[1]], term[2] + 1)
        # endif
    else:
        docs = list(inverted_index[term].keys())
    # endif
    return docs


# for processing the user's query
def query_processing(query, inverted_index):
    terms = []
    operators = []
    index = 0

    while(index < len(query)):
        term = stem(query[index])
        if check_term(term):
            if term in inverted_index:
                terms.append(stem(term))
        elif term == 'not':
            if (index+1 < len(query)) and check_term(query[index+1]) and query[index+1] in inverted_index:
                terms.append(['not', query[index+1]])
            index = index + 1
        elif term[0] == '/':
            process_proximity_operator(
                index, term, terms, query, inverted_index)
        else:
            operators.append(term)
        # endif

        index = index + 1
    # endwhile
    return (terms, operators)


# for searching the inverted_index
def search(query, inverted_index):
    
    (terms, operators) = query_processing(query, inverted_index)

    valid = validate_query(terms, operators, query)
    if not valid:
        return []

    # processing first term of the query
    term = terms.pop(0)
    docs = process_single_term(term, inverted_index)

    # processing the rest of the terms in the query if any.
    if terms != []:
        while (terms != []):
            term = terms.pop(0)
            list2 = process_single_term(term, inverted_index)

            operator = operators.pop(0)
            if operator == 'and':
                docs = intersection(docs, list2)
            elif operator == 'or':
                docs = union(docs, list2)
            # endif

        # endwhile
    # endif
    return docs
