# -*- coding: utf-8 -*-
import string
import re
import insurancespellcheck
import os
from pythainlp.tokenize import tcc
from pythainlp.tokenize import subword_tokenize
from pythainlp import subword_tokenize
import sklearn_crfsuite
from pythainlp.corpus import thai_syllables,thai_stopwords
stopwords = list(thai_stopwords())
syllable_dict = thai_syllables
custom_subwords = {
    "เงินคืน": [],
    'เงินเกิน': [],
    'เงินเคิน': [],
    'งานคืน': [],
    'หนึ่งคืน': [],
    'มันคือ': [],
    'เงินทุน': [],
    'เงินคือ': [],
    'ลืมคืน': [],
    'เงินเค็ม': [],
    'คืนเงิน': [],
    'เงินเดือน': [],
    'เงินผล': [],  
    'เป็นผล': [],
    'มันผล': [],
    'เน้นผล': [],
    'ประกัน':	[],
    'สัญญา':	[],
    'ติดตาม':	[],
    'ใบประกัน':	[],
    'เปลี่ยนแปลง':	[],
    'เปลี่ยนบัตร':	[],
    'เปลี่ยนเบี้ย':	[],
    'เปลี่ยนเมื่อ': [],
    'เปลี่ยนเบียร์': [],
    'เปลี่ยนงวด':	[],
    'เวนคืน': [],
    'ยกเลิก':	[],
    'ผลประโยชน์':[]
}
mydict = {
"เงินคืน": ['เงินเกิน','เงินเคิน','งานคืน','หนึ่งคืน','1คืน','มันคือ','เงินทุน','เงินคือ','ลืมคืน','เงินเค็ม','คืนเงิน','เงินเดือน'], 
'เงิน':['เดิน','เพลิน','โยน'], 
'เงินผล': ['เป็นผล','มันผล','เน้นผล'],
'เคลม': [	'เกม', 'เกมประกัน',	'เกมครับ','เล่นเกมต่อ', 'เฟรม',	'ครีม',	'เชม',	'เค็ม',	'เช่น',	'เตรียม',	'เครม',	'พิม'	,'เตือน',	'ทีม'	,'ธีม'	,'เขียน'	,'เทรน'	,'เสริม'	,'เคม'	,'เต็ม'	,'เขต'],
'ฟัง':	['ปัง', 'พัง'],
'สิน': ['ศีล','สิ่ง'], 
'กู้':	['กู'	,'กุ้ง'],
'จ่าย': ['ใส่',	'ส่าย','ถ่าย'],
'ค้าง':	['จ้าง'],
'บิล':	['บิล','บิน'],
'ชำระ':	['ชอบรับ'	,'ทำดอก'	,'มะระ',	'ทำลาย'], 
'ตัด':	['หลัก'],
'หัก':	['หัด'],
'ใบเสร็จ':	['ไม่เสร็จ'],
'กรมธรรม์':	['ก็มาทัน'	,'ก็มาทาน'	,'ก็มาทำ'	,'ก็มาทาม'	,'ก็มาทัม',	'กอทอ'	,'กอธอ'	,'กธ'	,'กธ.'	,'กท'	,'กท.'	,'กรรมฐาน','กรมทัณฑ์'	,'ตรงมาทัน'	,'การมาทำ'	,'กรมทหาร'	,'กันมาทัน'	,'ผมมาทัน'	,'ก้มว่ะ',	'กูทำ'	,'กันมานะ'	,'ตัวมาทาน'	,'กรมท่าน'	,'มาทำ',	'โทรมาฟัง',	'โปรโมชั่น'	,'กูไหมครับ'	,'ทั้งตัว'	,'ก็มาจากนั้น',	'ลงมาทาน'	,'มาทัน'	,'ไม่ทัน'	,'กฎบัตรผ่าน'	,'กุมภัณฑ์'	,'กรมการ'	,'กรมบริหาร'	,'กลุ่มมา'	,'กรมอัญชัน',	'ครบมาทัน',	'ก็มากัน',	'กฎหมายการ',	'กำกับ'	,'สมุนไพร',	'	องค์ประกอบ',	'คุณมาจาก',	'กฎไม่ทัน'	,'ประธาน'	,'ลงมาทำ',	'กลุ่มงาน'	,'ประการ'	,'ธรรมะ'	,'กำมะถัน',	'กับประธาน'	,'กอดขออภัย'	,'คุณธรรม',	'กลับมาทาน',	'ตัวมาตาม',	'อุปทาน'],
'ประกัน':	['ประกาศ',	'ปลากัด',	'พักกัน'	,'ตัดกัน'	,'ประการ'],
'แจ้ง':	['แกล้ง'	'แสร้ง'	'แป้ง'],
'ค่า':	[	'ผ้า'	,'ฆ่า']	,
'เช็ค':	['เขต',	'ชื่อ'	,'เค้ก',	'เด็ก'],
'เบิก':	['เบื่อ']			,
'สถานะ':	['สาม'	,'สถานี']		,
'สอบถาม':	[	'ก็ทาง'	,'แตกต่าง'	]	,
'สัญญา':	[	'สัญญาณ']	,
'โอพีดี':	['โอคีรี'	]		,
'ติดตาม':	['บทความ'	]		,
'ใบประกัน':	[	'ไปพักกัน']	,
'ครบ':	[	'พบ']	,
'เรื่อง':	['ลาก',	'เริ่ม'	,'เพื่อน,']	,
'ตาม':	['ฐาน'],
'ต้องการ':	['ต่อการ'	]	,
'หนี้':['นี่'	]	,
'เช็คเงิน':	['เป็นเงิน']		,
'ขอถาม'	:['ข้อความ']	,
'ออมนิ่':	[	'โอมิ'	]	,
'เลข':	['แรก'	]		,
'คืน':	['ยืน', 'กลืน']	,
'ขอเล่ม':	['ขอเล่น'	]	,
'คน':	['โค้ด', "โครต"],
'เปลี่ยน':	['พอรับ'],
'เปลี่ยนแปลง':	['เปลี่ยนแปลงงงงงง'	,'เป็นแปลง'	],
'โอน':	['โยน'],
'เปลี่ยนบัตร':	['เปลี่ยนบัตรรรรรรร'	,'ปฏิบัติ',	'เรียนบัตร'],
'เปลี่ยนเบี้ย':	['เปลี่ยนเบี้ยเงินประกัน',	'เปลี่ยนเมื่อ',	'เปลี่ยนเบียร์'],
'เปลี่ยนผู้':[	'เปลี่ยนผู้ถือกรม',	'เป็นผู้'	],
'เปลี่ยนวิธี':	['เปลี่ยนวิธีคิด'	,'เป็นวิธี'	],
'เปลี่ยนงวด':	['เปลี่ยนงวดประกัน'	,'เปลี่ยนนวด'	],
'เวนคืน':['แว่นคืน',	'แว่นขึ้น'	,'แหวนขึ้น'	,'เวรขึ้น', 'เป็นคืน','เพลงคืน','เวร','เวียน','เวท','เยน', 'เย็น',	'วิ่งขึ้น'	,'เลื่อนขึ้น'	,'เพลงคืน'	,'เก้งคืน'	,'เว้นคือ'	,'เวนเกิน',	'เป็นคือ'	,'เมื่อคืน',	'เวียนเทียน',	'เวียนคืน'	,'เรียนคืน'	,'เรียนคือ'	,'ปีนขึ้น',	'ตัวเอง'	,'เวียงคืน'	,'เงินเวียน'	,'วินคืน'	,'เบนคืน',	'เป็นคน'	,'เปลี่ยนคลื่น'	,'เมื่องอื่น'	,'เอียงคืน',	'เที่ยงคืน'	,'เวรคืน',	'แหวนครึ่ง',	'บริเวณคืน',	'เว่คืน'	,'เว้นคืน',	'เวรคือ'	,'เว่นขึ้น'	,'บินคืน'	,'เวที'	,'เวดขึ้น'	,'กลางคืน'	,'เวรครับ'	,'เรียกว่า'	,'เปลี่ยนคืน'	,'เวรเขื่อน'	,'เว่นคืน'	,'เว่งคืน'	,'แฟนคืน',	'เกวียนคืน'	,'ปืนคืน','ตัวเองคืน','วันคืน','ในคืน','เวทคืน','เลื่อนเป็น','เพลงคือ','เชิญขึ้น','มันคืน','เล่นขึ้น'	,'วิ่งคืน'],
'ยกเลิก':	['ละเลิก', 'ล้มเลิก'],
}
templates_file = os.path.join(os.path.dirname(insurancespellcheck.__file__),"sp.model")
invalidChars = set(string.punctuation.replace("_", ""))
dict_s=list(set(syllable_dict()))
# replace show correct word
def replace_correct_words(text: str, dictionary: dict = mydict):
    # Define a regex pattern to match the incorrect word within <คำผิด> tags
    pattern = re.compile(r'<คำผิด>(.*?)</คำผิด>')

    # Find all matches in the input string
    matches = pattern.findall(text)

    # Iterate over matches
    for match in matches:
        # Iterate over dictionary items
        for key, values in dictionary.items():
            # Check if the match is in the list of incorrect words
            if match in values:
                # Replace the incorrect word with the correct word
                replacement = key
                text = text.replace(f'<คำผิด>{match}</คำผิด>', replacement)
    return text

