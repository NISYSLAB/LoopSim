from bs4 import BeautifulSoup
import logging
import re

GRAPHML_FILE = "testhg.graphml"
TRIMMED_LOGS = True

# Output in a preferred format.
if TRIMMED_LOGS:
    logging.basicConfig(level=logging.INFO, format='%(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

f = open(GRAPHML_FILE, "r")
text_str = f.read()

soup = BeautifulSoup(text_str, 'xml')

edges_text = soup.find_all('edge')
nodes_text = soup.find_all('node')

# Store the edges and nodes in a dictionary
edges_dict = dict()
nodes_dict = dict()

for node in nodes_text:
    node_key = node.get_text()
    length = len(node.find_all('data'))
    for i in range(length):
        try:
            data = node.find_all('data')[i]
            node_label = data.find('y:NodeLabel').text
            nodes_dict[node['id']] = re.sub(r'(\s+|\n)', ' ', node_label)
        except IndexError:
            logging.debug('IndexError: A node with no valid properties encountered and ignored')
        except AttributeError:
            logging.debug('AttributeError: A node with no valid properties encountered and ignored')

for edge in edges_text:
    length = len(edge.find_all('data'))
    for i in range(length):
        try:
            data = edge.find_all('data')[i]
            edge_label = data.find('y:EdgeLabel').text
            if edges_dict.get(edge_label) != None:
                targets = edges_dict[edge_label][1]
            else:
                targets = []
            targets.append(nodes_dict[edge['target']])
            edges_dict[edge_label] = [nodes_dict[edge['source']], targets]
        except IndexError:
            logging.debug('An edge with no valid properties encountered and ignored')
        except AttributeError:
            logging.debug('AttributeError: An edge with no valid properties encountered and ignored')

# Print the edges_dict    
logging.info(edges_dict)
