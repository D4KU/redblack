import importlib
import unittest
import random
from datetime import datetime

import tree
importlib.reload(tree)
from tree import Tree, Node


class RbTreeTests(unittest.TestCase):

    def test_add(self):
        """ Use the tree we get from the test_build function
            and test the find function on each node"""
        rb_tree = Tree()
        rb_tree.insert(2)
        node_2 = rb_tree.root
        rb_tree.insert(1)
        node_1 = rb_tree.root.left
        rb_tree.insert(4)
        node_4 = rb_tree.root.right
        rb_tree.insert(5)
        node_5 = node_4.right
        rb_tree.insert(9)
        node_9 = node_5.right
        rb_tree.insert(3)
        node_3 = node_4.left
        rb_tree.insert(6)
        node_6 = node_9.left
        rb_tree.insert(7)
        node_7 = node_5.right
        rb_tree.insert(15)
        node_15 = node_9.right
        """
                            ___5B___
                        __2R__      7R
                      1B     4B    6B 9B
                            3R         15R
        """
        # valid cases
        self.assertEqual(rb_tree[5], node_5)
        self.assertEqual(rb_tree[2], node_2)
        self.assertEqual(rb_tree[1], node_1)
        self.assertEqual(rb_tree[4], node_4)
        self.assertEqual(rb_tree[3], node_3)
        self.assertEqual(rb_tree[7], node_7)
        self.assertEqual(rb_tree[6], node_6)
        self.assertEqual(rb_tree[9], node_9)
        self.assertEqual(rb_tree[15], node_15)
        # invalid cases
        with self.assertRaises(KeyError):
            rb_tree[-1]
        with self.assertRaises(KeyError):
            rb_tree[52454225]
        with self.assertRaises(KeyError):
            rb_tree[0]
        with self.assertRaises(KeyError):
            rb_tree[401]
        with self.assertRaises(KeyError):
            rb_tree[3.00001]

    # ***************TEST INSERTIONS***************

    def test_recoloring_only(self):
        """
        Create a red-black tree, add a red node such that we only have to recolor
        upwards twice
        add 4, which recolors 2 and 8 to False,
                6 to True
                    -10, 20 to False
        :return:
        """
        tree = Tree()
        root = Node(key=10, red=False, parent=None)
        # LEFT SUBTREE
        node_m10 = Node(key=-10, red=True, parent=root) #OK
        node_6 = Node(key=6, red=False, parent=node_m10) #OK
        node_8 = Node(key=8, red=True, parent=node_6, left=None, right=None) #OK
        node_2 = Node(key=2, red=True, parent=node_6, left=None, right=None) #OK
        node_6.left = node_2 #OK
        node_6.right = node_8 #OK
        node_m20 = Node(key=-20, red=False, parent=node_m10, left=None, right=None) #OK
        node_m10.left = node_m20 #OK
        node_m10.right = node_6 #OK

        # RIGHT SUBTREE
        node_20 = Node(key=20, red=True, parent=root) #OK
        node_15 = Node(key=15, red=False, parent=node_20, left=None, right=None) #OK
        node_25 = Node(25, red=False, parent=node_20, left=None, right=None) #OK
        node_20.left = node_15 #OK
        node_20.right = node_25 #OK

        root.left = node_m10 #OK
        root.right = node_20 #OK

        tree.root = root
        tree.insert(4)
        """
                    _____10B_____                                     _____10B_____
               __-10R__        __20R__                           __-10R__        __20R__
            -20B      6B     15B     25B  --FIRST RECOLOR-->  -20B      6R     15B     25B
                    2R  8R                                            2B  8B
               Add-->4R                                                4R



                                  _____10B_____
                             __-10B__        __20B__
   --SECOND RECOLOR-->    -20B      6R     15B     25B
                                  2B  8B
                                   4R
        """
        """ This should trigger two recolors.
            2 and 8 should turn to black,
            6 should turn to red,
            -10 and 20 should turn to black
            10 should try to turn to red, but since it's the root it can't be black"""
        expected_keys = [-20, -10, 2, 4, 6, 8, 10, 15, 20, 25]
        keys = list(tree.keys())
        self.assertEqual(keys, expected_keys)

        self.assertEqual(node_2.red, False)
        self.assertEqual(node_8.red, False)
        self.assertEqual(node_6.red, True)
        self.assertEqual(node_m10.red, False)
        self.assertEqual(node_20.red, False)

    def test_recoloring_two(self):
        rb_tree = Tree()
        root = Node(key=10, red=False, parent=None, left=None, right=None)
        # left subtree
        node_m10 = Node(key=-10, red=True, parent=root, left=None, right=None)
        node_m20 = Node(key=-20, red=False, parent=node_m10, left=None, right=None)
        node_6 = Node(key=6, red=False, parent=node_m10, left=None, right=None)
        node_m10.left = node_m20
        node_m10.right = node_6

        # right subtree
        node_20 = Node(key=20, red=True, parent=root, left=None, right=None)
        node_15 = Node(key=15, red=False, parent=node_20, left=None, right=None)
        node_25 = Node(key=25, red=False, parent=node_20, left=None, right=None)
        node_20.left = node_15
        node_20.right = node_25
        node_12 = Node(key=12, red=True, parent=node_15, left=None, right=None)
        node_17 = Node(key=17, red=True, parent=node_15, left=None, right=None)
        node_15.left = node_12
        node_15.right = node_17

        root.left = node_m10
        root.right = node_20
        rb_tree.root = root
        rb_tree.insert(19)


        """

                 _____10B_____                                        _____10B_____
            __-10R__        __20R__                              __-10R__        __20R__
         -20B      6B     15B     25B     FIRST RECOLOR-->    -20B      6B     15R     25B
                       12R  17R                                             12B  17B
                        Add-->19R                                                 19R


        SECOND RECOLOR


                _____10B_____
           __-10B__        __20B__
        -20B      6B     15R     25B
                      12B  17B
                            19R
        """
        expected_keys = [-20, -10, 6, 10, 12, 15, 17, 19, 20, 25]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_19 = node_17.right
        self.assertEqual(node_19.key, 19)
        self.assertEqual(node_19.red, True)
        self.assertEqual(node_19.parent, node_17)

        self.assertEqual(node_17.red, False)
        self.assertEqual(node_12.red, False)
        self.assertEqual(node_15.red, True)
        self.assertEqual(node_20.red, False)
        self.assertEqual(node_25.red, False)
        self.assertEqual(node_m10.red, False)
        self.assertEqual(rb_tree.root.red, False)

    def test_right_rotation(self):
        tree = Tree()
        root = Node(key=10, red=False, parent=None)

        # LEFT SUBTREE
        node_m10 = Node(key=-10, red=False, parent=root, left=None, right=None)
        node_7 = Node(key=7, red=True, parent=node_m10, left=None, right=None)
        node_m10.right = node_7

        # RIGHT SUBTREE
        node_20 = Node(key=20, red=False, parent=root, left=None, right=None)
        node_15 = Node(key=15, red=True, parent=node_20, left=None, right=None)
        node_20.left = node_15

        root.left = node_m10
        root.right = node_20

        tree.root = root
        tree.insert(13)

        """
                  ____10B____                                           ____10B____
              -10B          20B       --(LL -> R) RIGHT ROTATE-->    -10B         15B
                 7R       15R                                           7R      13R 20R
                 Add -> 13R
        """
        expected_keys = [-10, 7, 10, 13, 15, 20]
        keys = list(tree.keys())
        self.assertEqual(keys, expected_keys)

        node_20 = node_15.right
        node_13 = node_15.left

        self.assertEqual(node_15.red, False)  # this should be the parent of both now
        self.assertEqual(node_15.parent.key, 10)

        self.assertEqual(node_20.key, 20)
        self.assertEqual(node_20.red, True)
        self.assertEqual(node_20.parent.key, 15)
        self.assertEqual(node_20.left, None)
        self.assertEqual(node_20.right, None)

        self.assertEqual(node_13.key, 13)
        self.assertEqual(node_13.red, True)
        self.assertEqual(node_13.parent.key, 15)
        self.assertEqual(node_13.left, None)
        self.assertEqual(node_13.right, None)

    def test_left_rotation_no_sibling(self):
        rb_tree = Tree()
        root = Node(key=10, red=False, parent=None, left=None, right=None)
        # LEFT SUBTREE
        node_7 = Node(key=7, red=False, parent=root, left=None, right=None)
        node_8 = Node(key=8, red=True, parent=node_7, left=None, right=None)
        node_7.right = node_8

        # RIGHT SUBTREE
        rightest = Node(key=20, red=False, parent=root, left=None, right=None)
        root.left = node_7
        root.right = rightest

        rb_tree.root = root
        rb_tree.insert(9)
        """
                 -->     10B                                10B
        ORIGINAL -->  7B    20B  --LEFT ROTATION-->       8B   20B
                 -->    8R                              7R  9R
                 -->     9R
        We add 9, which is the right child of 8 and causes a red-red relationship
        this calls for a left rotation, so 7 becomes left child of 8 and 9 the right child of 8
        8 is black, 7 and 9 are red
        """
        expected_keys = [7, 8, 9, 10, 20]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_9 = node_8.right

        self.assertEqual(node_9.key, 9)
        self.assertEqual(node_9.red, True)
        self.assertEqual(node_9.parent.key, 8)
        self.assertEqual(node_9.left, None)
        self.assertEqual(node_9.right, None)

        self.assertEqual(node_8.parent.key, 10)
        self.assertEqual(node_8.red, False)
        self.assertEqual(node_8.left.key, 7)
        self.assertEqual(node_8.right.key, 9)

        self.assertEqual(node_7.red, True)
        self.assertEqual(node_7.parent.key, 8)
        self.assertEqual(node_7.left, None)
        self.assertEqual(node_7.right, None)

    def test_right_rotation_no_sibling_left_subtree(self):
        rb_tree = Tree()
        root = Node(key=10, red=False, parent=None, left=None, right=None)
        # LEFT SUBTREE
        node_m10 = Node(key=-10, red=False, parent=root, left=None, right=None)
        node_m11 = Node(key=-11, red=True, parent=node_m10, left=None, right=None)
        node_m10.left = node_m11
        # RIGHT SUBTREE
        node_20 = Node(key=20, red=False, parent=root, left=None, right=None)
        node_15 = Node(key=15, red=True, parent=node_20, left=None, right=None)
        node_20.left = node_15

        root.left = node_m10
        root.right = node_20
        rb_tree.root = root
        rb_tree.insert(-12)
        """


                            ____10____                                       ____10____
                       __-10B__     20B  (LL->R) Right rotate-->          -11B        20B
                   -11R          15R                                   -12R  -10R   15R
          Add--> 12R



        red-red relationship with -11 -12, so we do a right rotation where -12 becomes the left child of -11,
                                                                            -10 becomes the right child of -11
        -11's parent is root, -11 is black, -10,-12 are True
        """
        expected_keys = [-12, -11, -10, 10, 15, 20]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_m12 = node_m11.left
        self.assertEqual(rb_tree.root.left.key, -11)

        self.assertEqual(node_m12.key, -12)
        self.assertEqual(node_m12.red, True)
        self.assertEqual(node_m12.parent.key, -11)
        self.assertEqual(node_m12.left, None)
        self.assertEqual(node_m12.right, None)

        self.assertEqual(node_m11.red, False)
        self.assertEqual(node_m11.parent, rb_tree.root)
        self.assertEqual(node_m11.left.key, -12)
        self.assertEqual(node_m11.right.key, -10)

        self.assertEqual(node_m10.red, True)
        self.assertEqual(node_m10.parent.key, -11)
        self.assertEqual(node_m10.left, None)
        self.assertEqual(node_m10.right, None)

    def test_left_right_rotation_no_sibling(self):
        rb_tree = Tree()
        root = Node(key=10, red=False, parent=None, left=None, right=None)
        # LEFT PART
        node_m10 = Node(key=-10, red=False, parent=root, left=None, right=None)
        node_7 = Node(key=7, red=True, parent=node_m10, left=None, right=None)
        node_m10.right = node_7

        # RIGHT PART
        node_20 = Node(key=20, red=False, parent=root, left=None, right=None)
        node_15 = Node(key=15, red=True, parent=node_20, left=None, right=None)
        node_20.left = node_15

        root.left=node_m10
        root.right=node_20

        rb_tree.root = root
        rb_tree.insert(17)
        """
                    ___10___                                                     ____10____
                 -10B      20B                                                -10B        20B
                    7R   15R        --(LR=>RL) Left Rotate (no recolor) -->      7R     17R
                    Add--> 17R                                                         15R



                                                ____10____
        Right Rotate (with recolor) -->      -10B        17B
                                                7R     15R 20R

        15-17 should do a left rotation so 17 is now the parent of 15.
        Then, a right rotation should be done so 17 is the parent of 20(15's prev parent)
        Also, a recoloring should be done such that 17 is now black and his children are red
        """
        expected_keys = [-10, 7, 10, 15, 17, 20]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_15 = node_15
        node_20 = node_20
        node_17 = node_15.parent
        self.assertEqual(rb_tree.root.right, node_17)

        self.assertEqual(node_17.key, 17)
        self.assertEqual(node_17.red, False)
        self.assertEqual(node_17.parent, rb_tree.root)
        self.assertEqual(node_17.left.key, 15)
        self.assertEqual(node_17.right.key, 20)

        self.assertEqual(node_20.parent.key, 17)
        self.assertEqual(node_20.red, True)
        self.assertEqual(node_20.left, None)
        self.assertEqual(node_20.right, None)

        self.assertEqual(node_15.parent.key, 17)
        self.assertEqual(node_15.red, True)
        self.assertEqual(node_15.left, None)
        self.assertEqual(node_15.right, None)

    def test_right_left_rotation_no_sibling(self):
        rb_tree = Tree()
        root = Node(key=10, red=False, parent=None, left=None, right=None)
        # LEFT PART
        nodem10 = Node(key=-10, red=False, parent=root, left=None, right=None)
        node_7 = Node(key=7, red=True, parent=nodem10, left=None, right=None)
        nodem10.right = node_7

        # RIGHT PART
        node_20 = Node(key=20, red=False, parent=root, left=None, right=None)
        node_15 = Node(key=15, red=True, parent=node_20, left=None, right=None)
        node_20.left = node_15

        root.left = nodem10
        root.right = node_20

        rb_tree.root = root
        rb_tree.insert(2)
        """

            ___10___                                                        ___10___
         -10B       20B                                                  -10B       20B
            7R     15R   --- (LR=>RL) Right Rotation (no recolor)-->        2R    15R
    Add--> 2R                                                                7R


                                                 _____10_____
        Left Rotation (with recolor) -->     __2B__       __20B__
                                         -10R     7R    15R


        2 goes as left to 7, but both are red so we do a RIGHT-LEFT rotation
        First a right rotation should happen, so that 2 becomes the parent of 7 [2 right-> 7]
        Second a left rotation should happen, so that 2 becomes the parent of -10 and 7
        2 is black, -10 and 7 are now red. 2's parent is the root - 10
        """
        expected_keys = [-10, 2, 7, 10, 15, 20]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_2 = node_7.parent
        self.assertEqual(node_2.parent.key, 10)
        self.assertEqual(node_2.red, False)
        self.assertEqual(node_2.left.key, -10)
        self.assertEqual(node_2.right.key, 7)

        self.assertEqual(node_7.red, True)
        self.assertEqual(node_7.parent.key, 2)
        self.assertEqual(node_7.left, None)
        self.assertEqual(node_7.right, None)

        self.assertEqual(nodem10.red, True)
        self.assertEqual(nodem10.parent.key, 2)
        self.assertEqual(nodem10.left, None)
        self.assertEqual(nodem10.right, None)

    def test_recolor_lr(self):
        rb_tree = Tree()
        root = Node(key=10, red=False, parent=None)
        # RIGHT SUBTREE
        node_m10 = Node(key=-10, red=True, parent=root, left=None, right=None)
        node_m20 = Node(key=-20, red=False, parent=node_m10, left=None, right=None)
        node_m10.left = node_m20
        node_6 = Node(key=6, red=False, parent=node_m10, left=None, right=None)
        node_m10.right = node_6
        node_1 = Node(key=1, red=True, parent=node_6, left=None, right=None)
        node_6.left = node_1
        node_9 = Node(key=9, red=True, parent=node_6, left=None, right=None)
        node_6.right = node_9

        # LEFT SUBTREE
        node_20 = Node(key=20, red=False, parent=root, left=None, right=None)
        node_15 = Node(key=15, red=True, parent=node_20, left=None, right=None)
        node_20.left = node_15
        node_30 = Node(key=30, red=True, parent=node_20, left=None, right=None)
        node_20.right = node_30

        root.left = node_m10
        root.right = node_20
        rb_tree.root = root
        rb_tree.insert(4)
        """

                _________10B_________                                      _________10B_________
           ___-10R___              __20B__                            ___-10R___              __20B__
        -20B      __6B__         15R     30R  ---RECOLORS TO -->   -20B      __6R__         15R     30R
                1R     9R                                                  1B     9B
                  4R                                                         4R

                                      _________10B_________
                                 ___6R___              __20B__                                   ______6B__
        LEFT ROTATOES TO --> __-10B__    9B         15R      30R   ---RIGHT ROTATES TO-->   __-10R__       _10R_
                          -20B      1B                                                   -20B      1B    9B   __20B__
                                      4R                                                             4R     15R     30R



        Adding 4, we recolor once, then we check upwards and see that there's a black sibling.
        We see that our direction is RightLeft (RL) and do a Left Rotation followed by a Right Rotation
        -10 becomes 6's left child and 1 becomes -10's right child
        """
        expected_keys = [-20, -10, 1, 4, 6, 9, 10, 15, 20, 30]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_10 = rb_tree.root.right
        node_4 = node_1.right

        self.assertEqual(rb_tree.root.key, 6)
        self.assertEqual(rb_tree.root.parent, None)
        self.assertEqual(rb_tree.root.left.key, -10)
        self.assertEqual(rb_tree.root.right.key, 10)

        self.assertEqual(node_m10.parent.key, 6)
        self.assertEqual(node_m10.red, True)
        self.assertEqual(node_m10.left.key, -20)
        self.assertEqual(node_m10.right.key, 1)

        self.assertEqual(node_10.red, True)
        self.assertEqual(node_10.parent.key, 6)
        self.assertEqual(node_10.left.key, 9)
        self.assertEqual(node_10.right.key, 20)

        self.assertEqual(node_m20.red, False)
        self.assertEqual(node_m20.parent.key, -10)
        self.assertEqual(node_m20.left, None)
        self.assertEqual(node_m20.right, None)

        self.assertEqual(node_1.red, False)
        self.assertEqual(node_1.parent.key, -10)
        self.assertEqual(node_1.left, None)
        self.assertEqual(node_1.right.red, True)
        self.assertEqual(node_4.key, 4)
        self.assertEqual(node_4.red, True)

    def test_functional_test_build_tree(self):
        rb_tree = Tree()
        rb_tree.insert(2)
        self.assertEqual(rb_tree.root.key, 2)
        self.assertEqual(rb_tree.root.red, False)
        node_2 = rb_tree.root
        """ 2 """
        expected_keys = [2]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        rb_tree.insert(1)
        """
            2B
           1R
        """
        expected_keys = [1, 2]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_1 = rb_tree.root.left
        self.assertEqual(node_1.key, 1)
        self.assertEqual(node_1.red, True)

        rb_tree.insert(4)
        """
            2B
          1R  4R
        """
        expected_keys = [1, 2, 4]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_4 = rb_tree.root.right
        self.assertEqual(node_4.key, 4)
        self.assertEqual(node_4.red, True)
        self.assertEqual(node_4.left, None)
        self.assertEqual(node_4.right, None)

        rb_tree.insert(5)
        """
            2B                              2B
          1R  4R    ---CAUSES RECOLOR-->  1B  4B
               5R                              5R
        """
        expected_keys = [1, 2, 4, 5]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_5 = node_4.right
        self.assertEqual(node_5.key, 5)
        self.assertEqual(node_4.red, False)
        self.assertEqual(node_1.red, False)
        self.assertEqual(node_5.red, True)

        rb_tree.insert(9)
        """
            2B                                           __2B__
          1B  4B        ---CAUSES LEFT ROTATION-->     1B     5B
                5R                                          4R  9R
                 9R
        """
        expected_keys = [1, 2, 4, 5, 9]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_9 = node_5.right
        self.assertEqual(node_9.key, 9)
        self.assertEqual(node_9.red, True)
        self.assertEqual(node_9.left, None)
        self.assertEqual(node_9.right, None)

        self.assertEqual(node_4.red, True)
        self.assertEqual(node_4.left, None)
        self.assertEqual(node_4.right, None)
        self.assertEqual(node_4.parent.key, 5)

        self.assertEqual(node_5.parent.key, 2)
        self.assertEqual(node_5.red, False)
        self.assertEqual(node_5.left.key, 4)
        self.assertEqual(node_5.right.key, 9)

        rb_tree.insert(3)
        """
            __2B__                                  __2B__
          1B      5B     ---CAUSES RECOLOR-->     1B      5R
                4R  9R                                  4B  9B
               3R                                      3R
        """
        expected_keys = [1, 2, 3, 4, 5, 9]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_3 = node_4.left
        self.assertEqual(node_3.key, 3)
        self.assertEqual(node_3.red, True)
        self.assertEqual(node_3.left, None)
        self.assertEqual(node_3.right, None)
        self.assertEqual(node_3.parent.key, 4)

        self.assertEqual(node_4.red, False)
        self.assertEqual(node_4.right, None)
        self.assertEqual(node_4.parent.key, 5)

        self.assertEqual(node_9.red, False)
        self.assertEqual(node_9.parent.key, 5)

        self.assertEqual(node_5.red, True)
        self.assertEqual(node_5.left.key, 4)
        self.assertEqual(node_5.right.key, 9)

        rb_tree.insert(6)
        """
        Nothing special
           __2B__
         1B      5R___
               4B    _9B
              3R    6R
        """
        expected_keys = [1, 2, 3, 4, 5, 6, 9]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_6 = node_9.left
        self.assertEqual(node_6.key, 6)
        self.assertEqual(node_6.red, True)
        self.assertEqual(node_6.parent.key, 9)
        self.assertEqual(node_6.left, None)
        self.assertEqual(node_6.right, None)

        rb_tree.insert(7)
        """
                   __2B__                                                    __2B__
                 1B      ___5R___             ---LEFT  ROTATION TO-->       1B   ___5R___
                       4B      _9B_                                             4B      9B
                     3R       6R                                               3R      7R
                               7R                                                     6B
            RIGHT ROTATION (RECOLOR) TO
                 __2B__
               1B    ___5R___
                    4B      7B
                   3R     6R  9R
        """
        expected_keys = [1, 2, 3, 4, 5, 6, 7, 9]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_7 = node_5.right
        self.assertEqual(node_7.key, 7)
        self.assertEqual(node_7.red, False)
        self.assertEqual(node_7.left.key, 6)
        self.assertEqual(node_7.right.key, 9)
        self.assertEqual(node_7.parent.key, 5)

        self.assertEqual(node_5.red, True)
        self.assertEqual(node_5.right.key, 7)

        self.assertEqual(node_6.red, True)
        self.assertEqual(node_6.left, None)
        self.assertEqual(node_6.right, None)
        self.assertEqual(node_6.parent.key, 7)

        self.assertEqual(node_9.red, True)
        self.assertEqual(node_9.left, None)
        self.assertEqual(node_9.right, None)
        self.assertEqual(node_9.parent.key, 7)

        rb_tree.insert(15)
        """
                    __2B__                                         __2B__
               1B    ___5R___                                    1B    ___5R___
                    4B      7B       ---RECOLORS TO-->                4B       7R
                   3R     6R  9R                                     3R       6B 9B
                               15R                                                15R
                Red-red relationship on 5R-7R. 7R's sibling is False, so we need to rotate.
                7 is the right child of 5, 5 is the right child of 2, so we have RR => L: Left rotation with recolor
                What we get is:

                            ___5B___
                        __2R__      7R
                      1B     4B    6B 9B
                            3R         15R
        """
        expected_keys = [1, 2, 3, 4, 5, 6, 7, 9, 15]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_15 = node_9.right
        self.assertEqual(node_15.red, True)
        self.assertEqual(node_15.parent.key, 9)
        self.assertEqual(node_15.left, None)
        self.assertEqual(node_15.right, None)

        self.assertEqual(node_9.red, False)
        self.assertEqual(node_9.left, None)
        self.assertEqual(node_9.right.key, 15)
        self.assertEqual(node_9.parent.key, 7)

        self.assertEqual(node_6.red, False)

        self.assertEqual(node_7.red, True)
        self.assertEqual(node_7.left.key, 6)
        self.assertEqual(node_7.right.key, 9)

        self.assertEqual(rb_tree.root.key, 5)
        self.assertIsNone(node_5.parent)
        self.assertEqual(node_5.right.key, 7)
        self.assertEqual(node_5.left.key, 2)

        self.assertEqual(node_2.red, True)
        self.assertEqual(node_2.parent.key, 5)
        self.assertEqual(node_2.left.key, 1)
        self.assertEqual(node_2.right.key, 4)

        self.assertEqual(node_4.parent.key, 2)
        self.assertEqual(node_4.red, False)
        self.assertEqual(node_4.left.key, 3)
        self.assertEqual(node_4.right, None)

    def test_right_left_rotation_after_recolor(self):
        rb_tree = Tree()
        root = Node(key=10, red=False, parent=None, left=None, right=None)
        node_10 = root

        # left subtree
        node_5 = Node(key=5, red=False, parent=root, left=None, right=None)

        # right subtree
        node_20 = Node(key=20, red=True, parent=root, left=None, right=None)
        node_15 = Node(key=15, red=False, parent=node_20, left=None, right=None)
        node_25 = Node(key=25, red=False, parent=node_20, left=None, right=None)
        node_20.left = node_15
        node_20.right = node_25

        node_12 = Node(key=12, red=True, parent=node_15, left=None, right=None)
        node_17 = Node(key=17, red=True, parent=node_15, left=None, right=None)
        node_15.left = node_12
        node_15.right = node_17

        root.left = node_5
        root.right = node_20
        rb_tree.root = root
        rb_tree.insert(19)

        """
                    ____10B____                           ____10B____
                   5B      __20R__                       5B      __20R__
                      __15B__   25B   --RECOLORS TO-->      __15R__   25B
                   12R      17R                          12B      17B
                       Add-->19R                                   19R


                                  ____10B____
    LR=>RL: Right rotation to   5B          ___15R___
                                         12B      __20R__
                                                17B      25B
                                                  19R


                                     ______15B_____
       Left rotation to           10R           __20R__
                                5B  12B     __17B__    25B
                                                  19R
        """
        expected_keys = [5, 10, 12, 15, 17, 19, 20, 25]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_19 = node_17.right

        self.assertEqual(node_19.key, 19)
        self.assertEqual(node_19.red, True)
        self.assertEqual(node_19.left, None)
        self.assertEqual(node_19.right, None)
        self.assertEqual(node_19.parent, node_17)

        self.assertEqual(node_17.parent, node_20)
        self.assertEqual(node_17.red, False)
        self.assertEqual(node_17.left, None)
        self.assertEqual(node_17.right, node_19)

        self.assertEqual(node_20.parent, node_15)
        self.assertEqual(node_20.red, True)
        self.assertEqual(node_20.left, node_17)
        self.assertEqual(node_20.right, node_25)

        self.assertEqual(rb_tree.root, node_15)
        self.assertIsNone(node_15.parent)
        self.assertEqual(node_15.left, node_10)
        self.assertEqual(node_15.right, node_20)
        self.assertEqual(node_15.red, False)

        self.assertEqual(node_10.parent, node_15)
        self.assertEqual(node_10.red, True)
        self.assertEqual(node_10.right, node_12)
        self.assertEqual(node_10.left, node_5)

        self.assertEqual(node_12.red, False)
        self.assertEqual(node_12.parent, node_10)
        self.assertEqual(node_12.left, None)
        self.assertEqual(node_12.right, None)

    def test_right_rotation_after_recolor(self):
        rb_tree = Tree()
        root = Node(key=10, red=False, parent=None, left=None, right=None)
        node_10 = root
        # left subtree
        node_m10 = Node(key=-10, red=True, parent=root, left=None, right=None)
        node_6 = Node(key=6, red=False, parent=node_m10, left=None, right=None)
        node_m20 = Node(key=-20, red=False, parent=node_m10, left=None, right=None)
        node_m10.left = node_m20
        node_m10.right = node_6
        node_m21 = Node(key=-21, red=True, parent=node_m20, left=None, right=None)
        node_m19 = Node(key=-19, red=True, parent=node_m20, left=None, right=None)
        node_m20.left = node_m21
        node_m20.right = node_m19
        # right subtree
        node_20 = Node(key=20, red=False, parent=root, left=None, right=None)
        node_15 = Node(key=15, red=True, parent=node_20, left=None, right=None)
        node_25 = Node(key=25, red=True, parent=node_20, left=None, right=None)
        node_20.left = node_15
        node_20.right = node_25

        root.left = node_m10
        root.right = node_20
        rb_tree.root = root
        rb_tree.insert(-22)

        """

                    _____10_____                                               _____10_____
                   /            \                                             /            \
                -10R           20B                                         -10R           20B
               /    \          /   \                                      /   \          /    \
            -20B    6B       15R  25R     --RECOLOR TO-->              -20R    6B       15R  25R
            /   \                                                       /  \
          -21R -19R                                                   -21B -19B
           /                                                         /
 Add-> -22R                                                        22R



                                        ____-10B_____
                                       /             \
                                     -20R          __10R__
                                     /   \        /       \
        Right rotation to->       -21B  -19B     6B    __20B__
                                   /                  /       \
                                -22R                 15R     25R

        """
        expected_keys = [-22, -21, -20, -19, -10, 6, 10, 15, 20, 25]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        self.assertEqual(rb_tree.root, node_m10)
        self.assertEqual(node_m10.parent, None)
        self.assertEqual(node_m10.left, node_m20)
        self.assertEqual(node_m10.right, node_10)
        self.assertEqual(node_m10.red, False)

        self.assertEqual(node_10.parent, node_m10)
        self.assertEqual(node_10.red, True)
        self.assertEqual(node_10.left, node_6)
        self.assertEqual(node_10.right, node_20)

        self.assertEqual(node_m20.parent, node_m10)
        self.assertEqual(node_m20.red, True)
        self.assertEqual(node_m20.left, node_m21)
        self.assertEqual(node_m20.right, node_m19)

        self.assertEqual(node_m21.red, False)
        self.assertEqual(node_m21.left.key, -22)

        self.assertEqual(node_6.parent, node_10)
        self.assertEqual(node_6.red, False)
        self.assertEqual(node_6.left, None)
        self.assertEqual(node_6.right, None)

        self.assertEqual(node_m19.red, False)
        self.assertEqual(node_m19.parent, node_m20)
        self.assertEqual(node_m19.left, None)
        self.assertEqual(node_m19.right, None)

    # ***************TEST INSERTIONS***************

    # ***************TEST DELETIONS***************

    def test_deletion_root(self):
        rb_tree = Tree()
        root = Node(key=5, red=False, parent=None, left=None, right=None)
        left_child = Node(key=3, red=True, parent=root, left=None, right=None)
        right_child = Node(key=8, red=True, parent=root, left=None, right=None)
        root.left = left_child
        root.right = right_child
        """
      REMOVE--> __5__                     __8B__
               /     \     --Result-->   /
             3R      8R                3R
        """
        rb_tree.root = root
        del rb_tree[5]

        expected_keys = [3, 8]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_8 = rb_tree.root
        self.assertEqual(node_8.key, 8)
        self.assertEqual(node_8.red, False)
        self.assertEqual(node_8.parent, None)
        self.assertEqual(node_8.left.key, 3)
        self.assertEqual(node_8.right, None)
        node_3 = node_8.left
        self.assertEqual(node_3.red, True)
        self.assertEqual(node_3.parent, node_8)
        self.assertEqual(node_3.left, None)
        self.assertEqual(node_3.right, None)

    def test_deletion_root_2_nodes(self):
        rb_tree = Tree()
        root = Node(key=5, red=False, parent=None, left=None, right=None)
        right_child = Node(key=8, red=True, parent=root, left=None, right=None)
        root.right = right_child
        rb_tree.root = root
        del rb_tree[5]
        """
                __5B__ <-- REMOVE        __8B__
                     \      Should become--^
                     8R
        """
        expected_keys = [8]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        root = rb_tree.root
        self.assertEqual(root.key, 8)
        self.assertEqual(root.parent, None)
        self.assertEqual(root.red, False)
        self.assertEqual(root.left, None)
        self.assertEqual(root.right, None)

    def test_delete_single_child(self):
        rb_tree = Tree()
        root = Node(key=5, red=False, parent=None, left=None, right=None)
        left_child = Node(key=1, red=True, parent=root, left=None, right=None)
        right_child = Node(key=6, red=True, parent=root, left=None, right=None)
        root.left = left_child
        root.right = right_child
        rb_tree.root = root
        del rb_tree[6]
        """
           5                        5B
          / \   should become      /
        1R   6R                   1R
        """
        expected_keys = [1, 5]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        self.assertEqual(root.right, None)
        self.assertEqual(root.key, 5)
        self.assertEqual(root.red, False)
        self.assertEqual(root.parent, None)
        self.assertEqual(root.left.key, 1)
        node_1 = root.left
        self.assertEqual(node_1.left, None)
        self.assertEqual(node_1.right, None)

    def test_delete_single_deep_child(self):
        rb_tree = Tree()
        root = Node(key=20, red=False, parent=None, left=None, right=None)
        # left subtree
        node_10 = Node(key=10, red=False, parent=None, left=None, right=None)
        node_5 = Node(key=5, red=True, parent=node_10, left=None, right=None)
        node_15 = Node(key=15, red=True, parent=node_10, left=None, right=None)
        node_10.left = node_5
        node_10.right = node_15
        # right subtree
        node_38 = Node(key=38, red=True, parent=root, left=None, right=None)
        node_28 = Node(key=28, red=False, parent=node_38, left=None, right=None)
        node_48 = Node(key=48, red=False, parent=node_38, left=None, right=None)
        node_38.left = node_28
        node_38.right = node_48
        # node_28 subtree
        node_23 = Node(key=23, red=True, parent=node_28, left=None, right=None)
        node_29 = Node(key=29, red=True, parent=node_28, left=None, right=None)
        node_28.left = node_23
        node_28.right = node_29
        # node 48 subtree
        node_41 = Node(key=41, red=True, parent=node_48, left=None, right=None)
        node_49 = Node(key=49, red=True, parent=node_48, left=None, right=None)
        node_48.left = node_41
        node_48.right = node_49

        root.left = node_10
        root.right = node_38
        rb_tree.root = root
        del rb_tree[49]
        """
                ______20______
               /              \
             10B           ___38R___
            /   \         /         \
          5R    15R      28B         48B
                        /  \        /   \
                      23R  29R     41R   49R    <--- REMOVE
        """
        expected_keys = [5, 10, 15, 20, 23, 28, 29, 38, 41, 48]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        self.assertEqual(node_48.right, None)
        self.assertEqual(node_48.red, False)
        self.assertEqual(node_48.left.key, 41)
        with self.assertRaises(KeyError):
            rb_tree[49]

    def test_deletion_red_node_red_successor_no_children(self):
        """
        This must be the easiest deletion yet!
        """
        rb_tree = Tree()
        root = Node(key=10, red=False, parent=None, left=None, right=None)
        # Left subtree
        node_5 = Node(key=5, red=True, parent=root, left=None, right=None)
        node_m5 = Node(key=-5, red=False, parent=root, left=None, right=None)
        node_7 = Node(key=7, red=False, parent=node_5, left=None, right=None)
        node_5.left = node_m5
        node_5.right = node_7

        # right subtree
        node_35 = Node(key=35, red=True, parent=root, left=None, right=None)
        node_20 = Node(key=20, red=False, parent=node_35, left=None, right=None)
        node_38 = Node(key=38, red=False, parent=node_35, left=None, right=None)
        node_35.left = node_20
        node_35.right = node_38
        node_36 = Node(key=36, red=True, parent=node_38, left=None, right=None)
        node_38.left = node_36

        root.left = node_5
        root.right = node_35
        rb_tree.root = root
        del rb_tree[35]

        """
                    10B
                  /     \
                5R       35R   <-- REMOVE THIS
               /  \     /   \
            -5B   7B   20B  38B   We get it's in-order successor, which is 36
                           /
                          36R     36 Is red and has no children, so we easily swap it's key with 35 and remove 36

                      10B
                    /     \
     RESULT IS    5R       36R
                 /  \     /   \
              -5B   7B   20B  38B
        """
        expected_keys = [-5, 5, 7, 10, 20, 36, 38]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        # Careful with reference equals
        node_36 = rb_tree.root.right
        self.assertEqual(node_36.key, 36)
        self.assertEqual(node_36.red, True)
        self.assertEqual(node_36.parent, rb_tree.root)
        self.assertEqual(node_36.left.key, 20)
        self.assertEqual(node_36.right.key, 38)

        self.assertEqual(node_20.parent.key, 36)
        self.assertEqual(node_38.parent.key, 36)
        self.assertEqual(node_38.left, None)

    def test_mirror_deletion_red_node_red_successor_no_children(self):
        """
        This must be the easiest deletion yet!
        """
        rb_tree = Tree()
        root = Node(key=10, red=False, parent=None, left=None, right=None)
        # Left subtree
        node_5 = Node(key=5, red=True, parent=root, left=None, right=None)
        node_m5 = Node(key=-5, red=False, parent=root, left=None, right=None)
        node_7 = Node(key=7, red=False, parent=node_5, left=None, right=None)
        node_5.left = node_m5
        node_5.right = node_7
        node_6 = Node(key=6, red=True, parent=node_7, left=None, right=None)
        node_7.left = node_6

        # right subtree
        node_35 = Node(key=35, red=True, parent=root, left=None, right=None)
        node_20 = Node(key=20, red=False, parent=node_35, left=None, right=None)
        node_38 = Node(key=38, red=False, parent=node_35, left=None, right=None)
        node_35.left = node_20
        node_35.right = node_38
        node_36 = Node(key=36, red=True, parent=node_38, left=None, right=None)
        node_38.left = node_36

        root.left = node_5
        root.right = node_35
        rb_tree.root = root
        del rb_tree[5]

        """
                    10B
                  /     \
    REMOVE -->  5R       35R
               /  \     /   \
            -5B   7B   20B  38B   We get it's in-order successor, which is 6
                 /         /
               6R         36R      6 Is red and has no children,
                                    so we easily swap it's key with 5 and remove 6

                      10B
                    /     \
     RESULT IS    6R       35R
                 /  \     /   \
              -5B   7B   20B  38B
                             /
                            36R
        """
        expected_keys = [-5, 6, 7, 10, 20, 35, 36, 38]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_6 = rb_tree.root.left
        self.assertEqual(node_6.key, 6)
        self.assertEqual(node_6.red, True)
        self.assertEqual(node_6.parent, rb_tree.root)
        self.assertEqual(node_6.left.key, -5)
        self.assertEqual(node_6.right.key, 7)
        node_7 = node_6.right
        self.assertEqual(node_7.red, False)
        self.assertEqual(node_7.parent, node_6)
        self.assertEqual(node_7.left, None)
        self.assertEqual(node_7.right, None)

    def test_deletion_black_node_black_successor_right_red_child(self):
        rb_tree = Tree()
        root = Node(key=10, red=False, parent=None, left=None, right=None)
        # left subtree
        node_5 = Node(key=5, red=False, parent=root, left=None, right=None)
        node_m5 = Node(key=-5, red=False, parent=node_5, left=None, right=None)
        node_7 = Node(key=7, red=False, parent=node_5, left=None, right=None)
        node_5.left = node_m5
        node_5.right = node_7
        # right subtree
        node_30 = Node(key=30, red=False, parent=root, left=None, right=None)
        node_20 = Node(key=20, red=False, parent=node_30, left=None, right=None)
        node_38 = Node(key=38, red=True, parent=node_30, left=None, right=None)
        node_30.left = node_20
        node_30.right = node_38
        # 38 subtree
        node_32 = Node(key=32, red=False, parent=node_38, left=None, right=None)
        node_41 = Node(key=41, red=False, parent=node_38, left=None, right=None)
        node_38.left = node_32
        node_38.right = node_41
        node_35 = Node(key=35, red=True, parent=node_32, left=None, right=None)
        node_32.right = node_35

        root.left = node_5
        root.right = node_30

        rb_tree.root = root
        del rb_tree[30]
        """
                         ___10B___                                             ___10B___
                        /         \                                           /         \
                       5B         30B  <------- REMOVE THIS                  5B         32B  <----
                      /  \       /   \                                      /  \       /   \
                    -5B  7B    20B   38R                                  -5B  7B    20B   38R
                                    /   \                                                 /   \
                   successor ---> 32B    41B                                       -->  35B    41B
                                     \             30B becomes 32B
                                     35R           old 32B becomes 35B
        """
        expected_keys = [-5, 5, 7, 10, 20, 32, 35, 38, 41]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_32 = node_30
        self.assertEqual(node_32.key, 32)
        self.assertEqual(node_32.parent.key, 10)
        self.assertEqual(node_32.red, False)
        self.assertEqual(node_32.left, node_20)
        self.assertEqual(node_32.right, node_38)

        node_35 = node_38.left
        self.assertEqual(node_35.key, 35)
        self.assertEqual(node_35.parent.key, 38)
        self.assertEqual(node_35.red, False)
        self.assertEqual(node_35.left, None)
        self.assertEqual(node_35.right, None)

    def test_deletion_black_node_black_successor_no_child_case_4(self):
        rb_tree = Tree()
        root = Node(key=10, red=False, parent=None, left=None, right=None)
        # left subtree
        node_m10 = Node(key=-10, red=False, parent=root, left=None, right=None)
        # right subtree
        node_30 = Node(key=30, red=True, parent=root, left=None, right=None)
        node_20 = Node(key=20, red=False, parent=node_30, left=None, right=None)
        node_38 = Node(key=38, red=False, parent=node_30, left=None, right=None)
        node_30.left = node_20
        node_30.right = node_38

        root.left = node_m10
        root.right = node_30
        rb_tree.root = root
        del rb_tree[10]

        """
                  ___10B___   <----- REMOVE THIS       ___20B___
                 /         \                          /         \
               -10B        30R                      -10B        30R
                          /   \                                /   \
         successor --> 20B    38B                double black DB  38B
                                                Case 4 applies, since the sibling is black, has no red children and
                                                the parent is True
                                                So, we simply exchange colors of the parent and the sibling


                       ___20B___
                      /         \
                    -10B        30B        DONE
                                   \
                                  38R

        """
        expected_keys = [-10, 20, 30, 38]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        self.assertEqual(rb_tree.root.key, 20)
        self.assertEqual(rb_tree.root.red, False)
        node_30 = rb_tree.root.right
        self.assertEqual(node_30.parent.key, 20)
        self.assertEqual(node_30.key, 30)
        self.assertEqual(node_30.red, False)
        self.assertEqual(node_30.left, None)
        self.assertEqual(node_30.right.key, 38)
        node_38 = node_30.right
        self.assertEqual(node_38.key, 38)
        self.assertEqual(node_38.red, True)
        self.assertEqual(node_38.left, None)
        self.assertEqual(node_38.right, None)

    def test_deletion_black_node_no_successor_case_6(self):
        rb_tree = Tree()
        root = Node(key=10, red=False, parent=None, left=None, right=None)
        # left subtree
        node_m10 = Node(key=-10, red=False, parent=root, left=None, right=None)
        # right subtree
        node_30 = Node(key=30, red=False, parent=root, left=None, right=None)
        node_25 = Node(key=25, red=True, parent=node_30, left=None, right=None)
        node_40 = Node(key=40, red=True, parent=node_30, left=None, right=None)
        node_30.left = node_25
        node_30.right = node_40

        root.left = node_m10
        root.right = node_30
        rb_tree.root = root
        del rb_tree[-10]

        """
                        ___10B___
                       /         \           Case 6 applies here, since
         REMOVE-->  -10B         30B         The parent's color does not matter
         Double Black           /   \        The sibling's color is False
                              25R    40R     The sibling's right child is True (in the MIRROR CASE - left child should be True)
        Here we do a left rotation and change the colors such that
            the sibling gets the parent's color (30 gets 10's color)
            the parent(now sibling's left) and sibling's right become False


                 ___30B___
                /         \
              10B         40B
            /    \
         NULL    25R
        -10B
        would be here
        but we're removing it
        """
        self.assertEqual(rb_tree.root.red, False)
        self.assertEqual(rb_tree.root.key, 30)
        node_10 = rb_tree.root.left
        self.assertEqual(node_10.key, 10)
        self.assertEqual(node_10.red, False)
        self.assertEqual(node_10.parent, rb_tree.root)
        self.assertEqual(node_10.left, None)
        node_25 = node_10.right
        self.assertEqual(node_25.key, 25)
        self.assertEqual(node_25.red, True)
        self.assertEqual(node_25.parent, node_10)
        self.assertEqual(node_25.left, None)
        self.assertEqual(node_25.right, None)
        node_40 = rb_tree.root.right
        self.assertEqual(node_40.key, 40)
        self.assertEqual(node_40.parent, rb_tree.root)
        self.assertEqual(node_40.red, False)
        self.assertEqual(node_40.left, None)
        self.assertEqual(node_40.right, None)

    def test_mirror_deletion_black_node_no_successor_case_6(self):
        rb_tree = Tree()
        root = Node(key=10, red=False, parent=None, left=None, right=None)
        node_12 = Node(key=12, red=False, parent=root, left=None, right=None)
        node_5 = Node(key=5, red=False, parent=root, left=None, right=None)
        node_1 = Node(key=1, red=True, parent=node_5, left=None, right=None)
        node_7 = Node(key=7, red=True, parent=node_5, left=None, right=None)
        node_5.left = node_1
        node_5.right = node_7
        root.left = node_5
        root.right = node_12
        rb_tree.root = root
        del rb_tree[12]
        """
                   __10B__                                           __5B__
                   /      \                                         /      \
                 5B       12B  <--- REMOVE                        1B        10B
                /  \              has no successors                        /
              1R   7R                                                    7R
                            case 6 applies, so we left rotate at 5b
        """
        node_5 = rb_tree.root
        self.assertEqual(node_5.key, 5)
        self.assertEqual(node_5.red, False)
        self.assertEqual(node_5.parent, None)
        self.assertEqual(node_5.left.key, 1)
        self.assertEqual(node_5.right.key, 10)
        node_1 = node_5.left
        self.assertEqual(node_1.key, 1)
        self.assertEqual(node_1.parent, node_5)
        self.assertEqual(node_1.red, False)
        self.assertEqual(node_1.left, None)
        self.assertEqual(node_1.right, None)
        node_10 = node_5.right
        self.assertEqual(node_10.key, 10)
        self.assertEqual(node_10.parent, node_5)
        self.assertEqual(node_10.red, False)
        self.assertEqual(node_10.left.key, 7)
        self.assertEqual(node_10.right, None)
        node_7 = node_10.left
        self.assertEqual(node_7.key, 7)
        self.assertEqual(node_7.parent, node_10)
        self.assertEqual(node_7.red, True)
        self.assertEqual(node_7.left, None)
        self.assertEqual(node_7.right, None)

    def test_deletion_black_node_no_successor_case_3_then_1(self):
        """
        Delete a node such that case 3 is called, which pushes
        the double black node upwards into a case 1 problem
        """
        rb_tree = Tree()
        root = Node(key=10, red=False, parent=None, left=None, right=None)
        # left subtree
        node_m10 = Node(key=-10, red=False, parent=root, left=None, right=None)
        # right subtree
        node_30 = Node(key=30, red=False, parent=root, left=None, right=None)

        root.left = node_m10
        root.right = node_30
        rb_tree.root = root
        del rb_tree[-10]

        """                                             Double
                                                        Black
                    ___10B___                         __|10B|__
                   /         \     ---->             /         \
    REMOVE-->   -10B         30B                  REMOVED      30R  <--- COLOTrue True

            We color the sibling red and try to resolve the double black problem in the root.
            We go through the cases 1-6 and find that case 1 is what we're looking for
            Case 1 simply recolors the root to black and we are done
                ___10B___
                         \
                         30R
        """
        node_10 = rb_tree.root
        self.assertEqual(node_10.red, False)
        self.assertEqual(node_10.parent, None)
        self.assertEqual(node_10.left, None)
        self.assertEqual(node_10.right.key, 30)
        node_30 = node_10.right
        self.assertEqual(node_30.key, 30)
        self.assertEqual(node_30.red, True)
        self.assertEqual(node_30.parent, node_10)
        self.assertEqual(node_30.left, None)
        self.assertEqual(node_30.right, None)

    def test_deletion_black_node_no_successor_case_3_then_5_then_6(self):
        """
        We're going to delete a black node which will cause a case 3 deletion
        which in turn would pass the double black node up into a case 5, which
        will restructure the tree in such a way that a case 6 rotation becomes possible
        """
        rb_tree = Tree()
        root = Node(key=10, red=False, parent=None, left=None, right=None)
        # left subtree
        node_m30 = Node(key=-30, red=False, parent=root, left=None, right=None)
        node_m40 = Node(key=-40, red=False, parent=node_m30, left=None, right=None)
        node_m20 = Node(key=-20, red=False, parent=node_m30, left=None, right=None)
        node_m30.left = node_m40
        node_m30.right = node_m20
        # right subtree
        node_50 = Node(key=50, red=False, parent=root, left=None, right=None)
        node_30 = Node(key=30, red=True, parent=node_50, left=None, right=None)
        node_70 = Node(key=70, red=False, parent=node_50, left=None, right=None)
        node_50.left = node_30
        node_50.right = node_70
        node_15 = Node(key=15, red=False, parent=node_30, left=None, right=None)
        node_40 = Node(key=40, red=False, parent=node_30, left=None, right=None)
        node_30.left = node_15
        node_30.right = node_40

        root.left = node_m30
        root.right = node_50
        rb_tree.root = root
        del rb_tree[-40]
        """
        In mirror cases, this'd be mirrored
        |node| - double black node
                    ___10B___                                 ___10B___
                   /         \               DOUBLE          /         \
                -30B         50B             False-->   |-30B|        50B
               /    \       /   \                        /    \       /   \
  REMOVE-->|-40B|  -20B   30R   70B     --CASE 3--> REMOVED  -20R   30R   70B
                         /   \                                     /   \
                       15B   40B                                 15B   40B



      --CASE 5-->                              ___10B___
      parent is black        still double     /         \
      sibling is black         black -->  |-30B|        30B
      sibling.left is red                     \        /   \
      sibling.right is black                  -20R   15B   50R
      left rotation on sibling.left                       /   \
                                                        40B   70B


      What we've done here is we've simply
      restructured the tree to be eligible
      for a case 6 solution :)                              ___30B___
      --CASE 6-->                                          /         \
      parent color DOESNT MATTER                         10B         50B
      sibling is black                                  /   \       /   \
      sibling.left DOESNT MATTER                     -30B   15B   40B   70B
      sibling.right is True                              \
      left rotation on sibling (30B on the above)       -20R
      where the sibling gets the color of the parent
          and the parent is now to the left of sibling and
          repainted False
          the sibling's right also gets repainted black
        """
        node_30 = rb_tree.root
        self.assertEqual(node_30.key, 30)
        self.assertEqual(node_30.parent, None)
        self.assertEqual(node_30.red, False)
        self.assertEqual(node_30.left.key, 10)
        self.assertEqual(node_30.right.key, 50)

        # test left subtree
        node_10 = node_30.left
        self.assertEqual(node_10.key, 10)
        self.assertEqual(node_10.red, False)
        self.assertEqual(node_10.parent, node_30)
        self.assertEqual(node_10.left.key, -30)
        self.assertEqual(node_10.right.key, 15)
        node_m30 = node_10.left
        self.assertEqual(node_m30.key, -30)
        self.assertEqual(node_m30.red, False)
        self.assertEqual(node_m30.parent, node_10)
        self.assertEqual(node_m30.left, None)
        self.assertEqual(node_m30.right.key, -20)
        node_15 = node_10.right
        self.assertEqual(node_15.key, 15)
        self.assertEqual(node_15.red, False)
        self.assertEqual(node_15.parent, node_10)
        self.assertEqual(node_15.left, None)
        self.assertEqual(node_15.right, None)
        node_m20 = node_m30.right
        self.assertEqual(node_m20.key, -20)
        self.assertEqual(node_m20.red, True)
        self.assertEqual(node_m20.parent, node_m30)
        self.assertEqual(node_m20.left, None)
        self.assertEqual(node_m20.right, None)

        # test right subtree
        node_50 = node_30.right
        self.assertEqual(node_50.key, 50)
        self.assertEqual(node_50.red, False)
        self.assertEqual(node_50.parent, node_30)
        self.assertEqual(node_50.left.key, 40)
        self.assertEqual(node_50.right.key, 70)
        node_40 = node_50.left
        self.assertEqual(node_40.key, 40)
        self.assertEqual(node_40.parent, node_50)
        self.assertEqual(node_40.red, False)
        self.assertEqual(node_40.left, None)
        self.assertEqual(node_40.right, None)
        node_70 = node_50.right
        self.assertEqual(node_70.key, 70)
        self.assertEqual(node_70.red, False)
        self.assertEqual(node_70.parent, node_50)
        self.assertEqual(node_70.left, None)
        self.assertEqual(node_70.right, None)

    def test_mirror_deletion_black_node_no_successor_case_3_then_5_then_6(self):
        """
        We're going to delete a black node which will cause a case 3 deletion
        which in turn would pass the double black node up into a case 5, which
        will restructure the tree in such a way that a case 6 rotation becomes possible
        """
        rb_tree = Tree()
        root = Node(key=50, red=False, parent=None, left=None, right=None)
        # left subtree
        node_30 = Node(key=30, red=False, parent=root, left=None, right=None)
        node_20 = Node(key=20, red=False, parent=node_30, left=None, right=None)
        node_35 = Node(key=35, red=True, parent=node_30, left=None, right=None)
        node_30.left = node_20
        node_30.right = node_35
        node_34 = Node(key=34, red=False, parent=node_35, left=None, right=None)
        node_37 = Node(key=37, red=False, parent=node_35, left=None, right=None)
        node_35.left = node_34
        node_35.right = node_37
        # right subtree
        node_80 = Node(key=80, red=False, parent=root, left=None, right=None)
        node_70 = Node(key=70, red=False, parent=node_80, left=None, right=None)
        node_90 = Node(key=90, red=False, parent=node_80, left=None, right=None)
        node_80.left = node_70
        node_80.right = node_90

        root.left = node_30
        root.right = node_80
        rb_tree.root = root
        del rb_tree[90]

        """
                            Parent is black
               ___50B___    Sibling is black                       ___50B___
              /         \   Sibling's children are black          /         \
           30B          80B        CASE 3                       30B        |80B|
          /   \        /   \        ==>                        /  \        /   \
        20B   35R    70B    90B <---REMOVE                   20B  35R     70R   X
              /  \                                               /   \
            34B   37B                                          34B   37B



    Case 5
    Parent is black                                 __50B__
    Sibling is black             CASE 5            /       \
    Closer sibling child is True  =====>          35B      |80B|
        (right in this case,                    /   \      /
         left in mirror)                     30R   37B    70R
    Outer sibling child is blck             /  \
                                         20B  34B


    We have now successfully position our tree
    for a CASE 6 scenario
    The parent's color does not matter                           __35B__
    The sibling is black                                        /       \
    The closer sibling child             CASE 6               30R       50R
        's color does not matter         ====>               /   \     /   \
    The outer sibling child                                20B   34B 37B    80B
        (left in this case,                                                 /
         right in mirror)                                                  70R
         is True!
        """
        expected_keys = [20, 30, 34, 35, 37, 50, 70, 80]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_35 = rb_tree.root
        self.assertEqual(node_35.key, 35)
        self.assertEqual(node_35.parent, None)
        self.assertEqual(node_35.red, False)
        self.assertEqual(node_35.left.key, 30)
        self.assertEqual(node_35.right.key, 50)
        # right subtree
        node_50 = node_35.right
        self.assertEqual(node_50.key, 50)
        self.assertEqual(node_50.red, False)
        self.assertEqual(node_50.parent, node_35)
        self.assertEqual(node_50.left.key, 37)
        self.assertEqual(node_50.right.key, 80)
        node_37 = node_50.left
        self.assertEqual(node_37.key, 37)
        self.assertEqual(node_37.red, False)
        self.assertEqual(node_37.parent, node_50)
        self.assertEqual(node_37.left, None)
        self.assertEqual(node_37.right, None)
        node_80 = node_50.right
        self.assertEqual(node_80.key, 80)
        self.assertEqual(node_80.red, False)
        self.assertEqual(node_80.parent, node_50)
        self.assertEqual(node_80.left.key, 70)
        self.assertEqual(node_80.right, None)
        node_70 = node_80.left
        self.assertEqual(node_70.key, 70)
        self.assertEqual(node_70.red, True)
        self.assertEqual(node_70.parent, node_80)
        self.assertEqual(node_70.left, None)
        self.assertEqual(node_70.right, None)
        # left subtree
        node_30 = node_35.left
        self.assertEqual(node_30.key, 30)
        self.assertEqual(node_30.parent, node_35)
        self.assertEqual(node_30.red, False)
        self.assertEqual(node_30.left.key, 20)
        self.assertEqual(node_30.right.key, 34)
        node_20 = node_30.left
        self.assertEqual(node_20.key, 20)
        self.assertEqual(node_20.red, False)
        self.assertEqual(node_20.parent, node_30)
        self.assertEqual(node_20.left, None)
        self.assertEqual(node_20.right, None)
        node_34 = node_30.right
        self.assertEqual(node_34.key, 34)
        self.assertEqual(node_34.red, False)
        self.assertEqual(node_34.parent, node_30)
        self.assertEqual(node_34.left, None)
        self.assertEqual(node_34.right, None)

    def test_deletion_black_node_successor_case_2_then_4(self):
        rb_tree = Tree()
        root = Node(key=10, red=False, parent=None, left=None, right=None)
        # left subtree
        node_m10 = Node(key=-10, red=False, parent=root, left=None, right=None)
        node_m20 = Node(key=-20, red=False, parent=node_m10, left=None, right=None)
        node_m5 = Node(key=-5, red=False, parent=node_m10, left=None, right=None)
        node_m10.left = node_m20
        node_m10.right = node_m5
        # right subtree
        node_40 = Node(key=40, red=False, parent=root, left=None, right=None)
        node_20 = Node(key=20, red=False, parent=node_40, left=None, right=None)
        node_60 = Node(key=60, red=True, parent=node_40, left=None, right=None)
        node_40.left = node_20
        node_40.right = node_60
        node_50 = Node(key=50, red=False, parent=node_60, left=None, right=None)
        node_80 = Node(key=80, red=False, parent=node_60, left=None, right=None)
        node_60.left = node_50
        node_60.right = node_80

        root.left = node_m10
        root.right = node_40
        rb_tree.root = root
        del rb_tree[10]
        """

  REMOVE--->    ___10B___           parent is black             ___20B___
               /         \          sibling is red            /         \
            -10B         40B        s.children aren't red    -10B         60B
           /    \       /   \       --CASE 2 ROTATE-->      /    \       /   \
        -20B    -5B |20B|   60R       LEFT ROTATE         -20B  -5B    40R   80B
    SUCCESSOR IS 20----^   /   \      SIBLING 60                      /   \
                         50B    80B                       REMOVE--> 20    50B


    CASE 4                                         ___20B___
    20'S parent is True                           /         \
    sibling is False                            -10B         60B
    sibling's children are NOT True             /    \       /   \
        so we push parent's                  -20B  -5B    40B   80B
        redness down to the sibling                      /   \
        and remove node                      REMOVED--> X    50R
        """
        expected_keys = [-20, -10, -5, 20, 40, 50, 60, 80]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_20 = rb_tree.root
        self.assertEqual(node_20.key, 20)
        self.assertEqual(node_20.parent, None)
        self.assertEqual(node_20.red, False)
        self.assertEqual(node_20.left.key, -10)
        self.assertEqual(node_20.right.key, 60)
        # test left subtree
        node_m10 = node_20.left
        self.assertEqual(node_m10.key, -10)
        self.assertEqual(node_m10.red, False)
        self.assertEqual(node_m10.parent, node_20)
        self.assertEqual(node_m10.left.key, -20)
        self.assertEqual(node_m10.right.key, -5)
        node_m20 = node_m10.left
        self.assertEqual(node_m20.key, -20)
        self.assertEqual(node_m20.red, False)
        self.assertEqual(node_m20.parent, node_m10)
        self.assertEqual(node_m20.left, None)
        self.assertEqual(node_m20.right, None)
        node_m5 = node_m10.right
        self.assertEqual(node_m5.key, -5)
        self.assertEqual(node_m5.red, False)
        self.assertEqual(node_m5.parent, node_m10)
        self.assertEqual(node_m5.left, None)
        self.assertEqual(node_m5.right, None)
        # test right subtree
        node_60 = node_20.right
        self.assertEqual(node_60.key, 60)
        self.assertEqual(node_60.red, False)
        self.assertEqual(node_60.parent, node_20)
        self.assertEqual(node_60.left.key, 40)
        self.assertEqual(node_60.right.key, 80)
        node_80 = node_60.right
        self.assertEqual(node_80.key, 80)
        self.assertEqual(node_80.red, False)
        self.assertEqual(node_80.parent, node_60)
        self.assertEqual(node_80.left, None)
        self.assertEqual(node_80.right, None)
        node_40 = node_60.left
        self.assertEqual(node_40.key, 40)
        self.assertEqual(node_40.red, False)
        self.assertEqual(node_40.parent, node_60)
        self.assertEqual(node_40.left, None)
        self.assertEqual(node_40.right.key, 50)
        node_50 = node_40.right
        self.assertEqual(node_50.key, 50)
        self.assertEqual(node_50.red, True)
        self.assertEqual(node_50.parent, node_40)
        self.assertEqual(node_50.left, None)
        self.assertEqual(node_50.right, None)

    def test_mirror_deletion_black_node_successor_case_2_then_4(self):
        rb_tree = Tree()
        root = Node(key=20, red=False, parent=None, left=None, right=None)
        # left subtree
        node_10 = Node(key=10, red=False, parent=root, left=None, right=None)
        node_8 = Node(key=8, red=True, parent=node_10, left=None, right=None)
        node_15 = Node(key=15, red=False, parent=node_10, left=None, right=None)
        node_10.left = node_8
        node_10.right = node_15
        node_6 = Node(key=6, red=False, parent=node_8, left=None, right=None)
        node_9 = Node(key=9, red=False, parent=node_8, left=None, right=None)
        node_8.left = node_6
        node_8.right = node_9
        # right subtree
        node_30 = Node(key=30, red=False, parent=root, left=None, right=None)
        node_25 = Node(key=25, red=False, parent=node_30, left=None, right=None)
        node_35 = Node(key=35, red=False, parent=node_30, left=None, right=None)
        node_30.left = node_25
        node_30.right = node_35

        root.left = node_10
        root.right = node_30
        rb_tree.root = root
        del rb_tree[15]

        """

                ___20B___        Parent is black               ___20B___
               /         \       Sibling is red               /         \
            10B          30B     s.children are black        8B        30B
           /   \        /   \    ======>                    /  \       /   \
         8R    15B    25B   35B   Case 2                  6B   10R   25B   35B
        /  \    ^----Remove    left rotate                    /   \
       6B  9B                     on 10                      9B   |15B|



       Parent is red                                  ___20B___
       Sibling is black      CASE 4                  /         \
       s.children are black   ===>                  8B        30B
        switch the colors of the parent            /  \       /   \
        and the sibling                          6B   10B   25B   35B
                                                     /   \
                                                   9R     X
        """
        node_20 = rb_tree.root
        self.assertEqual(node_20.key, 20)
        self.assertEqual(node_20.red, False)
        self.assertEqual(node_20.parent, None)
        self.assertEqual(node_20.left.key, 8)
        self.assertEqual(node_20.right.key, 30)
        # right subtree
        node_30 = node_20.right
        self.assertEqual(node_30.key, 30)
        self.assertEqual(node_30.red, False)
        self.assertEqual(node_30.parent, node_20)
        self.assertEqual(node_30.left.key, 25)
        self.assertEqual(node_30.right.key, 35)
        node_25 = node_30.left
        self.assertEqual(node_25.key, 25)
        self.assertEqual(node_25.red, False)
        self.assertEqual(node_25.parent, node_30)
        self.assertEqual(node_25.left, None)
        self.assertEqual(node_25.right, None)
        node_35 = node_30.right
        self.assertEqual(node_35.key, 35)
        self.assertEqual(node_35.red, False)
        self.assertEqual(node_35.parent, node_30)
        self.assertEqual(node_35.left, None)
        self.assertEqual(node_35.right, None)
        # left subtree
        node_8 = node_20.left
        self.assertEqual(node_8.key, 8)
        self.assertEqual(node_8.parent, node_20)
        self.assertEqual(node_8.red, False)
        self.assertEqual(node_8.left.key, 6)
        self.assertEqual(node_8.right.key, 10)
        node_6 = node_8.left
        self.assertEqual(node_6.key, 6)
        self.assertEqual(node_6.red, False)
        self.assertEqual(node_6.parent, node_8)
        self.assertEqual(node_6.left, None)
        self.assertEqual(node_6.right, None)
        node_10 = node_8.right
        self.assertEqual(node_10.key, 10)
        self.assertEqual(node_10.red, False)
        self.assertEqual(node_10.parent, node_8)
        self.assertEqual(node_10.left, node_9)
        self.assertEqual(node_10.right, None)
        node_9 = node_10.left
        self.assertEqual(node_9.key, 9)
        self.assertEqual(node_9.red, True)
        self.assertEqual(node_9.parent, node_10)
        self.assertEqual(node_9.left, None)
        self.assertEqual(node_9.right, None)

    def test_delete_tree_one_by_one(self):
        rb_tree = Tree()
        root = Node(key=20, red=False, parent=None, left=None, right=None)
        # left subtree
        node_10 = Node(key=10, red=False, parent=root, left=None, right=None)
        node_5 = Node(key=5, red=True, parent=node_10, left=None, right=None)
        node_15 = Node(key=15, red=True, parent=node_10, left=None, right=None)
        node_10.left = node_5
        node_10.right = node_15
        # right subtree
        node_38 = Node(key=38, red=True, parent=root, left=None, right=None)
        node_28 = Node(key=28, red=False, parent=node_38, left=None, right=None)
        node_48 = Node(key=48, red=False, parent=node_38, left=None, right=None)
        node_38.left = node_28
        node_38.right = node_48
        # node_28 subtree
        node_23 = Node(key=23, red=True, parent=node_28, left=None, right=None)
        node_29 = Node(key=29, red=True, parent=node_28, left=None, right=None)
        node_28.left = node_23
        node_28.right = node_29
        # node 48 subtree
        node_41 = Node(key=41, red=True, parent=node_48, left=None, right=None)
        node_49 = Node(key=49, red=True, parent=node_48, left=None, right=None)
        node_48.left = node_41
        node_48.right = node_49

        root.left = node_10
        root.right = node_38
        """
                        ______20______
                       /              \
                     10B           ___38R___
                    /   \         /         \
                  5R    15R      28B         48B
                                /  \        /   \
                              23R  29R     41R   49R
        """
        rb_tree.root = root
        del rb_tree[49]
        del rb_tree[38]
        del rb_tree[28]
        del rb_tree[10]
        del rb_tree[5]
        del rb_tree[15]
        del rb_tree[48]
        """
            We're left with
                            __23B__
                           /       \
                         20B       41B
                                  /
                                 29R
        """
        node_23 = rb_tree.root
        self.assertEqual(node_23.key, 23)
        self.assertEqual(node_23.red, False)
        self.assertEqual(node_23.parent, None)
        self.assertEqual(node_23.left.key, 20)
        self.assertEqual(node_23.right.key, 41)
        node_20 = node_23.left
        self.assertEqual(node_20.red, False)
        self.assertEqual(node_20.parent, node_23)
        self.assertEqual(node_20.left, None)
        self.assertEqual(node_20.right, None)
        node_41 = node_23.right
        self.assertEqual(node_41.red, False)
        self.assertEqual(node_41.parent, node_23)
        self.assertEqual(node_41.key, 41)
        self.assertEqual(node_41.left.key, 29)
        self.assertEqual(node_41.right, None)
        node_29 = node_41.left
        self.assertEqual(node_29.key, 29)
        self.assertEqual(node_29.red, True)
        self.assertEqual(node_29.left, None)
        self.assertEqual(node_29.right, None)
        del rb_tree[20]
        """
            _29B_
           /     \
          23B    41B
        """
        node_29 = rb_tree.root
        self.assertEqual(node_29.key, 29)
        self.assertEqual(node_29.red, False)
        self.assertEqual(node_29.parent, None)
        self.assertEqual(node_29.left.key, 23)
        self.assertEqual(node_29.right.key, 41)
        node_23 = node_29.left
        self.assertEqual(node_23.parent, node_29)
        self.assertEqual(node_23.red, False)
        self.assertEqual(node_23.left, None)
        self.assertEqual(node_23.right, None)
        node_41 = node_29.right
        self.assertEqual(node_41.parent, node_29)
        self.assertEqual(node_41.red, False)
        self.assertEqual(node_41.left, None)
        self.assertEqual(node_41.right, None)
        del rb_tree[29]
        """
            41B
           /
         23R
        """
        node_41 = rb_tree.root
        self.assertEqual(node_41.key, 41)
        self.assertEqual(node_41.red, False)
        self.assertEqual(node_41.parent, None)
        self.assertEqual(node_41.right, None)
        node_23 = node_41.left
        self.assertEqual(node_23.key, 23)
        self.assertEqual(node_23.red, True)
        self.assertEqual(node_23.parent, node_41)
        self.assertEqual(node_23.left, None)
        self.assertEqual(node_23.right, None)
        del rb_tree[41]
        """
            23B
        """
        node_23 = rb_tree.root
        self.assertEqual(node_23.key, 23)
        self.assertEqual(node_23.red, False)
        self.assertEqual(node_23.parent, None)
        self.assertEqual(node_23.left, None)
        self.assertEqual(node_23.right, None)
        del rb_tree[23]
        self.assertEqual(rb_tree.root, None)

    # ***************TEST DELETIONS***************

    def test_add_delete_random_order(self):
        """
        What I add here I'll also add at a site for red black tree visualization
        https://www.cs.usfca.edu/~galles/visualization/RedBlack.html
        and then see if they're the same
        """
        rb_tree = Tree()
        rb_tree.insert(90)
        rb_tree.insert(70)
        rb_tree.insert(43)
        del rb_tree[70]
        rb_tree.insert(24)
        rb_tree.insert(14)
        rb_tree.insert(93)
        rb_tree.insert(47)
        del rb_tree[47]
        del rb_tree[90]
        rb_tree.insert(57)
        rb_tree.insert(1)
        rb_tree.insert(60)
        rb_tree.insert(47)
        del rb_tree[47]
        del rb_tree[1]
        del rb_tree[43]
        rb_tree.insert(49)
        """
        well, the results aren't the same, but I'll assume that the algorithms are different
        Nevertheless, what we're left with is a perfectly valid RedBlack Tree, and, I'd argue, even betterly
        balanced than the one from the visualization

                                    VISUALIZATION TREE
                                       ____24B____
                                      /           \
                                    14B           60R
                                                 /   \
                                               57B    93B
                                              /
                                            49R

                                       OUR TREE
                                       ______57B______
                                      /               \
                                  __24B__           __60B__
                                 /       \                 \
                               14R       49R               93R
        """
        expected_keys = [14, 24, 49, 57, 60, 93]
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)

        node_57 = rb_tree.root
        self.assertEqual(node_57.key, 57)
        self.assertEqual(node_57.parent, None)
        self.assertEqual(node_57.red, False)
        self.assertEqual(node_57.left.key, 24)
        self.assertEqual(node_57.right.key, 60)
        # right subtree
        node_60 = node_57.right
        self.assertEqual(node_60.key, 60)
        self.assertEqual(node_60.red, False)
        self.assertEqual(node_60.parent, node_57)
        self.assertEqual(node_60.right.key, 93)
        self.assertEqual(node_60.left, None)
        node_93 = node_60.right
        self.assertEqual(node_93.key, 93)
        self.assertEqual(node_93.red, True)
        self.assertEqual(node_93.parent, node_60)
        self.assertEqual(node_93.left, None)
        self.assertEqual(node_93.right, None)
        # left subtree
        node_24 = node_57.left
        self.assertEqual(node_24.key, 24)
        self.assertEqual(node_24.parent, node_57)
        self.assertEqual(node_24.red, False)
        self.assertEqual(node_24.left.key, 14)
        self.assertEqual(node_24.right.key, 49)
        node_14 = node_24.left
        self.assertEqual(node_14.key, 14)
        self.assertEqual(node_14.parent, node_24)
        self.assertEqual(node_14.red, True)
        self.assertEqual(node_14.left, None)
        self.assertEqual(node_14.right, None)
        node_49 = node_24.right
        self.assertEqual(node_49.key, 49)
        self.assertEqual(node_49.parent, node_24)
        self.assertEqual(node_49.red, True)
        self.assertEqual(node_49.left, None)
        self.assertEqual(node_49.right, None)

    def test_add_0_to_100_delete_100_to_0(self):
        rb_tree = Tree()
        for i in range(100):
            rb_tree.insert(i)
            self.assertEqual(rb_tree._len, i+1)
        expected_keys = list(range(100))
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)
        for i in range(99, -1, -1):
            self.assertTrue(rb_tree.__contains__(i))
            del rb_tree[i]
            self.assertFalse(rb_tree.__contains__(i))
            self.assertEqual(rb_tree._len, i)
        self.assertIsNone(rb_tree.root)

    def test_add_delete_0_to_100_delete_0_to_100(self):
        rb_tree = Tree()
        for i in range(100):
            rb_tree.insert(i)
            self.assertEqual(rb_tree._len, i+1)
        expected_keys = list(range(100))
        keys = list(rb_tree.keys())
        self.assertEqual(keys, expected_keys)
        for i in range(100):
            self.assertTrue(rb_tree.__contains__(i))
            del rb_tree[i]
            self.assertFalse(rb_tree.__contains__(i))
            self.assertEqual(rb_tree._len, 99-i)
        self.assertIsNone(rb_tree.root)

    # ***************TEST DELETIONS***************

    # ***************MISC TESTS***************

    def test_ceil(self):
        # add all the numbers 0-99 step 2
        # i.e 0, 2, 4
        rb_tree = Tree()
        for i in range(0, 100, 2):
            rb_tree.insert(i)
        # then search for the ceilings, knowing theyre 1 up
        for i in range(1, 99, 2):
            self.assertEqual(rb_tree.floor_and_ceil(i)[1].key, i+1)

    def test_ceil_same_key(self):
        rb_tree = Tree()

        rb_tree.insert(10)
        rb_tree.insert(15)
        rb_tree.insert(20)
        rb_tree.insert(17)

        for i in range(11):
            self.assertEqual(rb_tree.floor_and_ceil(i)[1].key, 10)
        for i in range(11, 16):
            self.assertEqual(rb_tree.floor_and_ceil(i)[1].key, 15)
        for i in range(16, 18):
            self.assertEqual(rb_tree.floor_and_ceil(i)[1].key, 17)
        for i in range(18, 21):
            self.assertEqual(rb_tree.floor_and_ceil(i)[1].key, 20)

    def test_floor(self):
        # add all the numbers 0-99 step 2
        # i.e 0, 2, 4
        rb_tree = Tree()
        for i in range(0, 100, 2):
            rb_tree.insert(i)
        # then search for the ceilings, knowing theyre 1 up
        for i in range(1, 99, 2):
            self.assertEqual(rb_tree.floor_and_ceil(i)[0].key, i - 1)

    def test_floor_same_key(self):
        rb_tree = Tree()

        rb_tree.insert(10)
        rb_tree.insert(15)
        rb_tree.insert(20)
        rb_tree.insert(17)

        for i in range(11, 15):
            self.assertEqual(rb_tree.floor_and_ceil(i)[0].key, 10)
        for i in range(15, 17):
            self.assertEqual(rb_tree.floor_and_ceil(i)[0].key, 15)
        for i in range(17, 20):
            self.assertEqual(rb_tree.floor_and_ceil(i)[0].key, 17)
        for i in range(20, 50):
            self.assertEqual(rb_tree.floor_and_ceil(i)[0].key, 20)