# get specific correct word
# return list
def get_correct_words(text: str, dictionary: dict = mydict):
    correct_words = []
    # Define a regex pattern to match the incorrect word within <คำผิด> tags
    pattern = re.compile(r'<คำผิด>(.*?)</คำผิด>')
    # Find all matches in the input string
    wrong_word = pattern.findall(text)
    for key, values in dictionary.items():
        for value in values:
            if value in wrong_word:
                correct_words.append(key)
    # return correct not duplicates
    return "\n".join(x for x in list(set(correct_words)))



## Tokenize subword
def tokenize_subword(text):
	return subword_tokenize(text, engine='dict', keep_whitespace=False)
##push mykey to subword
for key in custom_subwords.keys():
	custom_subwords[key] = tokenize_subword(key)
#Feature
def c(word):
    for i in list('กขฃคฆงจชซญฎฏฐฑฒณดตถทธนบปพฟภมยรลวศษสฬอ'):
        if i in word:
            return True
    return False

def n(word):
    for i in list('ฅฉผฟฌหฮ'):
        if i in word:
            return True
    return False

def v(word):
    for i in list('ะาำิีืึุู'):
        if i in word:
            return True
    return False

def w(word):
    for i in list('เแโใไ'):
        if i in word:
            return True
    return False

def is_special_characters(w):
    if any(char in invalidChars for char in w):
        return True
    else:
        return False

