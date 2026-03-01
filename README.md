# AI-Grid-Infrastructure
PRODUCT REQUIREMENTS DOCUMENT
AI Grid Orchestrator
A Smarter Way to Manage the U.S. Electric Grid
Ibrahima  |  Gary  |  Michael C
Grid Infrastructure & Smart Grid  —  Version 1.0  —  Due Wednesday


1.  EXECUTIVE SUMMARY


The Key Insight
Texas and Maine are both investing in renewables but wind and solar only cover 27-43% of total demand. Battery storage covers less than 1% of the daily energy deficit. The grid has no smart way to manage the gap in real time.


The Problem
The U.S. electric grid was not built for what it is dealing with right now. In Texas demand is exploding from AI data centers and crypto mining — projected to nearly double by 2030. In Maine gas dependency is driving electricity prices to nearly double the national average. Both states passed laws to try to fix it — Texas SB-6 and Maine LD 1726 — but all those laws give the grid is a kill switch. Cut power completely or do nothing. There is no middle ground.

That gap between what the law requires and what technology can actually do right now — that is the problem we are solving.

The Solution
The AI Grid Orchestrator is a software layer that sits between the electric grid and large loads like AI data centers. Instead of cutting power completely during a crisis it automatically throttles demand down by 5%, 12%, or 22% based on real time grid conditions — in milliseconds. The data center stays running. The grid stays stable. SB-6 compliance is maintained. We are not replacing the kill switch — we are making it smarter.



2.  SCOPE — WHAT'S IN AND WHAT'S OUT


IN SCOPE — What We Are Building
OUT OF SCOPE — What We Are NOT Building


Live data ingestion from ERCOT API (Texas frequency and reserves)
IN SCOPE


Live data ingestion from ISO-NE API (Maine fuel mix and real-time prices)
IN SCOPE


Logic Engine that translates grid stress into automatic throttle commands
IN SCOPE


Tiered load control — Critical AI stays on, Training AI gets throttled first
IN SCOPE


Mock data center server that responds to throttle commands automatically
IN SCOPE


Streamlit dashboard showing live grid status for Texas and Maine
IN SCOPE


Texas Reliability Mode trigger — frequency below 59.97 Hz reduces load 40%
IN SCOPE


Maine Green Mode trigger — gas above 50% or price above $150/MWh reduces load 25%
IN SCOPE


Cloud deployment — MVP runs on localhost only
OUT OF SCOPE


Real integration with actual data center hardware — mock server only for this sprint
OUT OF SCOPE


FERC or NERC regulatory certification — compliance framework is future phase
OUT OF SCOPE


Extreme weather harvest module (turbine pitch/yaw optimization) — future feature
OUT OF SCOPE


Virtual Power Plant aggregation of residential batteries and EVs — future phase
OUT OF SCOPE


Mobile app or external user accounts — dashboard is internal only for MVP
OUT OF SCOPE


Multi-state expansion beyond Texas and Maine — two states only for this sprint
OUT OF SCOPE




3.  THE PROBLEM IN DETAIL


Texas — Capacity Crisis
Metric
Data
Source
Fuel Mix
Gas 41% | Wind 27% | Solar 14% | Coal 13% | Nuclear 8%
ERCOT 2025-2026
Renewable Coverage
27-43% of monthly demand
ERCOT Fuel Mix Data
Worst Month
August — 27.1% covered (AC peak + wind lull)
ERCOT Analysis
Storage (2024)
5.5 GWh vs 1,200 GWh daily deficit (<1%)
SEIA Q1 2026
Storage (2026)
23 GWh vs 1,150 GWh daily deficit (2%)
SEIA Q1 2026
Storage (2030 Proj)
85 GWh vs 1,050 GWh daily deficit (~8%)
SEIA Projection
Data Center Demand
8 GW (2025) growing to 40+ GW by 2028
ERCOT Capacity Report
Key Law
SB-6 (2026) — remote disconnection for loads >75 MW
Texas Legislature


Maine — Price Crisis
Metric
Data
Source
Fuel Mix (NE Grid)
Gas 55% | Nuclear 25% | Renewables 13% | Hydro 6%
ISO-NE Feb 2026
Wholesale Price
$74.94/MWh day ahead (Feb 16-19 2026)
ISO-NE Weekly Report
Grid Imports
8,146 GWh from NY, Quebec, New Brunswick
ISO-NE Generation Table
Price Volatility
Prices hit negative on Feb 18 due to ME-NH congestion
ISO-NE Feb 2026
Storage (2024)
0.1 GWh vs 24 GWh daily deficit
SEIA Q1 2026
Storage (2030 Proj)
1.6 GWh vs 21 GWh daily deficit (~7.6%)
Maine Energy Plan 2025
Key Law
LD 1726 (Feb 2026) — flexible interconnection exploration
Maine Legislature




4.  WHO FEELS THIS PROBLEM


User
Their Pain Point
How Our Build Helps
Grid Operator (ERCOT)
Demand spikes from AI data centers threatening blackouts. Only tool is a blunt kill switch.
AI throttles large loads automatically in <200ms. Grid stays stable without cutting power.
Data Center Manager
SB-6 means full shutdown during emergencies. Operations crash. Revenue lost.
Throttle by 5-22% instead of 100% off. Stay running, stay compliant, avoid crashes.
Maine Resident
Paying $74.94/MWh — near double national average because of gas dependency.
Shift loads to hours when wind and hydro are running at full capacity. Break the gas price link.
Renewable Developer
Energy gets wasted during storms when turbines shut down or solar loses efficiency.
Smart dispatch captures surplus energy to batteries instead of losing it.




