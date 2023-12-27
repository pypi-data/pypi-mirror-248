from langchain.text_splitter import RecursiveCharacterTextSplitter
from urllib.parse import urlparse
import os
import nltk
nltk.download('punkt')
from urllib.request import urlopen, Request
from PyPDF2 import PdfWriter, PdfReader
import io
import requests
import fitz

def extract_text(url_link):
    response = requests.get(url=url_link, timeout=120, verify=False)
    pdf_io_bytes = io.BytesIO(response.content)
    pdf = PdfReader(pdf_io_bytes)
    text = " ".join(page.extract_text() for page in pdf.pages)

    # Initialize the text splitter with custom parameters
    custom_text_splitter = RecursiveCharacterTextSplitter(
        # Set custom chunk size
        chunk_size = 300,
        chunk_overlap  = 30,
        # Use length of the text as the size measure
        length_function = len,
        # Use only "\n\n" as the separator
        separators = ['\n']
    )

    custom_texts = custom_text_splitter.create_documents([text])

    pypdf_list = []
    for i in range(len(custom_texts)):
        custom_text_all = custom_texts[i].page_content
        pypdf_list.append(custom_text_all)
    return pypdf_list

# ------------------------------------------------------------------------------------------
# extract text from pdf using pymu
def extract_text_2(url_link):
    response = requests.get(url_link)
    pdf_data = io.BytesIO(response.content)
    doc = fitz.open("pdf", pdf_data)
    
    for page in doc:
        text = page.get_text()
        output = page.get_text('blocks')
        pymu_list = []
        for page in doc:
            output = page.get_text("blocks")                   
            previous_block_id = 0 # Set a variable to mark the block id
            for block in output:
                # print(block[4])
                # print('++')
                if block[6] == 0: # We only take the text
                    if previous_block_id != block[5]: # Compare the block number 
                        pymu_list.append(block[4])
    return pymu_list

# ------------------------------------------------------------------------------------------
# preprocessing text from pdf by P'Kaew's function
def clean_txt(text_list):
    list_clean = []

    # clean data in pypdf_list
    for i in range(len(text_list)):
        list_clean.append(_clean_missing_1(text_list[i]))

    df_clean = pd.DataFrame({"text": list_clean})
    return df_clean

# ------------------------------------------------------------------------------------------
# collect data
def create_table(url_linkk, num_id):
    ct_texts = extract_text(url_linkk)
    # ct_text_list = extract_text_2(url_linkk)
    df_clean = clean_txt(ct_texts)
    db_name_lst = []
    table_name_lst = []
    issue_date_lst = []
    expiration_date_lst = []
    file_name_lst = []
    document_id_lst = []
    url_lst = []
    domain_lst = []
    source_type_lst = []
    lang_lst = []
    category_1_lst = []
    category_2_lst = []
    title_lst = []
    description_lst = []
    section_lst = []
    par_lst = []
    updated_date_lst = []

    for i in range(len(df_clean)):
        db_name_lst.append('llm_ivx')
        table_name_lst.append('llm_ivx_pdf')
        issue_date_lst.append('null')
        expiration_date_lst.append('null')
        
        url_lst.append(url_linkk) # this

        a = urlparse(url_lst[0])
        file_name_lst.append(os.path.basename(a.path))

        # domain_lst.append('null')
        source_type_lst.append('pdf')
        lang_lst.append('th')
        category_1_lst.append('null')
        category_2_lst.append('null')
        title_lst.append('null')
        description_lst.append('null')
        section_lst.append('null')
        updated_date_lst.append('null')

    df_clean['db_name'] = db_name_lst
    df_clean['table_name'] = table_name_lst
    df_clean['issue_date'] = issue_date_lst
    df_clean['expiration_date'] = expiration_date_lst
    df_clean['file_name'] = file_name_lst
    df_clean['url'] = url_lst
    df_clean['source_type'] = source_type_lst
    df_clean['lang'] = lang_lst
    df_clean['category_1'] = category_1_lst
    df_clean['category_2'] = category_2_lst
    df_clean['title'] = title_lst
    df_clean['description'] = description_lst
    df_clean['section'] = section_lst
    df_clean['updated_date'] = updated_date_lst

    for k in range(len(df_clean)):
        document_id_lst.append(file_name_lst.index(df_clean['file_name'].values[0]) + num_id) # this
    df_clean['document_id'] = document_id_lst

    res = df_clean.reset_index().groupby('document_id').agg(lambda x: x.nunique())
    for j in range(res['index'].values[0]):
        num_str = str(j+1)
        par_num = 'par' + num_str
        par_lst.append(par_num)
    df_clean['paragraph/chunk'] = par_lst

    domain = urlparse(url_lst[0]).netloc
    df_clean['domain'] = domain

    new_cols = ['db_name', 'table_name', 'issue_date', 'expiration_date', 'file_name', 'document_id', 'url','domain', 'source_type', 'lang', 'category_1', 'category_2', 'title', 'description', 'section', 'paragraph/chunk', 'text', 'updated_date']

    df_clean = df_clean[new_cols]
    return df_clean