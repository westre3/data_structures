import unittest

from data_structures import Red_Black_Node, Red_Black_Tree, BLACK, RED

def Red_Black_Tree_Suite():
  suite = unittest.TestSuite()
  suite.addTest(Red_Black_Tree_Basic())
  suite.addTest(Red_Black_Tree_Insert())
  return suite

class Common_Functions(unittest.TestCase):
  def recursive_bst(self, g, n):
    """
    Method to recursively verify that the tree has the Binary Search Tree
    property (the key of any node in the left subtree of n is less than n's
              key, and the key of any node in the right subtree of n is
              greater than or equal to n's key)
    """

    if n.left != g.nil:
      max_left = g.Maximum(n.left).key
      self.assertLess(max_left, n.key, f"BST Property Violated : A node with key {max_left} is in the left subtree of a node with key {n.key}")
      self.recursive_bst(g, n.left)
    
    if n.right != g.nil:
      min_right = g.Minimum(n.right).key
      self.assertGreaterEqual(min_right, n.key, f"BST Property Violated : A node with key {min_right} is in the right subtree of a node with key {n.key}")
      self.recursive_bst(g, n.right)
  
  def test_bst(self, g):
    self.recursive_bst(g, g.root)

  def recursive_property_one(self, g, n):
    self.assertIn(n.color, [RED, BLACK], f"Property 1 Violated : Node with key {n.key} is neither RED nor BLACK")
    
    if n.left != g.nil:
      self.recursive_property_one(g, n.left)
    
    if n.right != g.nil:
      self.recursive_property_one(g, n.right)
  
  def test_property_one(self, g):
    self.assertIn(g.nil.color, [RED, BLACK], "Property 1 Violated : Leaf node is neither RED nor BLACK")
    
    self.recursive_property_one(g, g.root)
  
  def test_property_two(self, g):
    self.assertEqual(g.root.color, BLACK, "Property 2 Violated : Root node is not BLACK")
  
  def test_property_three(self, g):
    self.assertEqual(g.nil.color, BLACK, "Property 3 Violated : Leaf node is not BLACK")
  
  def recursive_property_four(self, g, n):
    if n.color == RED:
      self.assertNotEqual(n.left.color, RED, f"Property 4 Violated : node with key {n.key} is RED and has RED left child with key {n.left.key}")
      self.assertNotEqual(n.right.color, RED, f"Property 4 Violated : node with key {n.key} is RED and has RED right child with key {n.right.key}")
    
    if n.left != g.nil:
      self.recursive_property_four(g, n.left)
    
    if n.right != g.nil:
      self.recursive_property_four(g, n.right)
  
  def test_property_four(self, g):
    self.recursive_property_four(g, g.root)
  
  def recursive_property_five(self, g, n, bh):
    if n == g.nil:
      return bh + 1
    
    if n.color == BLACK:
      bh += 1
      
    left_bh = self.recursive_property_five(g, n.left, bh)  
    right_bh = self.recursive_property_five(g, n.right, bh)
    self.assertEqual(left_bh, right_bh, f"Property 5 Violated : node with key {n.key} black height is not consistent (left bh ({left_bh}) != right_bh ({right_bh})")
    
    return left_bh # equal to right_bh
  
  def test_property_five(self, g):
    self.recursive_property_five(g, g.root, 0)
  
  def test_properties(self, g):
    self.test_property_one(g)
    self.test_property_two(g)
    self.test_property_three(g)
    self.test_property_four(g)
    self.test_property_five(g)

