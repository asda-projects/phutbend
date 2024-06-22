

text_test = "Catch you later!Howdy!OIEEEEE?So long!Whats up? Till we meet again!Nice to see you!"

def replaces( string_text: str):
    replacers = {
        "?": "? @ ",
        "!": "! @ ",
        ".": ". @ "
    }
    
    for (key, value) in replacers.items():
        
        string_text =  string_text.replace(key, value)

    return string_text

if __name__ == "__main__":

    a = replaces(text_test)
    print(a)