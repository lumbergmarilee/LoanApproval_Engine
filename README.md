# LoanApproval_Engine

<img width="688" height="715" alt="image" src="https://github.com/user-attachments/assets/9b0aabdb-9ed7-4f67-86fa-c3f4f6676df9" />



Algorithm for approving loans

The Algorithm is given a client's credit modifer, the preferred loan amount and loan period.
It will find a client's credit_score and based on that it will secide whether or not to approve the loan. (btw credit_score = (credit_modifier/loan_amount)*loan_period )
The enigne will try to find the maximal loan amount that could be provided for the client.
If the requested loan period is not suitable for any loan, the algorithm will provide another suitable period (if it exists)

For running the application it is just needed to run the app.py script in a python environment and then the application will run at localhost 5000.

More about my decisions and way of approaching the task:

## Language chosen: Python
Python is the language I am most comfortable in for creating frontend and using API (so Flask).
For the frontend I decided to use HTML and CSS with minimal Javascript. I didn't think a whole React application was necessary so I kept it simple and these are also things that I have worked with before.

For the GitHUb project I didn't use any branching besides the main branch because the project was simple enough.

## Backend Logic

For the actual logic of the loan approval engine I decided to create just one python script with 5 functions. Didn't feel the need t ocreate multiple files for this.

The main function is **loan_approval_algorithm** that then calls out the other methods if necessary.

I tried to keep doubling code to a minimum so I created a helper function **approval_per_person** that get's the credit_modifier for the specific person and the loan_period (requested loan_amount wasn't necessary here because we will find the maximum allowed loan amount anyways) and first simply checks if the requested loan_period is allowed else tries to find another suitable period.

For finding the returnable loan amount I created a function **find_max_approval**. This finds the maximal loan amount which will be approved for this credit_modifier and loan_period. I tried using binary search for this at first. Seeing if an amount will be approved and if not trying to find a lower amount to be accepted. If approved trying to find if a higher amount would be approved. This was however rather slow. I then realised that the equation credit_score = (credit_modifier / loan_amount) * loan_period, can be transformed to max_amount = credit_modifier * loan_period. So instead of binary search I switched to using an algebratic approach. This means that for credit_score to be over or equal to one, from the division we see than credit_modifier * loan_period must be over the loan_amount. So the maximal loan_amount simply is credit_modifier * loan_period.

For finding an alternative suitable period I decided that "suitable" is any period in which the minimal loan (2000€) is approved for. I also created a helper function that does this called **find_suitable_period**. This aalso uses an algebratic approach where the minimal period which approves a loan_amount is math.ceil(loan_amount / credit_modifier).

I also created a scoring_algorithm method which simply uses the credit_score = (credit_modifier / loan_amount) * loan_period to tell if a specific credit_modifier, loan_amount and loan_period matches. We can use this from the frontend aswell to simply check if a specific loan will be approved or not (when it is not necessary to find the maximal allowed loan).

## Frontend specifications

As mentioned before I decided to use JavaScript, HTML and CSS for the design and frontend logic of the application.
For the structure of the project I decided to keep the .js, .html and .css files separate. Just so they would be easier to manage and troubleshooting would be easier.

### HTML choices

I thought about what the design of the engine should look like and decided on a slider approach. A user has to enter a person's ID number and then select the loan_amount and loan_period. I thought it would look good if both of these we're selected by a sliding mechanism, this would also make it easy to control the amounts that people can select (loan amount between 2000€ - 10 000€ and loan period between 12 - 60 months). It does look good, but I realised that for actually selecting specific numbers it can be a bit bothersome, so I added an input box next to the sliders that user's can use instead if wanted. I made the slider and input box sync, because I think this improves the customer experience overall. So if someone inputs a number it will also update the slider to show the same amount selected and vice versa. 

For the answer that will be shown as "approved" or "declined" I decided to just add a simple design box that pop's up under the "Check Eligibility" button. It looks clean while also keeping the code simple.

### CSS choices

I wanted to create an application that didn't feel too cramped and had some space to it. I also like a more rounded edge to these designs so I decited to implement a similar one. For the color scheme I chosee a light purple color palette with an anti'color being orange to showcase errors or loan denial's. I chose the main font to be Georgia Serif because I like it. For each separate "element" of the .html I created a design block in .css. Mostly my choices and reasonings for css choices are all "what I thought looked best".

### JavaScript chocies

Now I had to add logic to the .html page. For getting information from the page (person ID, requested loan amount and requested loan period) and submitting an answer I created a **submitLoan** function. It first clears any previous results and reads the personal code, loan amount and loan period from the input fields. If the personal code is empty it will show an error. It then disables the submit button and changes its text to "Checking…" so the user knows something is happening - this "Checking" rarely actually shows since I have 4 hard coded values for ID's and the code runs pretty fast. The function sends a POST request to the /api/loan-decision endpoint with the collected data as JSON. Once it gets a response back it checks if the decision was positive or negative and builds a simple HTML result box accordingly. The box shows the approved amount and period if positive, or the reason for decline if negative. If there's an additional note (like the period being adjusted) it adds that too. If the server can't be reached at all it shows a connection error. Regardless of what happens the button is re-enabled at the end.



