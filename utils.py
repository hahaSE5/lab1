from bs4 import BeautifulSoup, Tag

class HtmlElement:
    def __init__(self, tag_name, id=None, text=None):
        self.tag_name = tag_name
        if id:
            self.id = id
        else:
            self.id = tag_name
        self.text = text
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
    
    def remove_child(self, child_id):
        self.children = [child for child in self.children if child.id != child_id]
        
class HtmlDocument:
    def __init__(self):
        self.html = HtmlElement('html')
        self.head = HtmlElement('head')
        self.title = HtmlElement('title')
        self.body = HtmlElement('body')
        self.html.add_child(self.head)
        self.head.add_child(self.title)
        self.html.add_child(self.body)
        self.id_pool=[]
    
    def to_html(self,indent=2):
        def indent_html(element, level=0):
            lines = []
            indentation = " " * (level * indent)
            
            if element.tag_name:
                start_tag = f"{indentation}<{element.tag_name}"
                if element.id and element.id not in ["head","title","body","html"]:
                    start_tag += f' id="{element.id}"'
                start_tag += ">"
            else:
                start_tag = f"{indentation}"
            lines.append(start_tag)

            if element.text and element.text.strip():
                if not element.children:  # 如果没有子元素，则在同一行显示文本
                    lines[-1] += element.text.strip()
                else:  # 如果有子元素，则在下一行显示文本
                    lines.append(f"{indentation}  {element.text.strip()}")

            for child in element.children:
                lines.extend(indent_html(child, level + 1))

            end_tag = f"</{element.tag_name}>" if element.tag_name else ""
            if not element.children :  # 没有子元素且有文本时，结束标签在同一行
                lines[-1] += end_tag
            else:  # 其他情况，结束标签另起一行
                lines.append(f"{indentation}{end_tag}")

            return lines
        lines = indent_html(self.html)
        return "\n".join(lines)
    
    def from_html(self, html_str):
        soup = BeautifulSoup(html_str, 'html.parser')
        self.html = self._parse_element(soup.html)
    
    def _parse_element(self, soup_element):
        if isinstance(soup_element, Tag):
            element = HtmlElement(tag_name=soup_element.name, id=soup_element.get('id'), text=soup_element.string)
            for child in soup_element.contents:
                if isinstance(child, Tag):
                    element.add_child(self._parse_element(child))
                elif child.strip() and soup_element.name == 'div':
                    # 如果是文本节点且不是空白字符串，则创建一个文本元素
                    element.add_child(HtmlElement(tag_name=None,text=child.strip()))
            return element
        return None
    
    def find_element_by_id(self, id_value):
        def find_element(element):
            if element.id == id_value:
                return element
            for child in element.children:
                found = find_element(child)
                if found:
                    return found
            return None
        return find_element(self.html)
    
    def find_parent_by_id(self, id_value):
        def find_parent(element, parent=None):
            if element.id == id_value:
                return parent
            for child in element.children:
                found = find_parent(child, element)
                if found:
                    return found
            return None
        return find_parent(self.html)