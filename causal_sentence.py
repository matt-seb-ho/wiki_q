import wikipediaapi
import json
from enum import Enum
from tqdm import tqdm


wiki = wikipediaapi.Wikipedia('en')

class CausalOrder(Enum):
    PRECEDING = 1     # x [word] y, x causes y
    SUCCEEDING = 2    # x [word] y, y causes x
causal_words = {
    'because': CausalOrder.PRECEDING,
    'due to': CausalOrder.PRECEDING,
    'thus': CausalOrder.SUCCEEDING,
    'therefore': CausalOrder.SUCCEEDING,
    'causes': CausalOrder.SUCCEEDING,
}

catname = 'Category:Earth_phenomena'
cat = wiki.page(catname)

def get_category_members(category):
    return [c.title
        for c in category.categorymembers.values() 
            if c.ns != wikipediaapi.Namespace.CATEGORY]

def has_causal_word(sentence):
    for word in causal_words.keys():
        if (' ' + word + ' ') in sentence:
            return True, word
    return False, ''

def add_causal_sentences(name, page_to_sentence, add_context=False, count=[0]):
    page = wiki.page(name)
    sentences = page.text.split('.')
    # print('source sentences:', len(sentences))
    if len(sentences) == 0:
        return

    # last "sentence" is blank context for first sentence
    sentences.append('');
    page_sentences = []
    for i in range(len(sentences) - 1):
        has_word, word = has_causal_word(sentences[i])
        if has_word and add_context:
            page_sentences.append({
                'context': sentences[i - 1],
                'sentence': sentences[i],
                'keyword': word})
        elif has_word:
            page_sentences.append({
                'sentence': sentences[i],
                'keyword': word})

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
    res['Sentence Count'] = count[0]
    return res

def generate_question(entry):
    words = entry['sentence'].split(' ')
    keyword_index = words.index(entry['keyword'].split(' ')[0])
    causal_order = causal_words[entry['keyword']];
    if causal_order == CausalOrder.SUCCEEDING:
        before = ' '.join(words[:keyword_index])
        return 'why does ' + before + '?'
    else:
        after = ' '.join(words[keyword_index + len(entry['keyword'].split(' ')):])
        return 'why does ' + after + '?'

fname = 'res.json'
csentences = {}

WRITE_TO_JSON = False
if WRITE_TO_JSON:
    csentences = causal_sentences_from_category(catname, add_context=True)
    json_f = json.dumps(csentences, indent=2)
    f = open(fname, 'w')
    f.write(json_f)
    f.close()
    print('Successfully written to', fname)
else:
    f = open(fname)
    csentences = json.load(f)
    f.close()
    print('Successfully read from', fname)

# print(generate_question(csentences['Air shower (physics)'][0]))

counter = 0
limit = 20
for pagename in csentences:
    for sentence in csentences[pagename]:
        print(generate_question(sentence))
        counter += 1
    if counter > limit:
        break        
