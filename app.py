from flask import Flask, render_template
from form import Searching
from operations import search
from inverted_index import make_inverted_index
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
CURRENT_DIR = os.getcwd()

@app.route('/', methods=['GET', 'POST'])
def index():
    titles= None
    startings= None
    documents=None
    no_result = False
    
    # making the inverted_index
    inverted_index = make_inverted_index()
    form = Searching()

    if form.validate_on_submit():
        titles={}
        startings={}

        query = form.searched.data.lower().strip().split(' ')
        form.searched.data = ''

        # processing user query
        documents=search(query, inverted_index)


        # for displaying documents on the front-page
        if documents == []:
            no_result = True
        else:
            for doc in documents:
                
                # Opening and Reading the short stories
                file_name=CURRENT_DIR + '\ShortStories\\' + str(doc) + '.txt'
                f=open(file_name, "r", encoding='UTF8')
                file_lines=f.readlines()

                count=0
                starting = ''

                for line in file_lines:
                    if count == 0:
                        title=line.strip()
                        titles[doc]=title
                    else:
                        if line.strip() != '':
                            starting=starting + " " + line.strip()
                    count=count + 1
                    if count == 7:
                        break
                startings[doc]=starting
                f.close()

    return render_template('home.html', form=form, documents=documents, titles = titles, startings = startings, no_result = no_result)

@app.route('/story/<docID>', methods=['GET', 'POST'])
def stories(docID):
    file = "./Stories/" + docID + ".html"
    return render_template(file)

if __name__ == '__main__':
    app.run(debug=True)
