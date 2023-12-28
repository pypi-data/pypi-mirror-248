# Insurance Spell Check
Insurance Spell Check using Conditional Random Field (CRF)

## Install Library 
 ```
!pip install insurancespell
```
## How to use
Input:
```
เงินเวรคืนของก็มาทัน
```
```python
import insurancespellcheck
print(insurancespellcheck.check("เงินเวรคืนก็มาทัน"))
```
Output:
```
เงิน<คำผิด>เวรคืน</คำผิด><คำผิด>ก็มาทัน</คำผิด>
```

The words in <คำผิด>(*)</คำผิด> are wrongword in Insurance .

if you want to use auto_correct for change to correctword, use ```auto_correct=True``` in code.
```python
import insurancespellcheck
print(insurancespellcheck.check("เงินเวรคืนก็มาทัน",auto_correct=True))
```
Output:

```
เงินเวนคืนของกรมธรรม์

```
if you want to use correct_word for get specific correct word, use ```correct_word=True``` in code.
```python
import insurancespellcheck
print(insurancespellcheck.check("เงินเวรคืนก็มาทัน",correct_word=True))
```
Output:

```
['เวนคืน', 'กรมธรรม์']
```

## License
   Copyright 2023 Thiraphat Chorakhe