5.  WHAT WE ARE BUILDING


Core Features — MVP Sprint
Feature 1 — Real-Time Grid Monitor: Pull live data from ERCOT and ISO-NE every 60 seconds. Track system frequency, operating reserves, fuel mix percentage, and real-time prices.

Feature 2 — Logic Engine: Translate grid stress into automatic power commands. Texas: frequency below 59.97 Hz triggers Reliability Mode, reduce load 40%. Maine: gas above 50% or price above $150/MWh triggers Green Mode, reduce load 25%.

Feature 3 — Tiered Load Control: Critical AI (inference) never shuts down. Flexible AI (training) gets throttled first. Data centers stay partially running at all times.

Feature 4 — Mock Data Center Server: Python script that listens for throttle commands and adjusts a visual Power Draw variable in real time. Proves autonomous response without needing real hardware.

Feature 5 — Live Dashboard: Streamlit interface showing grid status, active throttle commands, fuel mix, and price signals for Texas and Maine. Built to demo in under 3 minutes.

Technical Stack
Layer
Tool
Why
Language
Python
Fastest for API handling and data math
Framework
FastAPI
Handles data flow between scripts efficiently
Dashboard
Streamlit
Build the visual interface quickly
Data Sources
ERCOT API + ISO-NE API
Live real-time grid data
Hosting
Localhost (MVP)
Keep it simple for the demo — no cloud needed yet




6.  BUILD PLAN  (Sunday – Wednesday 6:30 PM)


We have from Sunday to Wednesday 6:30 PM. Every day has a clear owner and a clear milestone. If the milestone is not hit by end of day the next person cannot start their piece.


Day
Focus
Who
Milestone
Blocked If...
Sunday
Setup + Planning
All
Everyone has Python, FastAPI, and Streamlit installed and working. API keys pulled for ERCOT and ISO-NE. Group aligned on who does what starting Monday.
Environment not set up or group not synced going into Monday
Monday
Data Ingestion — Texas
Ibrahima
Live ERCOT frequency and fuel mix printing in terminal every 60 seconds without crashing.
API connection fails or data is not updating live
Tuesday
Data Ingestion — Maine + Logic Engine
Gary + Michael C
Gary: Maine gas % and prices live from ISO-NE. Michael C: Logic Engine script calculating throttle setpoint for both states automatically.
Data not pulling or script not triggering without manual input
Wednesday AM
Load Control + Dashboard
All
Mock server responds to throttle command. Streamlit dashboard showing live gauges for both states.
Server not listening or dashboard not displaying live data
Wednesday 4-6 PM
Full End-to-End Test
All
Run the full system live — real data in, auto throttle fires, tiered response works, dashboard shows everything. Fix any last issues.
Any one of the three success criteria still broken
Wednesday 6:30 PM
DEADLINE — Demo Ready
All
3-minute demo talk track rehearsed. All three success criteria working. System is clean and ready to present.
Everything must be working by this time




7.  SUCCESS CRITERIA


The MVP must prove three things by Wednesday. If all three work the demo is a success.


Live Connection: Show actual real-time grid data from ERCOT and ISO-NE — not fake or hardcoded numbers.
Autonomous Action: The throttle command must trigger automatically without anyone clicking a button.
Tiered Response: Critical AI stays online while Training AI drops load to protect the grid.

Key Performance Indicators
KPI
Target
What It Proves
Response Latency
<200ms for critical commands
Fast enough for real grid events
Data Refresh Rate
Every 60 seconds without crashing
Reliable live connection
Throttle Accuracy
5% / 12% / 22% tiers execute correctly
Precision control vs blunt kill switch
Peaker Displacement
Reduction in gas peaker activations during peaks
Real world grid impact
Zero Blackouts
Grid stays stable during simulated demand spike
Core value proposition proven




8.  LEGAL COMPLIANCE


Our build does not fight existing laws — it exceeds what they require. That is the pitch.

Law
What It Requires
What Our Build Does
Texas SB-6 (2026)
Data centers >75 MW must be remotely disconnectable during emergencies.
Instead of a remote kill switch we provide automated throttling — safer, smarter, and fully compliant.
Maine LD 1726 (Feb 2026)
Utilities must explore flexible interconnection solutions.
Our load shifting and demand response software is exactly the flexible interconnection solution the law is asking for.


Bottom line: Both laws prove the problem is real and urgent. Neither law provides the software solution yet. We are building it.




9.  NEXT STEPS


Sunday — Everyone installs Python, FastAPI, and Streamlit. Pull API access for ERCOT and ISO-NE. Group gets aligned on the plan.
Monday — Ibrahima starts ERCOT data ingestion. Goal: live Texas frequency printing in terminal every 60 seconds.
Tuesday — Gary pulls ISO-NE Maine data live. Michael C builds and tests the Logic Engine script.
Wednesday AM — All three connect mock server and build Streamlit dashboard together.
Wednesday 4-6 PM — Full end-to-end system test. Run everything live and fix any last issues.
Wednesday 6:30 PM — DEADLINE. Demo is ready, talk track is rehearsed, all three success criteria are working.



AI Grid Orchestrator  —  Grid Infrastructure & Smart Grid  —  Ibrahima  |  Gary  |  Michael C


