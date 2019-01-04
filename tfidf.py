# encoding=utf-8
from __future__ import absolute_import
import os, codecs
import jieba
import jieba.posseg
from operator import itemgetter
import logging

_get_module_path = lambda path: os.path.normpath(os.path.join(os.getcwd(),
                                                 os.path.dirname(__file__), path))
_get_abs_path = jieba._get_abs_path

DEFAULT_IDF = _get_module_path("idf.big.txt ") # 2018/12/26 idf.txt/ idf.big.txt / idf_new.txt


class KeywordExtractor(object):

    STOP_WORDS = set((
        "the", "of", "is", "and", "to", "in", "that", "we", "for", "an", "are",
        "by", "be", "as", "on", "with", "can", "if", "from", "which", "you", "it",
        "this", "then", "at", "have", "all", "not", "one", "has", "or", "that"
        , "AUO", "Classify", "General", "Confidential"
    ))

    def set_stop_words2(self, stop_words_path):  # HL
        abs_path = _get_abs_path(stop_words_path)
        if not os.path.isfile(abs_path):
            raise Exception("jieba: file does not exist: " + abs_path)
        content = open(abs_path, 'rb').read().decode('utf-8')
        for line in content.splitlines():
            self.stop_words.add(line)

    def extract_tags(self, *args, **kwargs):
        raise NotImplementedError




