import os
import sys
import xml.etree.ElementTree as etree


class TreeBuilderWithComment(etree.TreeBuilder):
    """
    Class to parse comment nodes with ElementTree
    """
    def comment(self, data):
        self.start(etree.Comment, {})
        self.data(data)
        self.end(etree.Comment)


class CmdParam:
    """
    Class that represent a parameter with its type, XML node reference and default value
    """
    def __init__(self, type, node, default):
        self.type = type
        self.node = node
        self.default = default


class ONVIFMessage:
    """
    Class that represent an ONVIF message (SOAP)
    Attributes:
        name: Name of the command (String)
        params: Parameters of the command (Dictionary of CmdParam object)
    """
    def __init__(self, file):
        if not os.path.exists(file):
            sys.stderr.write("{} doesn't exist\n".format(file))
            return

        self.name = ''
        self.params = {}
        self.tree = etree.parse(file, parser=etree.XMLParser(target=TreeBuilderWithComment()))
        self._parse_message()

    def _guess_type(self, type_name):
        offset = type_name.find(' - ')
        return type_name[:offset] if offset != -1 else type_name

    def _search_params(self, node):
        if len(node.getchildren()) == 0:
            return

        # For all children node of 'node'
        for i in range(len(node)):
            self._search_params(node[i])

            if node[i].text is None:
                continue

            # If the node is a comment that indicate the type of the next node which is a parameter
            if node[i].text.startswith('type: '):
                param_name = node[i + 1].tag[node[i + 1].tag.find('}') + 1:]

                # Generate unique name
                while param_name in self.params:
                    number = 0
                    param_name = param_name + str(number)

                self.params[param_name] = CmdParam(self._guess_type(node[i].text[6:]), node[i + 1], node[i + 1].text)
            elif node[i].text.startswith('1 or more repetitions:'):
                pass
            elif node[i].text.startswith('Optional:'):
                pass
            elif node[i].text.startswith('You have a CHOICE of the next '):
                pass
            elif node[i].text.startswith('You may enter ANY elements at this point'):
                pass
            elif node[i].text.startswith('Zero or more repetitions:'):
                pass

    def _parse_message(self):
        root_node = self.tree.getroot()
        command_node = root_node.find('{http://www.w3.org/2003/05/soap-envelope}Body')[0]
        self.name = command_node.tag

        self._search_params(command_node)

    def get_message(self):
        """
        Return a string of XML representation of the SOAP message
        :return: String
        """
        return etree.tostring(self.tree.getroot(), encoding='ascii', method='xml')

    def get_all_params(self):
        """
        Return all available parameters
        :return: Array of string
        """
        return [k for k in self.params.keys()]

    def get_param(self, param):
        """
        Return the value of parameter
        :param param: Parameter name
        :return: Value of the parameter (string)
        """
        return self.params[param].node.text if param in self.params else ''

    def set_param(self, param, value):
        """
        Set parameter value
        :param param: Parameter name
        :param value: Value to set
        :return: None
        """
        if param not in self.params:
            return

        self.params[param].node.text = value
