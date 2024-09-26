# Context
As I was applying for exchange, the system kept prompting me for details on my course - how many units I'd done, how many core courses I'd completed, how many electives I had left, blah blah blah.

UQ, although a great university, is notorious for its poor study planning materials. So, what I could have (and realistically should have) done is spend 20 minutes shoddily organising my degree on an excel document.

Instead, I spent a solid couple of hours writing a program that would automate all this for me so I'd never have to worry about it again.

# Overview
This program is kind of like a database in the way that I've implemented data insertion and parsing for a data storage model. However, I didn't want to have to set up or have to maintain an actual database, so instead I tried interfacing with a static json file for the first time.
The program has a number of features implemented so far, all used with CLI:
```Python
Usage: python3 degree_manager.py [-h] [--add] [--his] [--prog] [--rec 1|2]
```
The commands can be used cumulatively or exclusively.

# Features
### Adding Courses
When first playing around with json, I was writing each of the possible courses in my degree directly into the file. I quickly realised that I would need a much quicker, streamlined, and input-safeguarded way of doing this.

With the `--add` command, the program parses all the subcategories contained in the degree, prompts the user to select one to insert into, prompts the user for the course details, validates the input, and then writes to and saves the json file.

It also prompts to repeat, making it easy to continuously enter new courses.
![Screenshot 2024-09-26 at 9 33 07 pm](https://github.com/user-attachments/assets/83cd2b21-8673-4fad-bbf7-5f0f9e17a593)
