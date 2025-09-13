# Run this script with: python hybrid_model_architecture.py

from graphviz import Digraph

dot = Digraph(comment='Hybrid Chess Engine Architecture', format='png')

# Nodes
dot.node('A', 'Chess Board\n(Position/FEN)')
dot.node('B', 'Feature Extraction\n(Board Encoding)')
dot.node('C', 'Neural Network\n(Model)')
dot.node('D', 'Stockfish\n(Traditional Engine)')
dot.node('E', 'Move Selection\n(Hybrid Logic)')
dot.node('F', 'Game Output\n(Best Move)')

# Edges
dot.edge('A', 'B', label='Extract Features')
dot.edge('B', 'C', label='NN Evaluation')
dot.edge('A', 'D', label='Stockfish Evaluation')
dot.edge('C', 'E', label='NN Move Score')
dot.edge('D', 'E', label='Stockfish Move Score')
dot.edge('E', 'F', label='Select Best Move')

# Render diagram to file
dot.render('hybrid_chess_engine_architecture', view=True)

print("Architecture diagram generated as 'hybrid_chess_engine_architecture.png'.")

# Architecture Diagram (Text Version)

"""
Chess Board (Position/FEN)
           |
           v
Feature Extraction (Board Encoding)
           |
           v
   Neural Network (Model)      Stockfish (Traditional Engine)
           |                           |
           v                           v
         Move Selection (Hybrid Logic)
                   |
                   v
         Game Output (Best Move)
"""
