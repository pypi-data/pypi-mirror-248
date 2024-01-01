import numpy as np

class TreeNode:

    def __init__(self, feature=None, value=None, result=None, left=None, right=None):
        self.feature = feature  # Fitur pemisah
        self.value = value      # Nilai pemisah
        self.result = result    # Hasil jika node ini adalah leaf node
        self.left = left        # Sub-tree kiri (nilai kurang dari atau sama dengan pemisah)
        self.right = right      # Sub-tree kanan (nilai lebih dari pemisah)
    
    