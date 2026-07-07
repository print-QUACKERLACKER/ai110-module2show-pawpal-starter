# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Classes from the instructions such as pet, owner, task and schedule. I had Claude figure out the relationships as they all intertwine with each other. Schedule has time and management properties, pet holds mainly str info, owner does aswell and task holds str objectives.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
No changes were made.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
Priority and time were decided based on how many hours the user entered prior, added up. If the user adds multiple of the same activities with the same details, the priorities will be randomized. Time stamps were scaled by x5 to ensure consistency. 
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

There is a limit to how much time the user can enter, this works in favor of producing accurate schedule planning for the user.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I utilized snippets of questions from the read me document to help form my instructions when using Claude. I asked Claude to also help run the initial pawpal file and update it with changes.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
So far for me, I did not reject any suggestions as I was straightforward with my questions and instructions that Claude was able to generate what I had expected.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested if the user could enter more time in activities than entered before when filling in basic info, and the program correctly displayed that there would be no time for the schedule. These tests are important to ensure that there is no point in the code where the program breaks and considers possibilities for new errors.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am fairly confident that my scheduler works correctly, as I approached making the design as if I were to actually use the program for my pet. I considered the elements I would want the code to have for maximum support for my pet's needs.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

Navigating well with AI. Claude is able to produce quick and easy explanations to code generated and allows for me to see what has changed before and after.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

Improve the UI design so that not everything looks the same. It would be helpful if the schedule builder could be a different color to differentiate itself from the rest of the app.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

You must have the logic and understanding thought out before using AI. AI is extremely helpful and can help you code a big project in just a few minutes, but all that wont mean anything if you don't give the AI the correct instructions and accurately draw out relationships between every component.