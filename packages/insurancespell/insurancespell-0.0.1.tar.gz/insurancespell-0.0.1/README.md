# Insurance Spell Check
Insurance Spell Check using Conditional Random Field (CRF)

## Install

> pip install insurancespell

## Using

```python
import insurancespell
print(insurancespell.check("เงินเวรคืนของก็มาทัน"))
```
Output:
```
เงิน<คำผิด>เวรคืน</คำผิด><คำผิด>ของก็มาทัน</คำผิด>
```

The words in <คำผิด>(*)</คำผิด> are wrongword in Insurance .

if you want to use autocorrect for change to correctword, use autocorrect=True in code.
```python
import insurancespell
print(insurancespell.check("เงินเวรคืนของก็มาทัน",autocorrect=True))
```
Output:

```
เงินเวนคืนของกรมธรรม์
```

## License
   Copyright 2023 Thiraphat Chorakhe
