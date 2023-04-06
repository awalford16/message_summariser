from gmail import Gmail
from ai import OpenAI

if __name__ == '__main__':
    gmail = Gmail()
    ai = OpenAI()

    # Morning Brew summariser
    source = "Morning Brew"
    gmail.read_mail_label(source)
    
    print("SPORTS: ", ai.summarize(source, "SPORTS"))
