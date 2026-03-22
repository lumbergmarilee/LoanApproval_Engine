# LoanApproval_Engine
Algorithm for approving loans

The Algorithm is given a client's credit modifer, the preferred loan amount and loan period.
It will find a client's credit_score and based on that it will secide whether or not to approve the loan. (btw credit_score = (credit_modifier/loan_amount)*loan_period )
The enigne will try to find the maximal loan amount that could be provided for the client.
If the requested loan period is not suitable for any loan, the algorithm will provide another suitable period (if it exists)

More about my decisions and way of approaching the task:

## Language chosen: Python
Python is the language I am most comfortable in for creating frontend and using API (so Flask).
For the frontend I decided to use HTML and CSS with minimal Javascript. I didn't think a whole React application was necessary so I kept it simple and these are also things that I have worked with before.

## Backend Logic

For the actual logic of the loan approval engine I decided to create just one python script with 5 functions. I decided to also do this in Python since I was doing everyhting else in Python.

The main function is **loan_approval_algorithm** that then calls out the other methods if necessary.

I tried to keep doubling code to a minimum so I created a helper function **approval_per_person** that get's the credit_modifier for the specific person and the loan_period (requested loan_amount wasn't necessary here because we will find the maximum allowed loan amount anyways) and first simply checks if the requested loan_period is allowed else tries to find another suitable period.

For finding the returnable loan amount I created a function **find_max_approval**. This finds the maximal loan amount which will be approved for this credit_modifier and loan_period. I tried using binary search for this at first. Seeing if an amount will be approved and if not trying to find a lower amount to be accepted. If approved trying to find if a higher amount would be approved. This was however rather slow. I then realised that the equation credit_score = (credit_modifier / loan_amount) * loan_period, can be transformed to max_amount = credit_modifier * loan_period. So instead of binary search I switched to using an algebratic approach. This means that for credit_score to be over or equal to one, from the division we see than credit_modifier * loan_period must be over the loan_amount. So the maximal loan_amount simply is credit_modifier * loan_period.

For finding an alternative suitable period I decided that "suitable" is any period in which the minimal loan (2000€) is approved for. I also created a helper function that does this called **find_suitable_period**. This aalso uses an algebratic approach where the minimal period which approves a loan_amount is math.ceil(loan_amount / credit_modifier).

I also created a scoring_algorithm method which simply uses the credit_score = (credit_modifier / loan_amount) * loan_period to tell if a specific credit_modifier, loan_amount and loan_period matches. We can use this from the frontend aswell to simply check if a specific loan will be approved or not (when it is not necessary to find the maximal allowed loan).

## Frontend specifications


