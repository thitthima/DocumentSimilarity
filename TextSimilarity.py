import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from tkinter import *
   
# import filedialog module 
from tkinter import filedialog 
# Create the root window 
window = Tk() 

# Function for opening the  
# file explorer window 
def browseFiles(): 
    global filename
    window.filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File", 
                                          filetypes = (("Text files", 
                                                        "*.txt*"), 
                                                       ("all files", 
                                                        "*.*"))) 
    filename=window.filename
       
    # Change label contents 
    label_file_explorer.configure(text="File Opened: "+filename) 
    return (filename)

def browseFiles2(): 
    global filename2
    window.filename2 = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File", 
                                          filetypes = (("Text files", 
                                                        "*.txt*"), 
                                                       ("all files", 
                                                        "*.*"))) 
    filename2=window.filename2
    
       
    # Change label contents 
    label_file_explorer2.configure(text="File Opened: "+filename2)        
    return (filename2)

def similar():
    global percentage_of_similarity
    #File 1
    file_docs = []
    # file1=input("Enter the file:")
    f = open(filename, "r").read()
    print(f)
    tokens = sent_tokenize(f)
    print(tokens)
    for line in tokens:
        file_docs.append(line)
    gen_docs = [[w.lower() for w in word_tokenize(text)] 
                for text in file_docs]
    from gensim import corpora
    dictionary = corpora.Dictionary(gen_docs)
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    import numpy as np
    from gensim.models import TfidfModel
    tf_idf = TfidfModel(corpus)
    from gensim.similarities import Similarity
        # building the index
    sims = Similarity(r'C:/Users/User/OneDrive/Desktop/UTeM/Sem5/NLP/Project/Real code',tf_idf[corpus],  #path based on your text file 
                                            num_features=len(dictionary))
    
    #File 2
    file2_docs = []
    # file2 =input("Enter the second file:")

    d = open(filename2, "r").read()
    print(d)    
    tokens2 = sent_tokenize(d)
    for line in tokens2:
        file2_docs.append(line)
    avg_sims = [] # array of averages
    
    # for line in query documents
    for line in file2_docs:
        # tokenize words
        query_doc = [w.lower() for w in word_tokenize(line)]
        # create bag of words
        query_doc_bow = dictionary.doc2bow(query_doc)
        # find similarity for each document
        query_doc_tf_idf = tf_idf[query_doc_bow]
        # print (document_number, document_similarity)
        print('Comparing Result:', sims[query_doc_tf_idf]) 
        # calculate sum of similarities for each query doc
        sum_of_sims =(np.sum(sims[query_doc_tf_idf], dtype=np.float32))
        # calculate average of similarity for each query doc
        avg = sum_of_sims / len(file_docs)
        # print average of similarity for each query doc
        print(f'avg: {sum_of_sims / len(file_docs)}')
        # add average values into array
        avg_sims.append(avg)  
    # calculate total average
    total_avg = np.sum(avg_sims, dtype=np.float)
    # round the value and multiply by 100 to format it as percentage
    percentage_of_similarity = round(float(total_avg) * 100)
    # if percentage is greater than 100
    # that means documents are almost same
    if percentage_of_similarity >= 100:
        percentage_of_similarity = 100
    # =============================================================================
    print("Percentage of similarity is ",percentage_of_similarity)  
    # =============================================================================
    label_percentage.configure(text="Similarity Percentage: "+ str(percentage_of_similarity))
   

def printt():
    return(percentage_of_similarity)       
                                                                                                   

   
# Set window title 
window.title('Text Similarity') 
lable_0 = Label(window,text="Welcome to Text Similarity", width=20,font=("bold",20))
lable_0.pack()
   
# Set window size 
window.geometry("700x500") 
   
#Set window background color 
window.config(background = "light blue") 
   
# Create a File Explorer label 
label_file_explorer = Label(window,  
                            text = "First Text File", 
                            width = 100, height = 4,  
                            fg = "blue") 
   
       
button_explore = Button(window,  
                        text = "Browse File", 
                        command = browseFiles)  

label_file_explorer2 = Label(window,  
                            text = "Second  Text File", 
                            width = 100, height = 4,  
                            fg = "blue") 

button_explore2 = Button(window,  
                        text = "Browse File", 
                        command = browseFiles2)  


button_submit = Button(window, text="Submit" , command=similar)

label_percentage = Label(window,  
                            text = "Similarity Percentage ", 
                            width = 100, height = 4,  
                            fg = "blue") 


# Grid method is chosen for placing 
# the widgets at respective positions  
# specifying rows and columns 
label_file_explorer.pack()
button_explore.pack()
label_file_explorer2.pack()
button_explore2.pack()
button_submit.pack()  
label_percentage.pack()  

# Let the window wait for any events 
window.mainloop() 
