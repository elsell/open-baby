# Open Baby

Open Baby is a super simple way to log every day 
events for your baby. 

Log feeds, diapers, and pumping from a minimal interface
designed to be used by exhaused parents.

While there are many apps that do just that, Open Baby is intended
to be a no-frills, open-source, alternative that puts you in complete
control of your data. No third-party apps or cloud integrations, and your data
stays on your computer in a format that can be easily exported at any time.

## Scope

Open Baby is intentionally simple. It does not include authentication or
authorization at this time. It is intended to be run locally behind a firewall
where devices on the network are generally trusted.

There is no reason why Open Baby cannot include auth/z in the future. However,
the author is a new parent themselves and must choose simplicity to minimize
time to delivery for the initial application.

## Features

### Log Feedings

Open Baby supports both bottle and breast feedings, and allows
tracking the following attributs:

- Bottle
    - Feed Start Time
    - Amount
    - Type (Formula vs Breast Milk)
    - Additional Notes
- Breast
    - Feed Start Time
    - Feed End Time
    - Side (Left, Right, Both)
    - Additional Notes


### Log Pumping

Open Baby supports logging pumping sessions to enable tracking supply 
over time. The following attributes are tracked:

- Pump Start Time
- Pump End Time
- Total Amount

> [!Note]
> The exclusion of tracking individual breast amounts was an intentional decision made by the primary user of Open Baby. Contributions are welcome if there is demand for tracking individual breast pumping metrics.

### Log Diapers

Open Baby supports logging diaper events with the following attributes:

- Time of Diaper
- Type (Pee, Poop, Both)
- Color (Brown, Yellow, Black, Green)
- Consistency (Watery, Paste)
- Amount (Small, Medium, Large)


## Technical Implementation

Open Baby is comprised of two main components: the backend and the frontend.

The backend is written in Python, using FastAPI.

The frontend is written in Typescript using Nuxt 3.

