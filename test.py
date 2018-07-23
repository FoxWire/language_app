'''
This looks like it could be used to compare trees and get a sort of distance from them.
This could be a better way of comparing chunks. Or it could be used to improve the current 
algorithm.


- create an algorithm that will take a parse tree and convert it into one of these parse trees.
'''
from zss import simple_distance, Node
from nltk.parse import stanford
import json
import re


A = (
    Node("f")
        .addkid(Node("a")
            .addkid(Node("d"))
            .addkid(Node("c")
                .addkid(Node("b"))))
        .addkid(Node("e"))
    )
B = (
    Node("f")
        .addkid(Node("a")
            .addkid(Node("d"))
            .addkid(Node("c")
                .addkid(Node("b"))))
        .addkid(Node("e"))
    )

test_tree = (
    Node("ROOT")
        .addkid(Node("S")
            .addkid(Node("NP")
                .addkid(Node("PRP")
                    .addkid(Node("I"))))
            .addkid(Node("VP")
                .addkid(Node("VBP")
                    .addkid(Node("am"))))
                .addkid(Node("NP")
                    .addkid(Node("NNP")
                        .addkid(Node("Stuart")))))
    )



parser = stanford.StanfordParser()

# These are the sentences to be parsed
chunk = 'I am Stuart' 

# parse the sentences
tree = next(parser.raw_parse(chunk))

tree.pretty_print()

tree_as_string = str(tree)
print(tree_as_string)

tree_as_list = [item.strip() for item in re.split(r'([\(\)])', tree_as_string) if item.strip()]
# At this point the string is processed and ready to be worked on.

def convert_parse_tree_to_python_tree(tree_as_list):
    tree_as_list = tree_as_list[2:-1]
    stack = [ ['ROOT', []],  ]
    root = stack[0]
    # Iterate over the list
    for i, item in enumerate(tree_as_list):
        if item == '(':

            # If the node doesn't have children
            match = re.search(r'[A-Z]+[ ][A-Za-z]+', tree_as_list[i + 1])
            if match:
                label = match.group().split(' ')
                node = [label[0], label[1]]
            else:
                node = [tree_as_list[i + 1], []]

            # Add the node to the children of the current item
            stack[-1][1].append(node)
            # Then add the node to the stack itself
            stack.append(node)
        elif item == ')':
            # this node has no children so just pop it from the stack
            stack.pop()
    return root




def convert_parse_tree_to_zss_tree(tree_as_list):
    tree_as_list = tree_as_list[2:-1]
    stack = [Node('ROOT')]
    root_node = stack[0]
    # Iterate over the list
    for i, item in enumerate(tree_as_list):
        if item == '(':
            # match the string for each item 
            match = re.search(r'[A-Z]+[ ][A-Za-z]+', tree_as_list[i + 1])
            if match:
                # if match, node has no children
                label = match.group().split(' ')
                node = Node(label[0]).addkid(Node(label[1]))
            else:
                # otherwise node has children
                node = Node(tree_as_list[i + 1])
            # Add the node to the children of the current item
            stack[-1].addkid(node)
            # Then add the node to the stack itself
            stack.append(node)
        elif item == ')':
            # this node has no children so just pop it from the stack
            stack.pop()
    return root_node


zss_tree = convert_parse_tree_to_zss_tree(tree_as_list)

print(simple_distance(zss_tree, test_tree))
print()
print(zss_tree)
print()
print(test_tree)



