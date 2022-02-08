# Lindsey's Spelling Bee

A clone of the NYT Spelling Bee. Words generated from the
ubuntu American English dictionary. Difficulty thresholds
modeled using past puzzles and a simple linear regression
on total possible score. Total score chosen over number of
words because it has a slightly tighter correlation.

![Score threshold modelling](https://github.com/PlethoraChutney/spelling-bee/blob/main/utils/threshold_modelling.png?raw=true)



## Project setup
```
npm install
python -m pip install -r requirements.txt
```

### Compiles and minifies for production
```
npm run build
```

### Compiles and minifies for development (devtools enabled)
```
npm run dev
```

### Lints and fixes files
```
npm run lint
```
