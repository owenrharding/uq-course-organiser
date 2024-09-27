# Context
As I was applying for exchange, the system kept prompting me for details on my course - how many units I'd done, how many core courses I'd completed, how many electives I had left, blah blah blah.

UQ, although a great university, is notorious for its poor study planning materials. So, what I could have (and realistically should have) done is spend 20 minutes shoddily organising my degree on an excel document.

Instead, I spent a solid couple of hours writing a program that would automate all this for me so I'd never have to worry about it again.

# Overview
This program is kind of like a database in the way that I've implemented data insertion and parsing for a data storage model. However, I didn't want to have to set up or maintain an actual database, so instead I tried interfacing with a static json file for the first time.
The program has a number of features implemented so far, all used with CLI:
```Python
Usage: python3 degree_manager.py [-h] [--add] [--his] [--prog] [--rec 1|2]
```
The commands can be used cumulatively or exclusively.

# Features
### Displaying Degree Progress
Th `--prog` command provides a snapshot of the user's current progress in their degree. It calculates how many courses have been completed, how many are in progress, and how many are still required to graduate.
![Screenshot 2024-09-26 at 9 36 33 pm](https://github.com/user-attachments/assets/25df43e7-57af-4379-81aa-7b8d698c4bd0)

### Recommending Future Courses
One frustration that all UQ (engineering) students will know is the pain of trying to create a study plan that lines up with the semester which courses are offered, as finding this information takes at least three different trips between different pages.
The `--rec` command lists all courses, sorted by course category, that the user hasn't completed yet. However, the best part about it is that it makes the suggestions based on which semester the user asks for, making it super easy to find which courses to do.
![Screenshot 2024-09-26 at 9 36 47 pm](https://github.com/user-attachments/assets/84a7003d-d2e6-45b4-85e4-252f77ba2b1f)

### Adding Courses
When first playing around with json, I was writing each of the possible courses in my degree directly into the file. I quickly realised that I would need a much quicker, streamlined, and input-safeguarded way of doing this.

With the `--add` command, the program parses all the subcategories contained in the degree, prompts the user to select one to insert into, prompts the user for the course details, validates the input, and then writes to and saves the json file.

It also prompts to repeat, making it easy to continuously enter new courses.
![Screenshot 2024-09-26 at 9 33 07 pm](https://github.com/user-attachments/assets/83cd2b21-8673-4fad-bbf7-5f0f9e17a593)

### History
The `--his` command gives the user a display of all the courses they've already completed, sorting by year and semester taken. If it were SQL, this sounds like it would be super easy, but with json this was a fairly annoying amount of overhead to go with it.
![Screenshot 2024-09-26 at 9 35 42 pm](https://github.com/user-attachments/assets/dc878cdb-90b1-40f5-8eee-5c1a7795c765)
