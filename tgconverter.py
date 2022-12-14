from tgparser import TGParser
import help
import sys
import os

if __name__ == "__main__":
    argv_length = len(sys.argv)

    if '-h' in sys.argv:
        help.print_help()
    else:
        directory = 'Input'
        html_exists = False
        for file in os.listdir(directory):
            if ".html" in file:
                    html_exists = True
                    parser = TGParser()
                    with open(directory + '/' + file, "r", encoding='utf-8') as f:
                        text = f.read()
                        parser.feed(text)
                        if "-p" in sys.argv:
                            parser.print_chat_text()
                        else:
                            parser.save_chat_text(filename=file)
                    f.close()    
        if not html_exists:
            print()
            print("===================================================================")
            print("You didn't input anything.")
            print()
            print('"-h" for help')
            print("===================================================================")
            print()