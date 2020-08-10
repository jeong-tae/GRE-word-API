# GRE-word-SLACK API
This code is based on python3.x. Unfortunately, dataset is not open to public. If you collect the dataset during the study, you can add to `./data` folder for this app.  
```
# You should follow this form when you add words  
word1 translation1  
word2 translation2  
...
```

### pre-requisites
> pip install slacker
> mkdir data
You should add data files into this "data" directory.

### Compile
Then, 
> python send_quiz.py "{word|meaning|cloze|synonyms}"

Or you can send the quiz set daily as adding a command on crontab.

### Interactive System
![Screenshot](/samples/gre_cloze.PNG)
