# Django-TestCases
A practice repo where I explore django tests, factory boy, mock calls, django signals and docker. The use case was from an interview where I failed so this is me learning from my mistakes
# Use Case
The use case is a fintech startup that trades digital currency between users of the system. The Transfer ledger always records two transactions per action. A debit on the receivers account(positive amount) and a credit on the senders account(negative amount)
# Practice points
1. Django Tests using factory boy
2. Using Github issues, cross linking and PRs
3. Django Signals

# How to get this up and running

Run ```docker-compose up -d``` to get it started.

Once everything is built and running, you should migrate your database by running ```docker-compose run --rm django migrate```.
Now you should be able to see the welcome page on <http://localhost:8000/>.

To get into the Django shell, use ```docker-compose run --rm django shell```.
Run ```docker-compose run --rm django test``` to execute the tests. 

You can use the management command ```initialize_data``` to seed the database with some test data. Run ```docker-compose run --rm django initialize_data``` to execute it.