def is_numthai(w):
    return w in list("๑๒๓๔๕๖๗๘๙๐")

def lenbytcc(w):
    return tcc.segment(w)

def in_dict(word):
    return word in dict_s

def has_silencer(word):
    for i in list('์ๆฯ.'):
        if i in word:
            return True
    return False

def has_tonemarks(word):
    t=False
    for i in ['่','้','็','๊','๋']:
        if i in word:
            t=True
    return t

def isThai(chr):
 cVal = ord(chr)
 if(cVal >= 3584 and cVal <= 3711):
  return True
 return False

def isThaiWord(word):
 t=True
 for i in word:
  l=isThai(i)
  if l!=True and i!='.':
   t=False
   break
 return t

def is_stopword(word):
    return word in stopwords

def is_s(word):
    if word == " " or word =="\t" or word=="" or word=="\r\n" or word=="\n":
        return True
    else:
        return False

def lennum(word,num):
    if len(word)==num:
        return True
    return False

def _doc2features(doc, i):
    word = doc[i][0]
    # Features from current word
    features={
        'word.word': word,
        'word.stopword': is_stopword(word),
        'word.isthai':isThaiWord(word),
        'word.isnumthai':is_numthai(word),
        'word.isspace':word.isspace(),
        'word.tonemarks':has_tonemarks(word),
        'word.in_dict':in_dict(word),
        'word.silencer':has_silencer(word),
        'word.isdigit': word.isdigit(),
        'word.lentcc':lenbytcc(word),
        'word.c':c(word),
        'word.n':n(word),
        'word.v':v(word),
        'word.w':w(word),
        'word.is_special_characters':is_special_characters(word)
    }
    if i > 0:
        prevword = doc[i-1][0]
        features['word.prevword'] = prevword
        features['word.previsspace']=prevword.isspace()
        features['word.previsthai']=isThaiWord(prevword)
        features['word.prevstopword']=is_stopword(prevword)
        features['word.prevtonemarks']=has_tonemarks(prevword)
        features['word.previn_dict']=in_dict(prevword)
        features['word.previn_isnumthai']=is_numthai(prevword)
        features['word.prevsilencer']=has_silencer(prevword)
        features['word.prevwordisdigit'] = prevword.isdigit()
        features['word.prevlentcc'] = lenbytcc(prevword)
        features['word.prev_c'] = c(prevword)
        features['word.prev_n'] = n(prevword)
        features['word.prev_w'] = w(prevword)
        features['word.prev_v'] = v(prevword)
        features['word.prev_is_special_characters'] =is_special_characters(prevword)
    else:
        features['BOS'] = True # Special "Beginning of Sequence" tag
    # Features from next word
    if i < len(doc)-1:
        nextword = doc[i+1][0]
        features['word.nextword'] = nextword
        features['word.next_isspace']=nextword.isspace()
        features['word.next_isthai']=isThaiWord(nextword)
        features['word.next_tonemarks']=has_tonemarks(nextword)
        features['word.next_stopword']=is_stopword(nextword)
        features['word.next_in_dict']=in_dict(nextword)
        features['word.next_in_isnumthai']=is_numthai(nextword)
        features['word.next_silencer']=has_silencer(nextword)
        features['word.next_wordisdigit'] = nextword.isdigit()
        features['word.next_lentcc']=lenbytcc(nextword)
        features['word.next_c']=c(nextword)
        features['word.next_n']=n(nextword)
        features['word.next_w']=w(nextword)
        features['word.next_v']=v(nextword)
        features['word.next_is_special_characters']=is_special_characters(nextword)
    else:
        features['EOS'] = True # Special "End of Sequence" tag

    return features

