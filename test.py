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


one = (
        Node("ROOT")
            .addkid(Node('S')
                .addkid(Node('VP')
                            .addkid(Node('VB'))
                            .addkid(Node('RB'))
                            .addkid(Node('VP')
                                .addkid(Node('VB'))
                                .addkid(Node('NP')
                                    .addkid(Node('PRP$'))
                                    .addkid(Node('NN')))
                                .addkid(Node('PP')
                                    .addkid(Node("IN"))
                                    .addkid(Node('NP')
                                        .addkid(Node("NN")))
                                    )
                                )))
    )

two = (
        Node("ROOT")
            .addkid(Node('S')
                .addkid(Node('VP')
                            .addkid(Node('VB'))
                            .addkid(Node('RB'))
                            .addkid(Node('VP')
                                .addkid(Node('VB'))
                                .addkid(Node('NP')
                                    .addkid(Node('PRP$'))
                                    .addkid(Node('NN')))
                                .addkid(Node('PP')
                                    .addkid(Node("IN"))
                                    .addkid(Node('NP')
                                        .addkid(Node("NN")))
                                    )
                                )))
    )



# A = (
#     Node("f")
#         .addkid(Node("a")
#             .addkid(Node("h"))
#             .addkid(Node("c")
#                 .addkid(Node("l"))))
#         .addkid(Node("e"))
#     )
# B = (
#     Node("f")
#         .addkid(Node("a")
#             .addkid(Node("d"))
#             .addkid(Node("c")
#                 .addkid(Node("b"))))
#         .addkid(Node("e"))
#     )
# print(simple_distance(one, two))


parser = stanford.StanfordParser()

# These are the sentences to be parsed
chunk_a = 'I am Stuart' 
# chunk_b = 'This is just a test sentence'

# parse the sentences
tree_a = next(parser.raw_parse(chunk_a))
# tree_b = next(parser.raw_parse(chunk_b))

tree_a.pretty_print()

# You may just have to iterate over the string representation
string_rep = str(tree_a)


string_rep = "".join(string_rep.split('\n'))
string_rep = string_rep.replace('(', '[').replace(')', ']')    


print(string_rep)

string_b = "[S [NP [PRP I]] [VP [VBP am] [NP [NNP Stuart]]]]"

string_a = "[X [X [X None]] [X [X None] [X [X None]]]]"

x = re.split(r'([^A-Za-z])', string_b)
list_b = [y for y in x if y and y != ' ']

stack = [ ['ROOT', []],  ]
root = stack[0]
# Iterate though the string 
for i, item in enumerate(list_b):
    if item == '[':
        node = [list_b[i + 1], [], ]
        # Add the node to the children of the current item
        stack[-1][1].append(node)
        # Then add the node to the stack itself
        stack.append(node)
    elif item == ']':
        # this node has no children so just pop it from the stack
        stack.pop()

import pdb; pdb.set_trace()