class Red_Black_Tree_Basic(unittest.TestCase):
  """
  Tests for basic functionality of Red Black Trees
  """
  
  def runTest(self):
    tests = [
            self.test_empty,
            self.test_insert,
            self.test_min,
            self.test_max,
            self.test_search,
            self.test_successor,
            self.test_predecessor
            ]
    
    for test in tests:
      test()

  def test_empty(self):
    """
    Test an empty tree that has just been initialized.
    """
    
    g = Red_Black_Tree()
    
    # In an empty tree, the root node is the leaf node
    self.assertEqual(g.root, g.nil, "Root node in empty tree is not equal to leaf")
    
    # In an empty tree, the root's parent is the leaf
    self.assertEqual(g.root.p, g.nil, "Root node's parent in empty tree is not leaf")
    
    # In an empty tree, the root node is BLACK
    self.assertEqual(g.root.color, BLACK, "Root node in empty tree is not BLACK")

  def test_insert(self):
    """
    Test a tree that has one node inserted.
    """
    
    g = Red_Black_Tree()
    g.Insert(1)
    
    # Inserted node is now the root node and is distinct from the leaf
    self.assertEqual(g.root.key, 1, "Inserted node is not the root node")
    self.assertNotEqual(g.nil.key, 1, "Inserted node is not distinct from leaf node")
    
    # Inserted node has leaf node as left and right children
    self.assertEqual(g.root.left, g.nil, "Inserted node's left child is not leaf")
    self.assertEqual(g.root.right, g.nil, "Inserted node's right child is not leaf")
    
    # Inserted node has nil as its parent
    self.assertEqual(g.root.p, g.nil, "Inserted node's parent is not leaf")
    
    # Both root node and leaf are BLACK
    self.assertEqual(g.root.color, BLACK, "Root node is not BLACK")
    self.assertEqual(g.nil.color, BLACK, "Leaf node is not BLACK")
  
  def test_min(self):
    """
    Test the min function
    """
    
    g = Red_Black_Tree()
    
    max_key = 10
    min_key = 1
    for i in range(min_key, max_key+1):
      g.Insert(i)
    
    g_min = g.Minimum(g.root).key
    self.assertEqual(g_min, min_key, f"Tree minimum returned {g_min} (Expected {min_key})")
    
    g = Red_Black_Tree()
    for i in range(max_key, min_key-1, -1):
      g.Insert(i)
    
    g_min = g.Minimum(g.root).key
    self.assertEqual(g_min, min_key, f"Tree minimum returned {g_min} (Expected {min_key})")
  
  def test_max(self):
    """
    Test the max function
    """
    
    g = Red_Black_Tree()
    
    max_key = 10
    min_key = 1
    for i in range(min_key, max_key+1):
      g.Insert(i)
    
    g_max = g.Maximum(g.root).key
    self.assertEqual(g_max, max_key, f"Tree maximum returned {g_max} (Expected {max_key})")
    
    g = Red_Black_Tree()
    for i in range(max_key, min_key-1, -1):
      g.Insert(i)
    
    g_max = g.Maximum(g.root).key
    self.assertEqual(g_max, max_key, f"Tree maximum returned {g_max} (Expected {max_key})")

  def test_search(self):
    """
    Test the search function
    """
    
    g = Red_Black_Tree()
    
    max_key = 10
    min_key = 1
    for i in range(min_key, max_key+1):
      g.Insert(i)
    
    for i in range(min_key, max_key+1):
      search_result = g.Search(g.root, i).key
      self.assertEqual(search_result, i, f"Searched for {i} but found {search_result}")
    
    g = Red_Black_Tree()
    for i in range(max_key, min_key-1, -1):
      g.Insert(i)

    for i in range(min_key, max_key+1):
      search_result = g.Search(g.root, i).key
      self.assertEqual(search_result, i, f"Searched for {i} but found {search_result}")

  def test_successor(self):
    """
    Test the successor function
    """
    
    g = Red_Black_Tree()
    
    max_key = 10
    min_key = 1
    for i in range(min_key, max_key+1):
      g.Insert(i)
    
    for i in range(min_key, max_key):
      search_result = g.Search(g.root, i)
      successor = g.Successor(search_result).key
      self.assertEqual(successor, i+1, f"Successor of node with key {i} returned {successor} (Expected {i+1})")
    
    g = Red_Black_Tree()
    for i in range(max_key, min_key-1, -1):
      g.Insert(i)

    for i in range(min_key, max_key):
      search_result = g.Search(g.root, i)
      successor = g.Successor(search_result).key
      self.assertEqual(successor, i+1, f"Successor of node with key {i} returned {successor} (Expected {i+1})")

  def test_predecessor(self):
    """
    Test the predecessor function
    """
    
    g = Red_Black_Tree()
    
    max_key = 10
    min_key = 1
    for i in range(min_key, max_key+1):
      g.Insert(i)
    
    for i in range(min_key+1, max_key+1):
      search_result = g.Search(g.root, i)
      predecessor = g.Predecessor(search_result).key
      self.assertEqual(predecessor, i-1, f"Predecessor of node with key {i} returned {predecessor} (Expected {i-1})")
    
    g = Red_Black_Tree()
    for i in range(max_key, min_key-1, -1):
      g.Insert(i)

    for i in range(min_key+1, max_key+1):
      search_result = g.Search(g.root, i)
      predecessor = g.Predecessor(search_result).key
      self.assertEqual(predecessor, i-1, f"Predecessor of node with key {i} returned {predecessor} (Expected {i-1})")

