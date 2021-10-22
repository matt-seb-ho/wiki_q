import wikipediaapi
import json
from tqdm import tqdm

wiki = wikipediaapi.Wikipedia('en')
causal_words = ['because', 'thus', 'as a result of', 'due to']

catname = 'Category:Earth_phenomena'
cat = wiki.page(catname)

def get_category_members(category):
    return [c.title
        for c in category.categorymembers.values() 
            if c.ns != wikipediaapi.Namespace.CATEGORY]

def has_causal_word(sentence):
    for word in causal_words:
        if (' ' + word + ' ') in sentence:
            return True
    return False

def add_causal_sentences(name, page_to_sentence, add_context=False, count=[0]):
    page = wiki.page(name)
    sentences = page.text.split('.')
    # print('source sentences:', len(sentences))
    if len(sentences) == 0:
        return

    page_sentences = []
    # if add_context is true, include the previous sentence as context
    if add_context:
        page_sentences = [sentences[i - 1] + '. ' + sentences[i]
            for i in range(1, len(sentences))
                if has_causal_word(sentences[i])]
        if has_causal_word(sentences[0]):
            page_sentences.append(sentences[0])
    else:
        page_sentences = [sentence for sentence in sentences if has_causal_word(sentence)]

    # print('causal_sentences:', len(page_sentences))
    if len(page_sentences):
        count[0] += len(page_sentences)
        page_to_sentence[name] = page_sentences

def causal_sentences_from_category(catname, add_context=False):
    res = {}
    cat = wiki.page(catname)
    pages = get_category_members(cat)
    print('Reading', len(pages), 'articles')
    count = [0]
    for i in tqdm(range(len(pages))):
        add_causal_sentences(pages[i], res, add_context, count)
    print('Gathered', count[0], 'sentences')
    return res

csentences = causal_sentences_from_category(catname, add_context=False)
json_f = json.dumps(csentences, indent=2)
fname = 'res.json'
f = open(fname, 'w')
f.write(json_f)
f.close()

print('Successfully written to', fname)
