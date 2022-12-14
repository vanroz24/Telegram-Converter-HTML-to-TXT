from html.parser import HTMLParser
from collections import deque

class TGParser(HTMLParser):
    is_from_name = False
    is_text = False
    is_time = False
    is_body_details = False
    name = ''
    text = ''
    time = ''
    # Body details usually contains the date
    body_details = ''
    # Counter to check if the message has ended. 2 divs signal the end
    div_count = 0
    # Storing dictionaries (name: 'user_name', text: 'user_text')
    chat_text = deque()

    def handle_starttag(self, tag, attrs):
        # print("DEBUG: starttag: ", tag)
        if tag == 'div':
            self.div_count = 0
        
        for attr in attrs:
            if attr[1] == 'from_name':
                self.is_from_name = True
            if attr[1] == 'pull_right date details':
                self.is_time = True
            if attr[1] == 'text':
                self.is_text = True
            if attr[1] == 'body details':
                self.is_body_details = True

    def handle_endtag(self, tag):
        # print("DEBUG: endtag: ", tag)        
        if self.is_text == True and tag == "div":
            self.div_count += 1
            # When the message has ended - append dictionary (name, text) to the chat_text deque
            if self.div_count > 1:
                if self.body_details != '':
                    self.chat_text.append(dict(name = self.body_details + "$date$" + self.name, text = self.text))
                    self.body_details = ''
                else:
                    self.chat_text.append(dict(name = self.name, text = self.text))
                self.div_count = 0
                self.is_text = False
                self.text = ''

    def handle_data(self, data):
        # print("DEBUG: data: ", data)
        if self.is_body_details == True:
            self.body_details = data.strip()
            self.is_body_details = False        
        if self.is_from_name == True:
            self.name = data.strip()
            self.is_from_name = False
        if self.is_time == True:
            self.time = data.strip()
            self.is_time = False
        if self.is_text == True:
            if self.time == '':
                self.text = self.text.strip() + " " + data.strip()
            else:
                self.text = self.text + self.time.strip() + ": " + data.strip()
                self.is_time = False
                self.time = ''

    def print_chat_text(self):
        for text in self.chat_text:
                for key, value in text.items():
                    if key == 'name':
                        if '$date$' in value:
                            temp_text = value.split('$date$')
                            print("===== " + temp_text[0] + " =====\n\n=== " + temp_text[1] + " ===\n")
                        else:
                            print("=== " + value + " ===\n")
                    if key == 'text':
                        print(value + "\n\n")

    def save_chat_text(self, filename="messages"):
        with open("Output/" + filename.replace(".html", "") + ".txt", "w", encoding='utf-8') as f:
            for text in self.chat_text:
                for key, value in text.items():
                    if key == 'name':
                        if '$date$' in value:
                            temp_text = value.split('$date$')
                            f.write("===== " + temp_text[0] + " =====\n\n=== " + temp_text[1] + " ===\n")
                        else:
                            f.write("=== " + value + " ===\n")
                    if key == 'text':
                        f.write(value + "\n\n")
        f.close()