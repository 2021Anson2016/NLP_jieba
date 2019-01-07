# NLP_jieba
筆記

(4)
提供一些討論完整的相關資源

英文
http://www.nltk.org/book/
https://web.stanford.edu/~jurafsky/slp3/ed3book.pdf

中文
http://www.52nlp.cn/
https://github.com/fxsjy/jieba

一篇NLP講解觀念清楚文章：
https://blog.liang2.tw/2015Talk-Chinese-Search/?full#not-the-best-way

https://stackoverflow.com/questions/11529273/how-to-condense-if-else-into-one-line-in-python
i = 5 if a > 7 else 0
translates into

if a > 7:
   i = 5
else:
   i = 0
   
http://cpmarkchang.logdown.com/posts/193915-natural-language-processing-tf-idf
1.Introduction
所謂的 TF-IDF , 是用來找出一篇文章中, 足以代表這篇文章的關鍵字的方法

例如, 有一篇新聞, 是 nltk 的 Reuters Corpus 中的文章, 這篇文章被歸類在 grain , ship 這兩種類別下, 文章的內容如下：

GRAIN SHIPS LOADING AT PORTLAND 
There were three grain ships loading and two ships were waiting to load at Portland , according to the Portland Merchants Exchange .

假設不知道什麼是 TF-IDF, 先用人工判別法試看看, 這篇新聞的關鍵字, 應該是 Portland , ship , grain 之類的字, 而不會是 to , at 這種常常出現的字
為什麼呢？因為 to 或 at 雖然在這篇文章中出現較多次, 但其他文章中也常有這些字, 所謂的關鍵的字, 應該是在這篇文章中出現較多次, 且在其他文章中比較少出現的字

所以,如果要在一篇文章中, 尋找這樣的關鍵字, 要考慮以下兩個要素:

1.這個字在這篇文章中出現的頻率( Term-Frequency TF )
2.在所有的文章中,有幾篇文章有這個字( Inverse-Document-Frequency IDF )
這就是所謂的 IF-IDF

公式如下：

其中, 表示在文章 中, 文字 出現的次數, 表示總共有幾篇文章, 表示有文字 的文章有幾篇

例如以上 Reuters Corpus 文章的例子, Portland 在這篇文章中出現了 3 次, 所以 , 而 Reuters Corpus , 總共有 10788 篇文章, , 在這些文章中, 有 Portland 這個字的文章, 有 28 篇, 所以 , 把這些數值帶入公式, 得出

如果是 to 這個字, 在這篇文章出現 2 次, 但是總共有 6944 篇文章有這個字, 所以算出來的 TF-IDF 是

就這樣, 根據公式算出 TF-IDF 值的大小, 值越大的, 越可以作為代表這篇文章的關鍵字
