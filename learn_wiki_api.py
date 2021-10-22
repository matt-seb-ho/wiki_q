import wikipediaapi

# create wiki object
wiki = wikipediaapi.Wikipedia('en')

# get single WikipediaPage with its name
pypage_name = 'Python_(programming_language)'
page_py = wiki.page(pypage_name)

# page.exists()
print('does', pypage_name, 'exist:', end='')
print('yes' if page_py.exists() else 'no')

# basic page properties:
# - title
# - summary: text from top blurb in the article 
# - url: fullurl or canonicalurl
print('title:', page_py.title)
print('summary:', page_py.summary[0:100])

# get full text:
# - use .text property:
#   - string concatenating summary and sections with title and text
print('.text:', page_py.text[2000:2100])

# get page's categories
# - use .categories property:
#   - dictionary with category title (string), value (WikipediaPage)
print('number of categories:', len(page_py.categories))
# print('first 5 category titles:', list(page_py.categories)[0:5]);
# print('first category value:', list(page_py.categories.values())[0])

# get all pages from category
# - use page.categorymembers property
#   - I think this only works on WikipediaPage of the form "Category:XYZ"

# code from documentation
# you need to do de-duplication and recursion yourself
def print_categorymembers(categorymembers, level=0, max_level=1):
    for c in categorymembers.values(): # I guess categorymembers is a dict 
        print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            print_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)

# cat = wiki.page("Category:Physics")
# print(cat.fullurl)
# print("Cat members of 'Category:Physics'")
# print_categorymembers(cat.categorymembers)
