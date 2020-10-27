BLACK = 0
RED   = 1

# A node in a Red Black Tree as presented in the CLRS textbook
class Red_Black_Node:
  """
  A node in a Red Black Tree as presented in the CLRS textbook. The node has
  the following attributes:
    
    key   : The key used to compare this node against other nodes
    left  : The node's left child
    right : The node's right child
    p     : The node's parent
    color : The node's color (either RED or BLACK)
  """
  
  def __init__(self, key : int):
    """
    Initializes the key to the value passed to the constructor and initializes
    all other values to None.

    Parameters
    ----------
    key : int
      The key of the node.

    Returns
    -------
    None.

    """
    
    # The key used to refer to this node
    self.key = key
    
    # Left child
    self.left = None
    
    # Right child
    self.right = None
    
    # Parent
    self.p = None
    
    # Color (Red or Black)
    self.color = None

# A Red Black Tree as presented in the CLRS textbook
class Red_Black_Tree:
  """
  A Red Black Tree as presented in the CLRS textbook. Red Black Trees are
  Binary Search Trees that that height balance themselves
  (keep h = O(lg(n))) by maintaining the following properties:
    
    1. Every node is either RED or BLACK
    2. The root is BLACK
    3. Every leaf is BLACK
    4. If a node is RED, it has no RED children
    5. For each node, all simple paths from the node to descendant leaves
       contain the same number of black nodes
  """
  
  def __init__(self):
    """
    Creates sentinel leaf (called T.nil in CLRS) and sets root equal to it

    Returns
    -------
    None.

    """
    
    # Create sentinel T.nil
    self.nil = Red_Black_Node(None)
    self.nil.left = None
    self.nil.right = None
    self.nil.p = None
    self.nil.color = BLACK

    # Initialize self.root to the sentinel T.nil    
    self.root = self.nil
    self.root.p = self.nil
    self.root.l = self.nil
    self.root.r = self.nil
    
    # Some bookeeping information
    self.num_nodes = 0

  def isEmpty(self):
    """
    Returns True if there are nodes in the tree and False otherwise.
    """
    
    return self.root == self.nil
  
  def Size(self):
    """
    Returns the number of nodes in the tree.
    """
    
    return self.num_nodes

  def Search(self, x : Red_Black_Node, k : int) -> Red_Black_Node:
    """
    A performs a classic search through a Binary Search Tree for a node whose
    key is equal to k.

    Parameters
    ----------
    x : Red_Black_Node
      The root of the subtree to be searched.
    k : int
      The key that we are searching for

    Returns
    -------
    Red_Black_Node
      A node whose key is equal to k or is None (if a node with key equal
                                                 to k is not found).

    """
    
    while x != self.nil and k != x.key:
      if k < x.key:
        x = x.left
      else:
        x = x.right
    return x
  
  def Minimum(self, x : Red_Black_Node) -> Red_Black_Node:
    """
    Finds the node with the minimum key in the subtree rooted at x.

    Parameters
    ----------
    x : Red_Black_Node
      The root of the subtree whose minimum will be returned.

    Returns
    -------
    Red_Black_Node
      The node with the minimum key in the subtree rooted at x.

    """
    
    while x.left != self.nil:
      x = x.left
    return x
  
  def Maximum(self, x : Red_Black_Node) -> Red_Black_Node:
    """
    Finds the node with the maximum key in the subtree rooted at x.

    Parameters
    ----------
    x : Red_Black_Node
      The root of the subtree whose maximum will be returned.

    Returns
    -------
    Red_Black_Node
      The node with the maximum key in the subtree rooted at x.

    """
    
    while x.right != self.nil:
      x = x.right
    return x
  
  def Successor(self, x : Red_Black_Node) -> Red_Black_Node:
    """
    Returns the successor of x (the node with the smallest key greater than x).

    Parameters
    ----------
    x : Red_Black_Node
      The node whose successor will be returned.

    Returns
    -------
    Red_Black_Node
      The node that is the successor of x.

    """
    
    if x.right != self.nil:
      return self.Minimum(x.right)
    else:
      y = x.p
      while y != self.nil and x == y.right:
        x = y
        y = y.p
      return y
  
  def Predecessor(self, x : Red_Black_Node) -> Red_Black_Node:
    """
    Returns the predecessor of x (the node with the largest key less than x).

    Parameters
    ----------
    x : Red_Black_Node
      The node whose predecessor will be returned.

    Returns
    -------
    Red_Black_Node
      The node that is the predecessor of x.

    """
    
    if x.left != self.nil:
      return self.Maximum(x.left)
    else:
      y = x.p
      while y != self.nil and x == y.left:
        x = y
        y = y.p
      return y
  
  def Insert(self, key : int) -> None:
    """
    Creates a new node z with the key and inserts it at the appropriate place
    in the tree, using Insert_Fixup to maintain Red Black properties.

    Parameters
    ----------
    key : int
      The key of the node to be inserted in the graph.

    Returns
    -------
    None

    """
    
    z = Red_Black_Node(key)
    
    y = self.nil
    x = self.root
    while x != self.nil:
      y = x
      if z.key < x.key:
        x = x.left
      else:
        x = x.right
    
    z.p = y
    
    if y == self.nil:
      self.root = z
    elif z.key < y.key:
      y.left = z
    else:
      y.right = z
    
    z.left = self.nil
    z.right = self.nil
    z.color = RED
    
    self.Insert_Fixup(z)
    
    self.num_nodes += 1
          
  def Delete(self, key : int) -> None:
    """
    Deletes node z from the tree. Calls Delete_Fixup to maintain Red Black
    properties.

    Parameters
    ----------
    key : int
      The key of the node to be deleted.

    Returns
    -------
    None

    """
    
    z = self.Search(self.root, key)
    
    if z == self.nil:
      return None
    
    # Throughout this algorithm, we keep track of z, the node to be deleted,
    # y, a node that may cause violations of the Red Black properties, and x,
    # the node that moves into y's original position (and may also cause
    # violations)
    y = z
    y_original_color = y.color
    
    # If z only has one child, then we want y = z and x = y's child
    if z.left == self.nil:
      x = z.right
      self.Transplant(z, x)
    elif z.right == self.nil:
      x = z.left
      self.Transplant(z, x)
    
    # If z has two children, then y should be z's successor. Now y replaces
    # z in the tree and x replaces y
    else:
      y = self.Successor(z)
      y_original_color = y.color
      
      # A successor cannot have a left child, so we know y will be replaced by
      # its right child
      x = y.right
      
      # Take care of replacing y with x and z with y
      if y.p == z:
        x.p = y
      else:
        self.Transplant(y, x)
        y.right = z.right
        y.right.p = y
      self.Transplant(z, y)
      y.left = z.left
      y.left.p = y
      y.color = z.color
    
    # If y was originally RED, no Red Black violations could have occurred.
    # We thus only have to fix the tree if y was originally black.
    if y_original_color == BLACK:
      self.Delete_Fixup(x)
    
    self.num_nodes -= 1
  
  ################## Auxiliary Funcntions ######################
  
  def Left_Rotate(self, x : Red_Black_Node) -> None:
    """
    Performs a left rotation on node x, assuming that x's right child is not the sentinel.
    This maintains the Binary Search Tree property, but not necessarily the
    Red Black Tree properties.

    Parameters
    ----------
    x : Red_Black_Node
      The node on which we are performing a left rotation.

    Returns
    -------
    None

    """
    
    y = x.right
    x.right = y.left
    if y.left != self.nil:
      y.left.p = x
    y.p = x.p
    if x.p == self.nil:
      self.root = y
    elif x == x.p.left:
      x.p.left = y
    else:
      x.p.right = y
    y.left = x
    x.p = y
  
  def Right_Rotate(self, y : Red_Black_Node) -> None:
    """
    Performs a right rotation on node x, assuming that x's left child is not the sentinel.
    This maintains the Binary Search Tree property, but not necessarily the
    Red Black Tree properties.

    Parameters
    ----------
    x : Red_Black_Node
      The node on which we are performing a right rotation.

    Returns
    -------
    None

    """

    x = y.left
    y.left = x.right
    if x.right != self.nil:
      x.right.p = y
    x.p = y.p
    if y.p == self.nil:
      self.root = x
    elif y == y.p.left:
      y.p.left = x
    else:
      y.p.right = x
    x.right = y
    y.p = x

  def Transplant(self, u : Red_Black_Node, v : Red_Black_Node) -> None:
    """
    Replaces the subtree rooted at node u with the subtree rooted at node v

    Parameters
    ----------
    u : Red_Black_Node
      The root of the subtree to be replaced.
    v : Red_Black_Node
      The root of the subtree doing the replacing.

    Returns
    -------
    None

    """
    
    if u.p == self.nil:
      self.root = v
    elif u == u.p.left:
      u.p.left = v
    else:
      u.p.right = v
    v.p = u.p
  
  def Insert_Fixup(self, z : Red_Black_Node) -> None:
    """
    Performs a sequence of re-colorings and rotations after an Insert to
    maintain Red Black properties. Note that insertions may only violate
    Property 2 or Property 4.

    Parameters
    ----------
    z : Red_Black_Node
      The node that was inserted.

    Returns
    -------
    None

    """
    # We are only violating Property 2 or 4 if both z and z's parent is RED
    while z.p.color == RED:
      
      # z's uncle is its grandparent's right child
      if z.p == z.p.p.left:
        y = z.p.p.right
        
        # z, z's parent, and z's uncle are RED, but z's grandparent is BLACK.
        # We fix this by making z's parent and z's uncle BLACK and z's
        # grandparent RED, then set z equal to its grandparent. (Case 1 in CLRS)
        if y.color == RED:
          z.p.color = BLACK
          y.color = BLACK
          z.p.p.color = RED
          z = z.p.p
        
        # z and z's parent are RED, but z's uncle and grandparent are BLACK.
        else:
          
          # z is its parent's right child (Case 2 in CLRS), so we change z
          # to be its parent and then rotate. Now z is its parent's left child
          if z == z.p.right:
            z = z.p
            self.Left_Rotate(z)
          
          # z is its parent's left child (Case 3 in CLRS)
          z.p.color = BLACK
          z.p.p.color = RED
          self.Right_Rotate(z.p.p)

      # z's uncle is its grandparent's left child
      else: # z.p == z.p.p.right
        y = z.p.p.left
        
        # z, z's parent, and z's uncle are RED, but z's grandparent is BLACK.
        # We fix this by making z's parent and z's uncle BLACK and z's
        # grandparent RED, then set z equal to its grandparent. (Case 1 in CLRS)
        if y.color == RED:
          z.p.color = BLACK
          y.color = BLACK
          z.p.p.color = RED
          z = z.p.p
        
        # z and z's parent are RED, but z's uncle and grandparent are BLACK.
        else:
          
          # z is its parent's left child (Case 2 in CLRS), so we change z
          # to be its parent and then rotate. Now z is its parent's right child
          if z == z.p.left:
            z = z.p
            self.Right_Rotate(z)
          
          # z is its parent's right child (Case 3 in CLRS)
          z.p.color = BLACK
          z.p.p.color = RED
          self.Left_Rotate(z.p.p)
        
    self.root.color = BLACK
  
  def Delete_Fixup(self, x : Red_Black_Node) -> None:
    """
    Performs a sequence of re-colorings and rotations after a Delete to
    maintain Red Black properties. Note this is only called if y was BLACK. If
    y was RED, we could not have violated any of the Red Black Tree proeprties:
      
      1. Every node is still RED or BLACK.
      2. If y was RED, it was not the root, so the root remains BLACK.
      3. y did not replace the sentinel leaf, so all leaves remain BLACK.
      4. No red nodes are now adjacent. y took on z's color, so the color of
         that node did not change. If y was RED, then its child x is BLACK, so
         replacing y with x could not put two RED nodes adjacent to each other.
      5. Since y was RED, no black heights in the tree have changed.
    
    If, however, y was BLACK, several properties could have been violated:
      
      1. Every node is still RED or BLACK.
      2. If y was the root node and x is RED, the root is now RED.
      3. The sentinel leaf is still BLACK.
      4. If y.p was RED and x is RED, then a RED node now has a RED child.
      5. Moving y within the tree caused any simple paths containing y to have
         one fewer BLACK node.

    Parameters
    ----------
    x : Red_Black_Node
      The node that replaced y in the Delete.

    Returns
    -------
    None

    """

    # We convert the violation of Property 5 to a violation of Property 1 by
    # adding y's BLACKness to x. Now x is either RED-BLACK or BLACK-BLACK. We
    # keep track of this in x.color: if x is RED-BLACK, x.color is RED. If x is
    # BLACK-BLACK, x.color is BLACK.We continue this while loop until:
    #   1. x is RED-BLACK, at which point we simply make it BLACK
    #   2. x is the root node, and we just remove the extra BLACK
    #   3. We exit because the rotations and re-colorings have
    #      solved the problem

    while x != self.root and x.color == BLACK:
      
      # x is its parent's left child
      if x == x.p.left:
        
        # We call x's sibling w
        w = x.p.right
        
        # x is BLACK-BLACK and x's sibling w is RED (Case 1 in CLRS).
        # Now w must have BLACK children. We swap the colors of w and x's
        # parent, then do a left rotation on x's parent. At this point, x's
        # new sibling (which was one of w's children before the rotation) is
        # BLACK, so we have converted Case 1 into Case 2, 3, or 4.
        if w.color == RED:
          w.color = BLACK
          x.p.color = RED
          self.Left_Rotate(x.p)
          w = x.p.right
        
        # x is BLACK-BLACK, x's sibling w is BLACK, and both of w's children
        # are BLACK (Case 2 in CLRS). We remove one BLACK from w (making it
        # RED) and push one BLACK from x to its parent (making x BLACK and x.p
        # either RED-BLACK or BLACK-BLACK). We thus repeat the loop with
        # x = x.p
        if w.left.color == BLACK and w.right.color == BLACK:
          w.color = RED
          x = x.p
        
        # x is BLACK-BLACK, x's sibling w is BLACK, but one of w's children
        # is RED
        else:
          
          # w's left child is RED and w's right child is BLACK (Case 3 in
          # CLRS). We swap the color of w and w's left child, then perform a 
          # right rotation. Now x's new sibling (which was w's left child) is
          # BLACK and has a RED right child (which was originally w). We have
          # converted Case 3 to Case 4.
          if w.right.color == BLACK:
            w.left.color = BLACK
            w.color = RED
            self.Right_Rotate(w)
            w = x.p.right
          
          # w's left child is BLACK and w's right child is RED (Case 4 in
          # CLRS). We can now perfectly "fix" the tree with a few re-colorings
          # and rotations. We set x equal to the root node to exit the loop
          w.color = x.p.color
          x.p.color = BLACK
          w.right.color = BLACK
          self.Left_Rotate(x.p)
          x = self.root
      
      # x is its parent's right child
      else: # x = x.p.right
        w = x.p.left
        
        # x is BLACK-BLACK and x's sibling w is RED (Case 1 in CLRS).
        # Now w must have BLACK children. We swap the colors of w and x's
        # parent, then do a right rotation on x's parent. At this point, x's
        # new sibling (which was one of w's children before the rotation) is
        # BLACK, so we have converted Case 1 into Case 2, 3, or 4.
        if w.color == RED:
          w.color = BLACK
          x.p.color = RED
          self.Right_Rotate(x.p)
          w = x.p.left
        
        # x is BLACK-BLACK, x's sibling w is BLACK, and both of w's children
        # are BLACK (Case 2 in CLRS). We remove one BLACK from w (making it
        # RED) and push one BLACK from x to its parent (making x BLACK and x.p
        # either RED-BLACK or BLACK-BLACK). We thus repeat the loop with
        # x = x.p
        if w.left.color == BLACK and w.right.color == BLACK:
          w.color = RED
          x = x.p
        
        # x is BLACK-BLACK, x's sibling w is BLACK, but one of w's children
        # is RED
        else:
          
          # w's right child is RED and w's left child is BLACK (Case 3 in
          # CLRS). We swap the color of w and w's right child, then perform a 
          # left rotation. Now x's new sibling (which was w's right child) is
          # BLACK and has a RED left child (which was originally w). We have
          # converted Case 3 to Case 4.
          if w.left.color == BLACK:
            w.right.color = BLACK
            w.color = RED
            self.Left_Rotate(w)
            w = x.p.left
          
          # w's right child is BLACK and w's left child is RED (Case 4 in
          # CLRS). We can now perfectly "fix" the tree with a few re-colorings
          # and rotations. We set x equal to the root node to exit the loop
          w.color = x.p.color
          x.p.color = BLACK
          w.left.color = BLACK
          self.Right_Rotate(x.p)
          x = self.root
    
    x.color = BLACK

class Retroactive_Priority_Queue:
  def __init__(self):
    pass

class Node:
  def __init__(self):
    pass

class Graph:
  def __init__(self):
    pass