def _extract_features(doc):
    return [_doc2features(doc, i) for i in range(len(doc))]

crf = sklearn_crfsuite.CRF(
    algorithm='pa',
    max_iterations=500,
    all_possible_transitions=True,
    model_filename=templates_file
)

## module check word
def check(text: str,auto_correct: bool=False, correct_word: bool = False):
    word_cut=tokenize_subword(text)
    X_test = _extract_features([(i,) for i in word_cut])
    y_=crf.predict_single(X_test)
    x= [(word_cut[i],data) for i,data in enumerate(y_)]
    output=""
    temp=''
    for i,b in enumerate(x):
        if i==len(x)-1 and 'B' in b[1] and temp=='B':
            output+="</คำผิด><คำผิด>"+b[0]+"</คำผิด>"
            temp='B'
        elif i==len(x)-1 and 'B' in b[1]:
            output+="<คำผิด>"+b[0]+"</คำผิด>"
            temp='B'
        elif 'B-' in b[1] and temp=='B':
            output+="</คำผิด><คำผิด>"+b[0]
            temp='B'
        elif 'B-' in b[1]:
            output+="<คำผิด>"+b[0]
            temp='B'
        elif 'O' in b[1] and temp=='B':
            output+="</คำผิด>"+b[0]
            temp='O'
        elif i==len(x)-1 and 'I' in b[1] and temp=='B':
            output+=b[0]+"</คำผิด>"
            temp='O'
        else:
            output+=b[0]
    if correct_word:
        output = get_correct_words(output)
    if auto_correct:
        output=replace_correct_words(output)
    return output
