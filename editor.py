from spellchecker import SpellChecker
import re

from utils import HtmlDocument, HtmlElement


class HtmlEditor:
    def __init__(self):
        self.document = None
        self.history = []
        self.redo_stack = []
        self.bin = []
        self.command_dict = {
            "insert": self.insert,
            "append": self.append,
            "edit-id": self.edit_id,
            "edit-text": self.edit_text,
            "delete": self.delete,
            "undo": self.undo,
            "redo": self.redo,
            "print-indent": self.print_indent,
            "print-tree": self.print_tree,
            "spell-check": self.spell_check,
            "read": self.read,
            "save": self.save,
            "init": self.init,
        }

    def execute(self, command):
        if command[0] not in self.command_dict:
            return "Unknown command"
        elif command[0] != "init" and command[0] != "read" and self.document is None:
            return "No document found"
        else:
            try:
                method = self.command_dict[command[0]]
                result = method(*command[1:])
                self.history.append(command)
                if command[0] in ["insert", "append", "edit-id", "edit-text", "delete"]:
                    self.redo_stack = ["edit"]
                elif command[0] in ["save", "init", "read"]:
                    self.redo_stack = ["io"]
                elif command[0] in ["print-indent", "print-tree", "spell-check"]:
                    self.redo_stack = ["print"]
                return result
            except Exception as e:
                return str(e)

    def insert(
        self,
        tag_name: str,
        id_value: str,
        insert_location: str,
        text_content: str = None,
    ):
        if id_value in self.document.id_pool:
            raise ValueError("ID already exists")
        location_element = self.document.find_element_by_id(insert_location)
        if not location_element:
            raise ValueError("Insert location not found")
        new_element = HtmlElement(tag_name, id_value, text_content)
        location_element_parent = self.document.find_parent_by_id(insert_location)
        location_element_parent.children.insert(
            location_element_parent.children.index(location_element), new_element
        )
        self.document.id_pool.append(id_value)

    def append(
        self,
        tag_name: str,
        id_value: str,
        parent_element: str,
        text_content: str = None,
    ):
        parent = self.document.find_element_by_id(parent_element)
        if not parent:
            raise ValueError("Append location not found")
        if id in self.document.id_pool:
            raise ValueError("ID already exists")
        new_element = HtmlElement(tag_name, id_value, text_content)
        parent.add_child(new_element)

    def edit_id(self, old_id, new_id):
        element = self.document.find_element_by_id(old_id)
        if not element:
            raise ValueError("Element not found")
        element.id = new_id

    def edit_text(self, element_id, new_text_content=None):
        element = self.document.find_element_by_id(element_id)
        if not element:
            raise ValueError("Element not found")
        element.text = new_text_content

    def delete(self, element_id):
        element = self.document.find_element_by_id(element_id)
        if not element:
            raise ValueError("Element not found")
        parent = self.document.find_parent_by_id(element_id)
        self.bin.append((parent.id, element, parent.children.index(element)))
        parent.children.remove(element)

    def undo(self):
        if self.history:
            last_command = self.history.pop()
            if last_command[0] in ["print-indent", "print-tree", "spell-check"]:
                raise ValueError("Pass undo printing")
            elif last_command[0] in ["save", "init", "read"]:
                raise ValueError("Cannot undo I/O operation")
            else:
                self.redo_stack.append(last_command)
                if last_command[0] == "insert":
                    self.delete(last_command[2])
                elif last_command[0] == "append":
                    self.delete(last_command[2])
                elif last_command[0] == "delete":
                    (
                        recover_element_parent_id,
                        recover_element,
                        recover_element_index,
                    ) = self.bin.pop()
                    recover_element_parent = self.document.find_element_by_id(
                        recover_element_parent_id
                    )
                    recover_element_parent.children.insert(
                        recover_element_index, recover_element
                    )
                elif last_command[0] == "edit-id":
                    self.edit_id(last_command[2], last_command[1])
                elif last_command[0] == "edit-text":
                    self.edit_text(last_command[1], last_command[2])
        else:
            raise ValueError("No command to undo")

    def redo(self):
        if self.redo_stack and self.redo_stack[-1] == "edit":
            self.redo_stack.pop()
            raise ValueError("Cannot redo after editing")
        elif self.redo_stack and self.redo_stack[-1] == "io":
            self.redo_stack.pop()
            raise ValueError("Cannot redo after I/O operation")
        elif self.redo_stack and self.redo_stack[-1] == "print":
            self.redo_stack.pop()
            raise ValueError("Pass redo printing")
        elif self.redo_stack:
            next_command = self.redo_stack.pop()
            self.execute(next_command)
        else:
            raise ValueError("No command to redo")

    def print_indent(self):
        indent_html = self.document.to_html()
        print(indent_html)

    def print_tree(self):
        def print_tree_recursively(element, level=0, is_last=False, prefix=""):
            connector = "└── " if is_last else "├── "
            if element.id and element.id not in ["head", "title", "body", "html"]:
                print(f"{prefix}{connector}{element.tag_name}#{element.id}")
            elif element.tag_name:
                print(f"{prefix}{connector}{element.tag_name}")
            elif element.text:
                print(f"{prefix}{connector}{element.text}")

            if element.tag_name and element.text:
                text_prefix = f"{prefix}    " if is_last else f"{prefix}│   "
                print(f"{text_prefix}└── {element.text}")

            children_count = len(element.children)
            for index, child in enumerate(element.children):
                new_prefix = f"{prefix}    " if is_last else f"{prefix}│   "
                print_tree_recursively(
                    child, level + 1, index == children_count - 1, new_prefix
                )

        print_tree_recursively(self.document.html)

    def spell_check(self):
        spell = SpellChecker(language="en")

        def check_text(element):
            if element.text:
                if not re.search(r"\b\d{4}-\d{2}-\d{2}\b|©", element.text):
                    words = re.findall(r"\b\w+\b", element.text)
                    misspelled = spell.unknown(words)
                    if misspelled:
                        print(f"Error in element: {element.tag_name}#{element.id}")
                        for error_word in misspelled:
                            print(
                                f"    Misspelled word: {error_word}. Did you mean: {spell.correction(error_word)}?"
                            )
            for child in element.children:
                check_text(child)

        check_text(self.document.html)

    def read(self, filepath):
        self.document = HtmlDocument()
        with open(filepath, "r") as file:
            self.document.from_html(file.read().strip())

    def save(self, filepath):
        with open(filepath, "w") as file:
            file.write(self.document.to_html())

    def init(self):
        self.document = HtmlDocument()
