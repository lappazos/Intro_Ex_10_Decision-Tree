##################################################################
# FILE : ex10.py
# WRITERS : Lior Paz,lioraryepaz,206240996
# EXERCISE : intro2cs ex10 2017-2018
# DESCRIPTION : illnesses decision tree
##################################################################

from collections import Counter
# for dict improvement
from copy import copy
# for list coping in build_tree
from itertools import combinations


# to create subsets


class Node:
    """
    This class creates the elements of the data structure we use - tree
    """

    def __init__(self, data="", pos=None, neg=None):
        """
        Constructor
        :param data: symptom / illness( in leaf)
        :param pos: positive child
        :param neg: negative child
        """
        self.data = data
        self.positive_child = pos
        self.negative_child = neg

    def get_positive(self):
        """
        A Method for node object
        :return: positive child
        """
        return self.positive_child

    def get_negative(self):
        """
        A Method for node object
        :return: negative child
        """
        return self.negative_child

    def get_data(self):
        """
        A Method for node object
        :return: symptom/illness
        """
        return self.data

    def is_leaf(self):
        """
        A Method for node object
        :return: is the node leaf
        """
        return self.positive_child is None


class Record:
    """
    Class that contain medical records, each object has its illness and his
    symptoms
    """

    def __init__(self, illness, symptoms):
        """
        Constructor
        :param illness: illness
        :param symptoms: symptoms
        """
        self.illness = illness
        self.symptoms = symptoms

    def get_symptoms(self):
        """
        A Method for record object
        :return: record's symptoms
        """
        return self.symptoms

    def get_illness(self):
        """
        A Method for record object
        :return: record's illness
        """
        return self.illness


def parse_data(filepath):
    """
    convert a txt file into records objects
    :param filepath: data file
    :return: list of record objects
    """
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    """
    each Diagnoser object has its own Tree and can diagnose according to it
    """

    def __init__(self, root):
        """
        Constructor
        :param root: node - root of tree
        """
        self.__root = root

    def diagnose(self, symptoms):
        """
        give a decision of illness according to symptoms
        :param symptoms:
        :return: illness string
        """
        node = self.__root
        return self.diagnose_helper(node, symptoms)

    def get_root(self):
        """
        A Method for Diagnoser object
        :return: tree root of diagnoser - node object
        """
        return self.__root

    def diagnose_helper(self, node, symptoms):
        """
        recursion helper to diagnose
        :param node: symptom to check if exist in patient
        :param symptoms: patient's symptoms
        :return: diagnosis string
        """
        # base case of recursion
        if node.is_leaf():
            return node.get_data()
        else:
            for symptom in symptoms:
                # yes track
                if symptom == node.get_data():
                    return self.diagnose_helper(node.get_positive(), symptoms)
            # no track
            return self.diagnose_helper(node.get_negative(), symptoms)

    def calculate_error_rate(self, records):
        """
        calculate arror rate of tree according to list of records
        :param records: list of record objects
        :return: integer of error rate
        """
        counter = 0
        for record in records:
            if self.diagnose(record.get_symptoms()) != record.get_illness():
                counter += 1
        return counter / len(records)

    def all_illnesses(self):
        """
        gives all leafes of tree, all existing illnesses in it
        :return: list of strings - illnesses
        """
        node = self.__root
        all_illnesses = set()
        # recursion helper function
        result = list(self.all_illness_helper(node, all_illnesses))
        result.sort()  # lexicographic order
        return result

    def all_illness_helper(self, node, all_illnesses):
        """
        recursion helper function
        :param node: node to follow
        :param all_illnesses: set of illnesses that updates with the recursion
        :return: set of all_illnesses
        """
        if node.is_leaf():
            all_illnesses.add(node.get_data())
            return all_illnesses
        else:
            all_illnesses.update(self.all_illness_helper(
                node.get_positive(), all_illnesses))
            all_illnesses.update(self.all_illness_helper(
                node.get_negative(), all_illnesses))
            return all_illnesses

    def most_common_illness(self, records):
        """
        most common illness in a list of records
        :param records: list of record objects
        :return: string
        """
        illnesses_dict = Counter()
        for record in records:
            illnesses_dict[self.diagnose(record.get_symptoms())] += 1
        return max(illnesses_dict, key=illnesses_dict.get)

    def paths_to_illness(self, illness):
        """
        gives all paths to illness
        :param illness: requested illness
        :return: list of lists
        """
        node = self.__root
        return self.paths_helper(illness, node)

    def paths_helper(self, illness, node):
        """
        helper function to recursion
        :param illness: requested illness
        :param node: node in progress of path check
        :return: temp path according to recursion phase
        """
        # my recursion is working bottom to top - it makes its way all the
        # way down to the leaf, and build the path on its way up
        if node.is_leaf():
            # base case
            if node.get_data() == illness:
                path = [[]]
                return path
            else:
                # if the illness wont fit - no path will be created
                path = []
                return path
        else:
            positive_paths = self.paths_helper(illness, node.get_positive())
            for path in positive_paths:
                path.insert(0, True)
            negative_paths = self.paths_helper(illness, node.get_negative())
            for path in negative_paths:
                path.insert(0, False)
            return positive_paths + negative_paths


