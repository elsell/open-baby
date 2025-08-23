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

## Quick Start

The quickest way to get started with Open Baby is using [Docker Compose](https://docs.docker.com/compose/).

### Step 1: Create Configuration Files

Open Baby uses `.env` files for configuration. Create two files within a directory
called `env` (at the same level as `compose.yaml`):

```bash
# env/frontend.env
NUXT_PUBLIC_API_BASE=http://192.168.1.204:8000 # Replace 192.168.1.204 with the IP of the computer running Open Baby.
```

You must create `backend.env`, but you don't need to include any configuration options.
Optionally, you can specify to use a development environment configuration:
```bash
# env/backend.env
ENVIRONMENT=dev
```

### Step 2: Run Open Baby

Assuming that you have [installed Docker Compose](https://docs.docker.com/compose/install/), simply run the following command from the root of the repository:

```bash
sudo docker compose up
```

You then can access Open Baby in your web browser at http://localhost:3000!

## Features

### Log Feedings

Open Baby supports both bottle and breast feedings, and allows
tracking the following attributes:

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

