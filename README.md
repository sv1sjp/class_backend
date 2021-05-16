# Ergasia_1_E18019_VAGIAKAKOS_DIMITRIOS
1η Απαλλακτική Εργασία στο μάθημα Πληροφοριακά Συστήματα. Τμήμα Ψηφιακών Συστημάτων Πανεπιστήμιο Πειραιώς

## Depedencies

Για την εκτέλεση του προγράμματος, κρίνεται απαραίτητη η εγκατάσταση ορισμένων βιβλιοθηκών της python3.

```bash
pip install pymongo flask bson
```
Το πρόγραμμα θα εκτελείται στην πόρτα 5000 μέσω flask και η Mongodb στην πόρτα 27017. Βεβαιωθείτε ότι δεν τρέχει κάποια άλλη υπηρεσία σε αυτές τις πόρτες.


## Προετοιμασία της MongoDB

Δημιουργήστε μία MongoDB με όνομα mongodb στην πόρτα 27017 και κάντε import το αρχείο "Students.json" 

Aν τρέχτε την Mongodb μέσω Docker, αντιγράψτε πρώτα το αρχείο ως εξής:
```bash
docker cp students.json mongodb:/students.json
```

Στην MongoDB πρακτικά δημιουργήθηκε μία database "InfoSys" με collecrtions students και users. Στην Collection students υπάρχουν τσ δεδομένα που κάναμε import προηγουμένως στην mongodb, ενώ στην collection users, θα προσθέτουμε μελοντικά τους χρήστες που εγγράφονται.



## /createUser

Δίνοντας 0.0.0.0:5000/createUser με μέθοδο POST, μπορούμε να δημιουργήσουμε έναν χρήστη στο σύστημα. Ο Χρήστης θα δοθεί ως ένα json αρχείο της μορφής:

```json

{
        "username": "some username", 
        "password": "a very secure password"
    }
```
To πρόγραμμα ελέγχει αν το json αρχείο είναι στην σωστή μορφή και μόνο τότε γίνεται η δημιουργία του χρήστη. Επιπλέον, αν υπάρχει χρήστης με ίδιο username, πάλι δεν θα γίνεται η εισαγωγή.

## /login 

Δίνοντας 0.0.0.0:5000/login με μέθοδο POST, μπορεί ένας user να κάνει login στο σύστημα. Ο Χρήστης θα δοθεί ως ένα json αρχείο της μορφής:

```json

{
        "username": "some username", 
        "password": "a very secure password"
    }
 ```

To πρόγραμμα ελέγχει αν το json αρχείο είναι στην σωστή μορφή και μόνο τότε γίνεται η προσπάθεια σύνδεσης του χρήστη. Αν το username δεν υπάρχει ή ο κωδικός του υπαρκτού username είναι λανθασμένος, τότε δεν γίνεται Login. 

Σε κάθε επιτυχημένο login, το πρόγραμμα επιστρέφει το username μαζί με το uuid. Το Uuid δημιουργείται κατά τo login, οπότε αλλάζει κάθε φορά που θα ξανακάνετε login στο πρόγραμμα.

## /getStudent
Δίνοντας 0.0.0.0:5000/getStudent με μέθοδο GET, μπορεί ένας user να αναζητήσει πληροφορίες για έναν student βάση του email του. Ο Χρήστης θα δοθεί ως ένα json αρχείο της μορφής:

```json
{"email" : "student@email.com" }
 ```
 Δικαίωμα αναζήτησης βάση email έχει αποκλειστικά χρήστης που έχει κάνει login πρώτα και έχει προστέσει το uuid του ως header στο "authorization". Διαφορετικά, το /getStudent δεν θα λειτουργήσει.
 
 ## /getStudents/thirties
 
 Δίνοντας 0.0.0.0:5000/getStudent με μέθοδο GET, μπορεί ένας user να δει στοιχεία για όσους είναι γεννημένοι το 1991.
 Δικαίωμα προβολής έχει αποκλειστικά χρήστης που έχει κάνει login πρώτα και έχει προστέσει το uuid του ως header στο "authorization". Διαφορετικά, το /getStudent/thirties δεν θα λειτουργήσει.
 
  ## /getStudents/oldies
 
 Δίνοντας 0.0.0.0:5000/oldies με μέθοδο GET, μπορεί ένας user να δει στοιχεία για όσους είναι γεννημένοι το 1991.
 Δικαίωμα προβολής έχει αποκλειστικά χρήστης που έχει κάνει login πρώτα και έχει προστέσει το uuid του ως header στο "authorization". Διαφορετικά, το /getStudent/oldies δεν θα λειτουργήσει.
 
## /getStudentAddress

Δίνοντας 0.0.0.0:5000/getStudentAddress με μέθοδο GET, μπορεί ένας user να αναζητήσει διεύθυνση για έναν student βάση του email του. Το email του student θα δοθεί ως ένα json αρχείο της μορφής:

```json
{"email" : "student@email.com" }
 ```
 Δικαίωμα αναζήτησης βάση email έχει αποκλειστικά χρήστης που έχει κάνει login πρώτα και έχει προστέσει το uuid του ως header στο "authorization". Διαφορετικά, το /getStudentAddress δεν θα λειτουργήσει.

## /deleteStudent

Δίνοντας 0.0.0.0:5000/deleteStudent με μέθοδο DELETE, μπορεί ένας user να διαγράψει έναν student βάση του email του. Το email του student θα δοθεί ως ένα json αρχείο της μορφής:

```json

{"email" : "student@email.com" }

 ```
 Δικαίωμα διαγραφής βάση email έχει αποκλειστικά χρήστης που έχει κάνει login πρώτα και έχει προστέσει το uuid του ως header στο "authorization". Διαφορετικά, το /deleteStudent δεν θα λειτουργήσει.

## /addCourses

Δίνοντας 0.0.0.0:5000/addCourses με μέθοδο PATCH, μπορεί ένας user να προσθέσει μαθήματα σε έναν student βάση του email του. Το email του student θα δοθεί ως ένα json αρχείο της μορφής:
``json
{
            email: "an email",
            courses: [
                {'course 1': 10, 
                {'course 2': 3 }, 
                {'course 3': 8},
                ...
            ]
        } 
   ``
Δικαίωμα προσθεσης έχει αποκλειστικά χρήστης που έχει κάνει login πρώτα και έχει προστέσει το uuid του ως header στο "authorization". Διαφορετικά, το /addCourses δεν θα λειτουργήσει.

 
 
## /getStudentAddress

Δίνοντας 0.0.0.0:5000/getPassedCourses με μέθοδο GET, μπορεί ένας user να αναζητήσει διεύθυνση για έναν student βάση του email του. Το email του student θα δοθεί ως ένα json αρχείο της μορφής:

```json
{"email" : "student@email.com" }
 ```
 Δικαίωμα αναζήτησης περασμένων μαθημάτων βάση email έχει αποκλειστικά χρήστης που έχει κάνει login πρώτα και έχει προστέσει το uuid του ως header στο "authorization". Διαφορετικά, το /getStudentAddress δεν θα λειτουργήσει.