class IDFLoader(object):

    def __init__(self, idf_path=None):
        self.path = ""
        self.idf_freq = {}
        self.median_idf = 0.0
        if idf_path:
            self.set_new_path(idf_path)

    def set_new_path(self, new_idf_path):
        if self.path != new_idf_path:
            self.path = new_idf_path
            content = open(new_idf_path, 'rb').read().decode('utf-8')
            print('有用jieba有统计好的idf值')
            self.idf_freq = {}
            for line in content.splitlines():
                #print('顯示錯誤： %s' %(line.strip().split(' ')))
                word, freq = line.strip().split(' ')
                self.idf_freq[word] = float(freq)
            self.median_idf = sorted(
                self.idf_freq.values())[len(self.idf_freq) // 2]

            print('sorted(self.idf_freq.values()) = %s' %(sorted(self.idf_freq.values())))

            #print('len(self.idf_freq) // 2 = %s' %(len(self.idf_freq) // 2))
            #print('self.median_idf = %s' %(self.median_idf))
            with codecs.open('idfFreq_0104.txt', 'w', encoding='utf-8') as file:
                idfFreq = sorted(self.idf_freq.values())
                file.write("{}\n".format(idfFreq))

    def get_idf(self):
        return self.idf_freq, self.median_idf


class TFIDF(KeywordExtractor):

    def __init__(self, idf_path=None):
        self.tokenizer = jieba.dt
        self.postokenizer = jieba.posseg.dt
        self.stop_words = self.STOP_WORDS.copy()
        self.idf_loader = IDFLoader(idf_path or DEFAULT_IDF)
        self.idf_freq, self.median_idf = self.idf_loader.get_idf()
        print('stop_words = ' ,self.stop_words )
        #print('self.idf_freq = %s, self.median_idf = %s' %(self.idf_freq, self.median_idf ))


    def add_stop_words(self, this_stop_word):
        #print(this_stop_word)
        self.stop_words.add(this_stop_word)

    def renew_stop_words(self):
        self.stop_words = set((
        "the", "of", "is", "and", "to", "in", "that", "we", "for", "an", "are",
        "by", "be", "as", "on", "with", "can", "if", "from", "which", "you", "it",
        "this", "then", "at", "have", "all", "not", "one", "has", "or", "that"
    ))


    def set_idf_path(self, idf_path):
        new_abs_path = _get_abs_path(idf_path)
        if not os.path.isfile(new_abs_path):
            raise Exception("jieba: file does not exist: " + new_abs_path)
        self.idf_loader.set_new_path(new_abs_path)
        self.idf_freq, self.median_idf = self.idf_loader.get_idf()

    logging.debug('Start of TF-IDF program')
    def extract_tags(self, sentence, topK=20, withWeight=False, allowPOS=(), withFlag=False):
        """
        Extract keywords from sentence using TF-IDF algorithm.
        Parameter:
            - topK: return how many top keywords. `None` for all possible words.
            - withWeight: if True, return a list of (word, weight);
                          if False, return a list of words.
            - allowPOS: the allowed POS list eg. ['ns', 'n', 'vn', 'v','nr'].
                        if the POS of w is not in this list,it will be filtered.
            - withFlag: only work with allowPOS is not empty.
                        if True, return a list of pair(word, weight) like posseg.cut
                        if False, return a list of words
        """
        if allowPOS:
            allowPOS = frozenset(allowPOS)
            words = self.postokenizer.cut(sentence)
        else:
            words = self.tokenizer.cut(sentence)
        freq = {}
        freq_cnt = {}
        TF = {}
        IDF_all = {}
        for w in words:
            if allowPOS:
                if w.flag not in allowPOS:
                    continue
                elif not withFlag:
                    w = w.word
            wc = w.word if allowPOS and withFlag else w
            #if len(wc.strip()) < 2 or wc.lower() in self.stop_words or wc.lower()[0].encode('UTF-8').isalpha() or wc.lower()[0].isdigit():  # HL 拿掉數字和英文
            #if len(wc.strip()) < 2 or wc.lower() in self.stop_words or wc.lower()[0].isdigit():  # Anson 保留英文/拿掉數字
            # Anson 保留英文/數字/中文；去掉一個中文字 // 拿掉停止詞
            if len(wc.strip()) < 2 or wc.lower() in self.stop_words or wc in self.stop_words:
                #print('顯示斷字  = %s ' %wc) # 要拿掉的字 ； #print('顯示self.stop_words: %s' %self.stop_words)
                continue

            freq[w] = freq.get(w, 0.0) + 1.0
            freq_cnt[w] = freq_cnt.get(w, 0.0) + 1.0
            IDF_all[w] = IDF_all.get(w,0.0) + 1.0

            #print('顯示斷字  = %s / 出現次數 = %d' %(w, freq_cnt[w]))
            #logging.basicConfig(level=logging.DEBUG, format='顯示freq %s' %(freq_cnt))
        total = sum(freq.values())
        #print('顯示total斷字個數 = %d\n' %total)
        ''' freq = TF-IDF = Term of Freq 關鍵字出現次數 \
        self.idf_freq.get(kw, self.median_idf) = idf of kw '''
        ''' if allowPOS and withFlag:
                kw = k.word
            else:
                kw = k'''
        for k in freq:
            kw = k.word if allowPOS and withFlag else k
            print('顯示kw = %s, self.median_idf = %s '  %(kw, self.median_idf) )
            #print('顯示kw = %s, IDF = %s\n' %(kw, self.idf_freq.get(kw, self.median_idf)))
            #print('顯示kw = %s, IDF = %s\n' %(kw, self.idf_freq.get(kw, self.median_idf)))

            '''TF(Term of Freq 關鍵字出現次數)'''
            TF[k] = freq[k]
            #print('顯示TF[%s] = %s\n' %(k,TF[k]))
            #freq[k] *= self.idf_freq.get(kw, self.median_idf) / total
            freq[k] = (freq[k]/ total) * self.idf_freq.get(kw, self.median_idf)
            IDF_all.update({kw:self.idf_freq.get(kw, self.median_idf)})


        #print('顯示IDF_all斷字個數 = %s\n' %IDF_all)
        #print('顯示TF-IDF freq = %s\n' %freq)
        #print('顯示freq個數 = %s\n' %len(freq_cnt))
        if withWeight:
            tags = sorted(freq.items(), key=itemgetter(1), reverse=True)
            freq_cnt_tags = sorted(freq_cnt.items(), key=itemgetter(1), reverse=True)
            IDF_all_cnt_tags = sorted(IDF_all.items(), key=itemgetter(1), reverse=True)
        else:
            tags = sorted(freq, key=freq.__getitem__, reverse=True)
            freq_cnt_tags = sorted(freq_cnt.items(), key=freq_cnt.__getitem__, reverse=True)
        if topK:
            return tags[:topK], TF, total, IDF_all_cnt_tags
        else:
            return tags, freq, total

