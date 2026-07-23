# Project Requirements

## Identified Problem or Need

**New Zealand Association of Radio Transmitters (NZART)** are an incorporated society that requires elections for their council members and for the office of president. They are currently physically mailing the voting slips to all their members with a return stamp, as they have done for the last 100 years but this is a cost of thousands of dollars annually to them along with poor voter turnout due to the inconvenience of physical mail and they wish to replace this with a more efficient and cheaper system (digital) that they can use.

## End-User Requirements

Replace this text with a description of your typical end-users and their specific needs / expectations / requirements.

There are two types of end users to this application:

 - Administrators/Returning Officer

 Very small group of trusted individuals that have much more control over the system. These people are fairly IT literate and expect to be able to use the system from a desktop situation rather than mobile.


 - Voting NZART Members

 Very large user base and so we should expect a large range of requirements. They require their interface to be accessible, intuitive and functional across a range of devices. Thus the mobile and desktop experience should be fairly equal. Some of these people will be scarily proficient in IT others will need a simple system. To allow them to use the system, it needs to be conventional and intuitive to reduce their mental load.



## Proposed Solution

I will create a system that allows candidates to be nominated and countersigned, which admins can then approve for a candidate to be open for election for the position of council or president NZART. The system will provide an interface for the users to vote as well.


# Relevant Implications

## Accessibility

I need to ensure that all people can use the system, regardless of how able they are. 

### Relevance to the System

The voting system will have to be used by all of NZART members so we have to be inclusive or else they will not be able to vote which is a problem. A significant portion of this user base is advanced in age and so vision impairments are more common. Additionally, the site will have to be responsive to cater for the wide range of devices that the users will have, from old windows pcs to ipads.

### Impact / Considerations
I will ensure excellent contrast between text and background to maintain readability for everyone.
I will ensure text sizing is not too small for the users.
I will use alt text in images and use semantic tags where possible to assist screen readers.
I will create a usable tabbing order for keyboard only navigation.


## Legal

Are there any relevant laws applicable to our voting system for an incorporated society?

### Relevance to the System

Under the Incorporated Societies Act 2022, we know that we can legally use an electronic means of voting (Section 93, subsection 2) once the NZART constitution has been updated to allow this (Remit passed AKL AGM 2026). Additionally, the system is storing some member data so we need to comply with data protection and privacy as per the Privacy Act 2020.

### Impact / Considerations

The system will keep the minimum amount of member data needed to function including email, name and callsign of current financial NZART members. There is no need to keep addresses, registration or licensing information.
Ensure that the system abides by the terms including security and fitness for purpose as set out in the future amendment to the contusion. 


## Aesthetics
Aesthetic Implications pertain to how the website looks from the user's perspective

### Relevance to the System
The website will have to look well put together as it needs to convey a trustworthy image or else people will not trust it with their vote.
The website, as it is affiliated with NZART will have to reflect the professionally of the organization.
Additionally, the less 'homebrew' the site looks, the less likely our end users will be curious and want to investigate.

### Impact / Considerations
Use a color scheme that is close to the existing NZART infrastructure. (lots of white and black with a red accent)
Making use of flask components wherever possible and using tailwind vars for consistency. 


## Security, Verifiability and Logging 

Ensure the system is secure from external or internal tampering by a bad actor.

### Relevance to the System

NZART is a large and serious organization which has to mean the threat of a bad actor is non-negligible. Additionally, the possibility of 'curious/investigative tampering' is _extremely_ high as it turns out amateur radio and computer nerds have quite a large overlap so plenty of members have the technical knowledge and spare time to go poking.

### Impact / Considerations

I will have to keep security in mind and prioritize it throughout the design process to ensure that is secure. I will cross check this with OWASP webapp standards (ensuring proper auth checks on serverside etc) as well as using homomorphic encryption to encrypt the votes in the database so that in the event of a breach, no cast votes are compromised.
I will add time and ip logging at a minimum to the member logins and votes to aid in any correlation/investigation of suspicious activity.
Additionally, the system will be submitted to a penetration test by a large reputable company before it is deployed to production.


## Functionality

The system has to work as expected, reliably, and quickly so it can function well to meet the specifications.

### Relevance to the System

NZART as an organization has a level of professionalism to meet so by this product being associated with them it also has to abide by those expectations. The system also has to function as it has a legitimate purpose that it must fulfill otherwise NZART will have to fall back to mailing voting slips which is a cost getting harder for them to bear. 

### Impact / Considerations

I will test the functionality by testing all elements of the website under different conditions to ensure everything works as expected in development. I will use Gunicorn with optimized assets to reduce loading times and CPU in production and get help deploying to production and load-testing it there.

## End-User

The system has to meet the requirements set by the end user for their purpose, prioritizing their wants and needs over my own beliefs.

### Relevance to the System

I am developing this system for NZART for them to use so it should be exactly what they need it to be otherwise it will simply not be used. This includes the member facing portion of the system where there is a diverse range of technical proficiencies, devices and user demographics that have to be considered or else we risk alienating that portion of the user base **which we must not do** as the system is the only way of registering their vote.

### Impact / Considerations

I will regularly get feedback from the current NZART council and my local branch which ensures that my feedback is from this wide range of users to cater and refine the site for all of them.



## Usability

The system needs to be as simple and intuitive as possible to perform tasks to meet the objective.

### Relevance to the System

The system must simple and intuitive to cater for the entire member base of NZART as everyone is relying on it to register their vote. This should be an easy and simple process, not one that is universally frustrating to the thousands that will use it.

### Impact / Considerations

I will use a conventional design including the recognized icons for save and discard
I will provide a way for the users to safely cancel their actions.
I will provide good feedback of system status which should help assure users of status when casting ballots etc.







# User Experience (UX) Principles

## Clear User Flows

The flows (step by step path) that the users take to complete an action need to be concise.

### Relevance to the System

Since there is a large range and number of people using the system to vote, it is essential that their flow is optimized to save their time and prevent collective human suffering. If 

### Impact / Considerations

I will test the user flow with the council and Nelson branch to get as many eyes on it as possible to get good feedback to arrive on a flow that everyone can agree is clear and efficient.
I will use Penpot to aid in this testing with a bare-bones flow prototype that makes it as easy as possible to refine this flow. 
This should result in a flow that has the minimum amount of steps while still being clear.



## Test and Improve

Test the system consistently to reveal issues and fix them.

### Relevance to the System

I am an inexperienced solo developer that will not get every single element of the system correct or even good the first time. To make the best result, this needs to be addressed somehow.

### Impact / Considerations

I am not building this voting system in complete isolation. I have a wide range of people with different experiences and skills in tech available so it only makes sense that I should use these people to test with and get feedback for my system which will give me the chance to fix the issues that I will introduce with incorrect design assumptions. Team work makes the dream work.
I can do this by sending penpot designs and a demo live version of the website to the council through email chains and meeting with them on Zoom and I can also do testing with the Nelson Branch through their monthly meetings.



## Consistency and Clarity

Keeping a simple layout consistent across pages helps learn and remember how to use the site quickly.

### Relevance to the System

The voting users experience should be as fast as possible and so we can use a consistent and simple layout for clarity so there should be no instructions needed to learn how to use the website. The administrators/voting officers would also benefit from not needing a manual to use their part of the website as it may be a different set of people each term so a nice and easy learning curve is beneficial to all.

### Impact / Considerations
I will make extensive use of Jinja components and templating to build the website which leads to a consistent look.
I will use tailwind vars where appropriate to keep cross-element consistency.



