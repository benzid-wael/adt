from graphviz import Digraph
from graphviz import Graph


class Visualizer:

    factory_class = Graph
    default_format = 'png'

    @classmethod
    def from_data(cls, data):
        graph = cls.factory_class()
        for node in data.nodes():
            graph.node(node.id, label=str(node))
        for (parent, child) in data.edges():
            graph.edge(parent.id, child.id)
        return graph

    @classmethod
    def render(cls, graph: Graph, filename=None, directory=None, format=None):
        format = format or cls.default_format
        graph.render(filename, directory, format=format)


class DigraphVisualizer(Visualizer):
    factory_class = Digraph
