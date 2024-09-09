from pyvis.network import Network

# Create a network
net = Network()

# Add nodes and edges
net.add_node(1, label='Node 1')
net.add_node(2, label='Node 2')
net.add_edge(1, 2)

# Set font options
options = """
var options = {
  "nodes": {
    "font": {
      "size": 20,
      "face": "Arial",
      "color": "red"
    }
  }
}
"""
net.set_options(options)

# Write HTML file
output_html_file = "example.html"
net.write_html(output_html_file)