# These tests take the bulk of the time for testing.
class RbTreePerformanceTests(unittest.TestCase):
    def test_addition_performance(self):
        """
        Add 25,000 elements to the tree
        """
        possible_keys = list(range(-100000, 100000))
        elements = [random.choice(possible_keys) for _ in range(25000)]
        start_time = datetime.now()
        tree = Tree()
        for el in elements:
            tree.insert(el)
        time_taken = datetime.now()-start_time
        self.assertTrue(time_taken.seconds < 1)

    def test_deletion_performance(self):
        """
        Delete 25,000 elements from the tree
        """
        possible_keys = list(range(-100000, 100000))
        elements = set([random.choice(possible_keys) for _ in range(25000)])
        # fill up the tree
        tree = Tree()
        for el in elements:
            _, success = tree.insert(el)
            self.assertTrue(success)
        start_time = datetime.now()
        for el in elements:
            del tree[el]
        time_taken = datetime.now()-start_time
        self.assertTrue(time_taken.seconds < 1)

    def test_deletion_and_addition_performance(self):
        possible_keys = list(range(-500000, 500000))
        elements = list(set([random.choice(possible_keys) for _ in range(25000)]))
        first_part = elements[:len(elements)//2]
        second_part = elements[len(elements)//2:]
        deletion_part = first_part[len(first_part)//3:(len(first_part)//3)*2]
        tree = Tree()
        start_time = datetime.now()

        # fill up the tree 1/2
        for el in first_part:
            tree.insert(el)
        # delete 1/2 of the tree
        for del_el in deletion_part:
            del tree[del_el]
        for el in second_part:
            tree.insert(el)

        time_taken = datetime.now()-start_time
        self.assertTrue(time_taken.seconds < 1)


if __name__ == '__main__':
    unittest.main()
