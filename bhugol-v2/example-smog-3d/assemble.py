import os
H=os.path.dirname(os.path.abspath(__file__))
h=open(H+'/head.html').read().replace('float m = (mv > 15.0 && idx <= lit && idx < 7.5) ? 1.0 : 0.0;','float m = (mv > 15.0 && ((idx <= lit && idx < 7.5) || (idx > 7.5 && lit >= 3.0))) ? 1.0 : 0.0;')
open(H+'/template.html','w').write(h+''+open(H+'/body.js').read()+'\n'+open(H+'/build.js').read()+open(H+'/tpl_tail.txt').read())