def build_tree(records, symptoms):
    """
    build tree function
    :param records: records to create the leaves
    :param symptoms: symptoms to check in the tree
    :return: tree root
    """
    # in every phase i pop the first symptom out, that way till the end of
    # list.
    # in addition, i create yes & no lists along the recursion, so when ill
    # get to the leaf, ill be able to scan the records and choose the
    # correct illness candidates
    symptom = symptoms.pop(0)
    lst_add = [symptom]
    return Node(symptom,
                build_tree_helper(copy(symptoms), lst_add, [], records),
                build_tree_helper(copy(symptoms), [], lst_add, records))


def build_tree_helper(symptoms, yes_list, no_list, records):
    """
    helper function
    :param symptoms: symptoms to build the tree - change with the recursion
    :param yes_list: positive nodes in path
    :param no_list: negative nodes in path
    :param records: original records - list of record objects
    :return: node object - process of the recursion
    """
    # in every phase i pop the first symptom out, that way till the end of
    # list.
    # in addition, i create yes & no lists along the recursion, so when ill
    # get to the leaf, ill be able to scan the records and choose the
    # correct illness candidates
    if len(symptoms) > 0:
        symptom = symptoms.pop(0)
        lst_add = [symptom]
        return Node(symptom,
                    build_tree_helper(copy(symptoms), yes_list + lst_add,
                                      no_list, records),
                    build_tree_helper(copy(symptoms), yes_list, no_list +
                                      lst_add, records))
    else:
        # base case
        return Node(find_leaf(yes_list, no_list, records), None, None)


def find_leaf(yes_list, no_list, records):
    """
    determine the illness in the leaf
    :param yes_list: positive nodes
    :param no_list: negative nodes
    :param records: original records - list of record objects
    :return: illness string
    """
    illnesses_dict = Counter()
    for record in records:
        if symptom_check(no_list, record, yes_list):
            illnesses_dict[record.get_illness()] += 1
    if len(illnesses_dict) == 0:
        # if no match to record was found
        return records[0].get_illness()
    return max(illnesses_dict, key=illnesses_dict.get)


def symptom_check(no_list, record, yes_list):
    """
    check if record is good for leaf
    :param no_list: negative nodes
    :param record: record object to check
    :param yes_list: positive nodes
    :return: True or False
    """
    symptoms_to_check = record.get_symptoms()
    for symptom in yes_list:
        if symptom not in symptoms_to_check:
            return False
    for symptom in no_list:
        if symptom in symptoms_to_check:
            return False
    return True


def optimal_tree(records, symptoms, depth):
    """
    finds optimal tree to a given list of records, symptoms, in accuracy of
    specific depth
    :param records: list of record objects
    :param symptoms: list of symptoms
    :param depth: depth of trees to check
    :return: optimal tree root node object
    """
    combs = combinations(symptoms, depth)
    lowest = (1, None)
    for combination in combs:
        temp = Diagnoser(build_tree(records, list(combination)))
        temp_calc = temp.calculate_error_rate(records)
        if temp.calculate_error_rate(records) < lowest[0]:
            lowest = (temp_calc, temp)
    return lowest[1].get_root()
