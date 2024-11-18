from editor import HtmlEditor;
import unittest;
command_list=[
        "read file/test.html",
        "insert li item0 item1 test-insert",
        "append li item4 item3 test-append",
        "edit-id item2 item2.5",
        "edit-text item1 Item1-new-text",
        "delete last-updated",
        "undo",
        "redo",
        "save test.html",
        "init",
        "print-tree", 
    ]
command_insert=["read file/test.html",
        "insert li item0 item1 test-insert",
        "save test-insert.html"]
command_append=["read file/test.html",
        "append li item4 item3 test-append",
        "save test-append.html"]
command_edit_id=["read file/test.html",
        "edit-id item2 item2.5",
        "save test-id.html"]
command_edit_text=["read file/test.html",
        "edit-text item1 Item1-new-text",
        "save test-edit-text.html"]
command_delete=["read file/test.html",
        "delete last-updated",
        "save test-delete.html"]
def execute_command(editor,command):
     for command in command_list:
        response = editor.execute(command.split())
def read_html_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
def compareHtmlequal(html_1,html_2):
    file1_path='file/'+html_1;
    file2_path='file/'+html_2;
    content1 = read_html_file(file1_path)
    content2 = read_html_file(file2_path)
    #self.assertEqual(content1, content2", "Files are not identical.")
    return;
class EditorTestCase(unittest.TestCase):
    def setUp(self):
       self.HtmlEditor=HtmlEditor()
    def test_insert(self):
        #execute_command(self.editor,command_insert)
        #compareHtmlequal("test2.html","test-insert.html")
        return;
    def test_append(self):
        #execute_command(self.editor,command_append)
        #compareHtmlequal("test3.html","test-append.html")
        return;
    def test_edit_id(self):
        #execute_command(self.editor,command_edit_id)
        #compareHtmlequal("test4.html","test-id.html")
        return;
    def test_edit_text(self):
        #self.HtmlEditor.execute(coomand_edit_text)
        #compareHtmlequal("test5.html","test-text.html")
        return;
    def test_delete(self):
        #self.HtmlEditor.execute(coomand_delete)
        #compareHtmlequal("test6.html","test-delete.html")
        return;
if __name__ == '__main__':
    unittest.main()
