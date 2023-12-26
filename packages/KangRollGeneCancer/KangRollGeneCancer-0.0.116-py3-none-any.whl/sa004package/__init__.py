import sys, os
current_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.isdir(os.path.join(current_dir, 'pytransform')):
    sys.path.append(current_dir)
