#!/usr/bin/python
import os
from markdown import markdown

DOCS = "/Users/brennannovak/MailPileCode/doc/"
if not os.path.exists(DOCS):
    DOCS = '../../Mailpile/doc/'
    if not os.path.exists(DOCS):
        raise ValueError('Could not find wiki')

FAQS = [
    ('about',
     'What is Mailpile?',
     'FAQ-What-Is-Mailpile.md'),
    ('basic',
     'Basic Questions?',
     'FAQ---Basic-Questions.md'),
    ('look',
     'Branding and Design',
     'FAQ-Branding-&-Design.md'),
    ('usability',
     'Interface and Usability Design',
     'FAQ-Interface-&-Usability-Design.md'),
    ('crypto',
     'Encryption and Security',
     'FAQ-Encryption-&-Security.md'),
    ('tech',
     'Technical Questions',
     'FAQ-Technical-Questions---Not-Encryption.md'),
    ('dev',
     'Contributing, Helping, Developing',
     'FAQ-Contributing,-Helping,-Developing.md'),
    ('wishlist',
     'Feature Requests',
     'FAQ-Feature-Requests.md'),
    ('misc',
     'Miscellanious Questions',
     'FAQ-Random-Questions.md'),
]

toc = []
answers = []
for section, title, fn in FAQS:
    data = open(os.path.join(DOCS, fn)).read()

    # Initialize the table-of-contents for this section
    toc.append('<li><a href="#%s">%s</a><ul>' % (section, title))

    # Markdown helpfully puts each paragraph/heading on a new line, so we can
    # just iterate through the lines and edit/insert things we need.
    marked = []
    q_count = 1
    for line in markdown(data).splitlines():
        if '<h3>' in line:
            question_toc = line.replace('<h3>', '').replace('</h3>', '')            
            qid = '%s-%s' % (section, q_count)
            toc.append('<li class="section-%s"><a href="#%s">%s</a></li>' % (section, qid, question_toc))

            if q_count > 1:
                marked.append('</li>')
                
            # 
            question = line.replace('<h3>', '<h3 class="faq-title">')
            marked.append('<li class="faq-item" id="%s"> %s <span class="faq-section">%s</span>' % (qid, question, section))
            q_count += 1
        else:
            marked.append(line)

    if q_count > 1:
        marked.append('</li>')

    toc.append('</ul></li>')
    answers.extend(['<li class="faq-section-title" id="%s"><h2>%s</h2></li>' % (section, title)] + marked)

print 'Subject: Frequently Asked Questions'
print 'Format: html'
print 
print '<div id="faq">'
print open('faq.md').read()
print '<div id="toc">'
print '<ul>%s</ul></div>' % '\n'.join(toc)
print '<ul class="list">%s</ul>' % '\n'.join(answers)
print '</div>'
print open('features.md').read()