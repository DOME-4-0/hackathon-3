# Plan for the hackathon: 

## Day 1: Hack 1

- options 1, based on 
  - A) manual registration of data sets and 
  - B) batch registration of ontology based data or 
  - c) graph based data 



We need 1-2 problems, where in the domain a stakeholder has a few data resources that the user wants to make available trhough or on DOME 4.0 platform: 

User Story: --> I have a few (preferably many!) data sets, they are non-standard (no ontology based), but I want to make them discoverable by third parties 

Options: 
 - Data re Pharma, Data about various projects, etc from participants
 - Repositories
 - Data from Siemens, Bosch, Fraunhofer or other stake holders 
 - Data re some user store/show case in DOME4.0 

Option A is suitable for small, occasional data set registration, 

B requires some ontology, so it will be the first step of the hack, to create the ontology, or prepare it. 

C is similar to B, but the user is not interested in an ontology of the case, but we would still need to cast it in the 
DOME 4.0 basic metadata (the data set ontology)

in each case the hack should demonstrate the discoverability of the data 

### hack 1 (A): 
Hands on session on using all features of DOME 4.0, through the web interface, including onboarding of data sets (even if they are synthetic) (Bjorn is lead? and Adham backup)

Users will find data that are relevant to them (but does not have to be for the hackathon), the main goal is to learn the end user aspects. Report: is what do we like and what we do not like in DOME 4.0. 
  
### hack 2 (B):
- IDMT Case: Preview what the IDMT data/ontology is about, upload it through the ontology interface of DOME 4.0, then perrform searches and visualisations. [Amit]
- Pharma Case
  - connector to one of the open MRI databases (Adham to share with treesa)
  - building a basic ontology of the data sets already available at Chris's group. [Owain/Lingyun]   
- Owain
  - API to scan publications (from arxive) and pulling in the data into a DME 4.0 data set and uploading then visualisation, we can then think how to add this as a service into DOME 4.0, so we can relate papers to data sets and vice versa.    
- Lingyun
  - Nasicon battery data case, and digitalising it into the Data set ontology of DOME 4.0 [Lingyun]
- Talk to Adrien about demonstrating how he integrated a "secret application " by mixing the DOME 4.0 platform and the containers running locally behind firewalls [Candidate Adrien, Adham to contact]
- The Chase Case - Noel and Silvia

# Day 2: Problem Hack 2 (or Storyboard Development)
Here we will have two options, or strands, potentially 4. 
1. Story board development:
   2. based on hack 1 and the other sessions, what does DOME 4.0 still needs, what can we do to take it to the next level!
   3. a breakout to 
      4. a group discussing monetization avenues for stakeholders/platform, business models and exploitation avenues
      5. what other technical aspects can be done, can we use what we developed in a different more useful way? what do we need to do with provenance?
6. **OpenModel-DOME 4.0** case (Casper, Jesper, Owain?, Monica?)
7. **VIPCOAT-DOME 4.0 Case** (Casper, Treesa)--> (OTEAPI compatibility and uses)
8. address one of the use cases in details...need more details, e.g. from CMCL
  * CMCL connector provides emission simulation data
  * given the label (e.g. CO or SO2), search Chemeo and/or Pubchem GHS for more data
  * combine them in a Jupyter notebook (a new "app")
10. integrate applications (like the ones from the success stories ) using containerisation 
11. hands on visualisation session (Roberto, and Adham)
12. Docuementation building from a user perspective (Willem/Bijan)
