# Sprint 1 - Developing a DB and UI Prototype


## Sprint Goals

Develop a design for the database and a UI prototype that simulates the key functionality of the system. Test and refine the UI so that it can serve as the model for the next phase of development in Sprint 2.

### Specific Goals

**Edit these goals as needed**

- Design the database:
    - Tables
    - Fields / types
    - Primary keys
    - Default / nullable values
    - Relationships (foreign keys)
- Design the UI
    - Key pages
    - User interactions and 'flow'
    - Page layouts / features
    - Colour palette
    - Etc.


## Initial Database Design

Replace this text with notes regarding the DB design.

![DB Design](screenshots/placeholder.png)


### Required Data Input

The user data will have to be input by the election officer consisting of all the NZART financial members at the time of election. This will consist of name, callsign and email address.

Candidate info will have to be entered on nomination.


### Required Data Output

The system will display the member's name when they log in and will display to the election nominees/officer the results of the election.
It will fetch candidate info to be displayed.

### Required Data Processing

Replace this text with a description of how the data will be processed to achieve the desired output(s) - any processes / formulae?

Most candidate and user data is stored in the clear as it has to be displayed but passwords must be salted and hashed according to best practices.

The ballots are interesting as they have to be homomorphically encrypted by the clients on submission to ensure ballot integrity and secrecy. I will use the Microsoft SEAL homomorphic encryption for the ballots using the BFV scheme which allows for exact operations on integers which is what we want for tallying the votes. I plan to use the tenseal library for the backend and the node-seal library for the client-side operations.


## UI 'Flow'

The first stage of prototyping was to explore how the UI might 'flow' between states, based on the required functionality.

This Figma demo shows the initial design for the UI 'flow':

**FIGMA FLOW - PLACE THE FIGMA EMBED CODE HERE - MAKE SURE IT IS SET SO THAT EVERYONE CAN ACCESS IT**

### Testing

Replace this text with notes about what you did to test the UI flow and the outcome of the testing.

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

*IMPROVED FIGMA FLOW - PLACE THE FIGMA EMBED CODE HERE - MAKE SURE IT IS SET SO THAT EVERYONE CAN ACCESS IT*


## Initial UI Prototype

Next stage is to find colors for the site:

### Starting with the already established NZART colours
https://www.realtimecolors.com/?colors=050315-fbfbfe-ae1f1a-000000-ae1f1a&fonts=Roboto%20Slab-roboto

### Moving to a slightly more colorful pallete:
https://www.realtimecolors.com/?colors=050315-fbfbfe-ae1f1a-beb8ad-a7b09a&fonts=Roboto%20Slab-Roboto


The next stage of prototyping was to develop the layout for each screen of the UI.

This Figma demo shows the initial layout design for the UI:



*FIGMA PROTOTYPE - PLACE THE FIGMA EMBED CODE HERE - MAKE SURE IT IS SET SO THAT EVERYONE CAN ACCESS IT*

### Testing

Replace this text with notes about what you did to test the UI flow and the outcome of the testing.

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

*FIGMA IMPROVED PROTOTYPE - PLACE THE FIGMA EMBED CODE HERE - MAKE SURE IT IS SET SO THAT EVERYONE CAN ACCESS IT*


## Refined UI Prototype

Having established the layout of the UI screens, the prototype was refined visually, in terms of colour, fonts, etc.

This Figma demo shows the UI with refinements applied:

*FIGMA REFINED PROTOTYPE - PLACE THE FIGMA EMBED CODE HERE - MAKE SURE IT IS SET SO THAT EVERYONE CAN ACCESS IT*

### Testing

Replace this text with notes about what you did to test the UI flow and the outcome of the testing.

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

*FIGMA IMPROVED REFINED PROTOTYPE - PLACE THE FIGMA EMBED CODE HERE - MAKE SURE IT IS SET SO THAT EVERYONE CAN ACCESS IT*


## Sprint Review

Replace this text with a statement about how the sprint has moved the project forward - key success point, any things that didn't go so well, etc.

