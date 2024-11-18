from editor import HtmlEditor

def user_input():
    editor = HtmlEditor()
    try:
        while True:
            command = input("Enter command: ").split()
            if command[0] == "exit":
                break
            response = editor.execute(command)
            if response:
                print(response)
    except KeyboardInterrupt:
        print("\nGoodbye!")
        
def auto_input():
    editor = HtmlEditor()
    command_list=[
        "read file/test.html",
        "insert li item0 item1 test-insert",
        "append lis item4 item3 test-append",
        "edit-id item2 item2.5",
        "edit-text item1 Item1-new-text",
        "delete last-updated",
        "undo",
        "redo",
        "save test.html",
        "init",
        "print-tree", 
    ]
    for command in command_list:
        response = editor.execute(command.split())
        if response:
            print(response)
             
if __name__ == "__main__":
    
    auto_input()
    
    # auto_input()
    
    # need_user_input=input("Do you want to input command manually? (y/n): ")
    # if need_user_input.lower()=='y':
    #     user_input()
