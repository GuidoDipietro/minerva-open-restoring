# Minerva Open Guadalajara 2023

These are the scripts I used to restore a JSON formatted file only from encrypted PDF files for result submission of an official WCA competition in Mexico.

# What happened?

Delegates of a competition must generate the scrambles using a software called [TNoodle](https://github.com/thewca/tnoodle-lib), which generates human-readable PDF files with the scrambles, as well as JSON and other files for result submission.

As scrambles are part of the data that must be submitted to the WCA in order to add the results to their database, this is a key part in this process.

By accident (it can happen, that's fine), the JSON files were lost after the first day, leaving the Delegates only with the PDF files which are not meant for data interchange, but only for staff to use them on the day of the competition.

Moreover, the PDFs are encrypted each one with a different password, which made everything more difficult.

# How to proceed?

Restoring the correct JSON was possible as the data was 100% available from the PDF files, given the passwords were still available. But this was an annoying and time consuming task, as it basically implied opening each PDF file one by one, then copying the scrambles by hand and then checking they were correct.

This would have taken days and probably many errors on its way. So thankfully we have computers.

The Delegates for this competition generated new scrambles after day 1, so now we had a valid JSON in which we just had to replace the old scrambles with the ones that were actually used.

# Scripts

With the file names and the passwords we can generate decryption commands using some tool such as `qpdf`. So I did that in `decrypt.sh` (passwords redacted). For some reason I couldn't get this to work in Python. The original files were replaced by these which are now simple to read (check them in the dir `PDFs`).

After that, we can extract the text from a PDF file using `PyPDF2` then parse it accordingly splitting it using multi-delimiters indicating the start of a scramble. I used `'1', '\n2', '\n3', '\n4', '\n5', 'E1', 'E2'` which were enough for most of the sets.

In the file `work.py` I perform this extraction and parsing and then format this as a JSON object in the same way as it is stored in the final JSON file we want to form.

This works perfectly for most sets, except for Clock as the notation has weird numbers and it gets a bit messy (due to the `1` delimiter). For this reason, the Clock sets were typed out manually aided by `clock.py` to save some typing. It was 3am already so this was the easiest thing to do.

# Final result

You can see the final result in `parsed.txt`, which has each round followed by their scrambles, struct which was then pasted into the final JSON file which is not added to this repo but basically follows a structure where you have a key `events` with key `rounds` with key `scrambleSets` which is an array with two keys `scrambles` and `extraScrambles`. So we just replace those two by the thing we genned and we're good to go!

All in all, it didn't take me longer than a few hours, mostly triple-checking that everything was correct and I had not made mistakes in the parsing. :D
