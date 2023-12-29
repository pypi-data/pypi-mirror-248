// {% raw %}
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    macros: {
      st:	'\\mid',
      dv:	'\\nabla\\cdot',
      curl:	'\\nabla\\times',
      defeq:	'\\stackrel{\\text{def}}{=}',

      leq:	  '\\leqslant',
      geq:	  '\\geqslant',
      subset: '\\subseteq',
      supset: '\\supseteq',

      P:    '\\mathbf{P}',
      E:    '\\mathbf{E}',
      R:	'\\mathbb{R}',
      C:	'\\mathbb{C}',
      N:	'\\mathbb{N}',
      Z:	'\\mathbb{Z}',
      Q:	'\\mathbb{Q}',
      T:	'\\mathbb{T}',

      lap:	'\\Delta',
      grad:	'\\nabla',

      'var':	'\\operatorname{Var}',
      rank:	'\\operatorname{rank}',
      Span:	'\\operatorname{span}',
      Ad:	'\\operatorname{adj}',
      'trace':	'\\operatorname{tr}',
      erf:	'\\operatorname{erf}',
      sign:	'\\operatorname{sign}',

      abs:	  [ '#1\\lvert#2#1\\rvert', 2, '' ],
      norm:	  [ '#1\\lVert#2#1\\rVert', 2, '' ],
      set:	  [ '#1\\{ #2 #1\\}', 2, '' ],
      paren:  [ '#1(#2#1)', 2, '' ],
      brak:   [ '#1[#2#1]', 2, '' ]
      // IE+compat doesn't like commas after the last item.
    }
  },
  svg: {
    fontCache: 'global'
  }
};
// {% endraw %}