class Red_Black_Tree_Insert(Common_Functions):
  """
  Tests that Insert works and maintains Red Black Properties
  """

  def runTest(self):
    tests = [
            self.test_case_3_1,
            self.test_case_2_1,
            self.test_case_1_1,
            self.test_case_3_2,
            self.test_case_2_2,
            self.test_case_1_2
            ]

    for test in tests:
      test()

  def test_case_1_1(self):
    """
    Test that Insert_Fixup resolves violations in Case 1 of CLRS when z's
    uncle is its grandparent's right child
    """

    # Create graph shown to Figure 13.4(a) in CLRS to test Case 1    
    g = Red_Black_Tree()

    n11 = Red_Black_Node(11)
    n2 = Red_Black_Node(2)
    n1 = Red_Black_Node(1)
    n7 = Red_Black_Node(7)
    n5 = Red_Black_Node(5)
    n4 = Red_Black_Node(4)
    n8 = Red_Black_Node(8)
    n14 = Red_Black_Node(14)
    n15 = Red_Black_Node(15)
    
    n11.color = BLACK
    n2.color = RED
    n1.color = BLACK
    n7.color = BLACK
    n5.color = RED
    n4.color = RED
    n8.color = RED
    n14.color = BLACK
    n15.color = RED
    
    n11.p = g.nil
    n11.left = n2
    n2.p = n11
    n11.right = n14
    n14.p = n11
    
    n2.left = n1
    n1.p = n2
    n2.right = n7
    n7.p = n2
    
    n1.left = g.nil
    n1.right = g.nil
    
    n7.left = n5
    n5.p = n7
    n7.right = n8
    n8.p = n7
    
    n5.left = n4
    n4.p = n5
    n5.right = g.nil
    
    n4.left = g.nil
    n4.right = g.nil
    
    n8.left = g.nil
    n8.right = g.nil
    
    n14.left = g.nil
    n14.right = n15
    n15.p = n14
    
    n15.left = g.nil
    n15.right = g.nil
    
    g.root = n11
    g.Insert_Fixup(n4)
    
    # Ensure tree now has Binary Search Tree and Red Tree properties
    self.test_bst(g)
    self.test_properties(g)

  def test_case_1_2(self):
    """
    Test that Insert_Fixup resolves violations in Case 1 of CLRS when z's
    uncle is its grandparent's left child
    """

    # Create graph similar to Figure 13.4(a) in CLRS, except with z's uncle
    # as its grandparent's left child, to test Case 1
    g = Red_Black_Tree()

    n11 = Red_Black_Node(11)
    n2 = Red_Black_Node(2)
    n1 = Red_Black_Node(1)
    n7 = Red_Black_Node(7)
    n5 = Red_Black_Node(5)
    n9 = Red_Black_Node(9)
    n8 = Red_Black_Node(8)
    n14 = Red_Black_Node(14)
    n15 = Red_Black_Node(15)
    
    n11.color = BLACK
    n2.color = RED
    n1.color = BLACK
    n7.color = BLACK
    n5.color = RED
    n9.color = RED
    n8.color = RED
    n14.color = BLACK
    n15.color = RED
    
    n11.p = g.nil
    n11.left = n2
    n2.p = n11
    n11.right = n14
    n14.p = n11
    
    n2.left = n1
    n1.p = n2
    n2.right = n7
    n7.p = n2
    
    n1.left = g.nil
    n1.right = g.nil
    
    n7.left = n5
    n5.p = n7
    n7.right = n9
    n9.p = n7
    
    n5.left = g.nil
    n5.right = g.nil
    
    n9.left = n8
    n8.p = n9
    n9.right = g.nil
    
    n8.left = g.nil
    n8.right = g.nil
    
    n14.left = g.nil
    n14.right = n15
    n15.p = n14
    
    n15.left = g.nil
    n15.right = g.nil
    
    g.root = n11
    g.Insert_Fixup(n8)
    
    # Ensure tree now has Binary Search Tree and Red Tree properties
    self.test_bst(g)
    self.test_properties(g)
  
  def test_case_2_1(self):
    """
    Test that Insert_Fixup resolves violations in Case 2 of CLRS when z's
    uncle is its grandparent's right child
    """
    
    # Create graph shown in Figure 13.4(b) in CLRS to test Case 2
    g = Red_Black_Tree()
    
    n11 = Red_Black_Node(11)
    n2 = Red_Black_Node(2)
    n1 = Red_Black_Node(1)
    n7 = Red_Black_Node(7)
    n5 = Red_Black_Node(5)
    n4 = Red_Black_Node(4)
    n8 = Red_Black_Node(8)
    n14 = Red_Black_Node(14)
    n15 = Red_Black_Node(15)
    
    n11.color = BLACK
    n2.color = RED
    n1.color = BLACK
    n7.color = RED
    n5.color = BLACK
    n4.color = RED
    n8.color = BLACK
    n14.color = BLACK
    n15.color = RED
    
    n11.p = g.nil
    n11.left = n2
    n2.p = n11
    n11.right = n14
    n14.p = n11
    
    n2.left = n1
    n1.p = n2
    n2.right = n7
    n7.p = n2
    
    n1.left = g.nil
    n1.right = g.nil
    
    n7.left = n5
    n5.p = n7
    n7.right = n8
    n8.p = n7
    
    n5.left = n4
    n4.p = n5
    n5.right = g.nil
    
    n4.left = g.nil
    n4.right = g.nil
    
    n8.left = g.nil
    n8.right = g.nil
    
    n14.left = g.nil
    n14.right = n15
    n15.p = n14
    
    n15.left = g.nil
    n15.right = g.nil
    
    g.root = n11
    g.Insert_Fixup(n7)
    
    self.test_bst(g)
    self.test_properties(g)

  def test_case_2_2(self):
    """
    Test that Insert_Fixup resolves violations in Case 2 of CLRS when z's
    uncle is its grandparent's left child
    """
    
    g = Red_Black_Tree()
    
    n11 = Red_Black_Node(11)
    n4 = Red_Black_Node(4)
    n5 = Red_Black_Node(5)
    n15 = Red_Black_Node(15)
    n13 = Red_Black_Node(13)
    n12 = Red_Black_Node(12)
    n14 = Red_Black_Node(14)
    n18 = Red_Black_Node(18)
    
    n11.color = BLACK
    n4.color = BLACK
    n5.color = RED
    n15.color = RED
    n13.color = RED
    n12.color = BLACK
    n14.color = BLACK
    n18.color = BLACK
    
    n11.p = g.nil
    n11.left = n4
    n4.p = n11
    n11.right = n15
    n15.p = n11
    
    n4.left = g.nil
    n4.right = n5
    n5.p = n4
    
    n5.left = g.nil
    n5.right = g.nil
    
    n15.left = n13
    n13.p = n15
    n15.right = n18
    n18.p = n15
    
    n13.left = n12
    n12.p = n13
    n13.right = n14
    n14.p = n13
    
    n12.left = g.nil
    n12.right = g.nil
    
    n14.left = g.nil
    n14.right = g.nil
    
    n18.left = g.nil
    n18.right = g.nil
    
    g.root = n11
    g.Insert_Fixup(n13)
    
    self.test_bst(g)
    self.test_properties(g)

  def test_case_3_1(self):
    """
    Test that Insert_Fixup resolves violations in Case 3 of CLRS when z's
    uncle is its grandparent's right child
    """
    
    # Create graph shown to Figure 13.4(c) in CLRS to test Case 3
    g = Red_Black_Tree()
    
    n11 = Red_Black_Node(11)
    n7 = Red_Black_Node(7)
    n2 = Red_Black_Node(2)
    n1 = Red_Black_Node(1)
    n5 = Red_Black_Node(5)
    n4 = Red_Black_Node(4)
    n8 = Red_Black_Node(8)
    n14 = Red_Black_Node(14)
    n15 = Red_Black_Node(15)
    
    n11.color = BLACK
    n7.color = RED
    n2.color = RED
    n1.color = BLACK
    n5.color = BLACK
    n4.color = RED
    n8.color = BLACK
    n14.color = BLACK
    n15.color = RED
    
    n11.p = g.nil
    n11.left = n7
    n7.p = n11
    n11.right = n14
    n14.p = n11
    
    n7.left = n2
    n2.p = n7
    n7.right = n8
    n8.p = n7
    
    n2.left = n1
    n1.p = n2
    n2.right = n5
    n5.p = n2
    
    n1.left = g.nil
    n1.right = g.nil
    
    n5.left = n4
    n4.p = n5
    n5.right = g.nil
    
    n4.left = g.nil
    n4.right = g.nil
    
    n8.left = g.nil
    n8.right = g.nil
    
    n14.left = g.nil
    n14.right = n15
    n15.p = n14
    
    n15.left = g.nil
    n15.right = g.nil
    
    g.root = n11
    g.Insert_Fixup(n2)
    
    self.test_bst(g)
    self.test_properties(g)
  
  def test_case_3_2(self):
    """
    Test that Insert_Fixup resolves violations in Case 3 of CLRS when z's
    uncle is its grandparent's left child
    """
    
    g = Red_Black_Tree()
    
    n11 = Red_Black_Node(11)
    n4 = Red_Black_Node(4)
    n15 = Red_Black_Node(15)
    n13 = Red_Black_Node(13)
    n18 = Red_Black_Node(18)
    n16 = Red_Black_Node(16)
    n19 = Red_Black_Node(19)
    
    n11.color = BLACK
    n4.color = BLACK
    n15.color = RED
    n13.color = BLACK
    n18.color = RED
    n16.color = BLACK
    n19.color = BLACK
    
    n11.p = g.nil
    n11.left = n4
    n4.p = n11
    n11.right = n15
    n15.p = n11
    
    n4.left = g.nil
    n4.right = g.nil
    
    n15.left = n13
    n13.p = n15
    n15.right = n18
    n18.p = n15
    
    n13.left = g.nil
    n13.right = g.nil
    
    n18.left = n16
    n16.p = n18
    n18.right = n19
    n19.p = n18
    
    n16.left = g.nil
    n16.right = g.nil
    
    n19.left = g.nil
    n19.right = g.nil
    
    g.root = n11
    g.Insert_Fixup(n18)
    
    self.test_bst(g)
    self.test_properties(g)
    
class Red_Black_Tree_Delete(unittest.TestCase):
  pass

class Red_Black_Tree_Advanced(unittest.TestCase):  
  def test_bst_property(self):
    """
    Insert 100 nodes in the Red Black Tree and verify that the Binary Search
    Tree property is maintained
    """
    
    g = Red_Black_Tree()
    
    for i in range(100):
      g.Insert(i)
    
    self.recursive_bst(g, g.root)
  
  def test_properties(self):
    """
    Inserts 100 nodes and verifies that all 5 properties of Red Black Trees
    are maintained.
    """
    
    

if __name__ == "__main__":
  runner = unittest.TextTestRunner()
  runner.run(Red_Black_Tree_Suite())