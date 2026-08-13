<div align="center">

# Alfath Asqar Tsani

**Software Engineering · Platform Systems · Data Infrastructure**

Computer Science at IPB University  
Bogor, Indonesia

<a href="https://www.linkedin.com/in/asqaraa">LinkedIn</a>
&nbsp;&nbsp;·&nbsp;&nbsp;
<a href="mailto:Alfath.asqartsani@gmail.com">Email</a>
&nbsp;&nbsp;·&nbsp;&nbsp;
<a href="#selected-systems">Selected Work</a>

</div>

<br>

<table>
<tr>
<td align="center" width="33%">
<h3>~8,000</h3>
<sub>student records managed</sub>
</td>
<td align="center" width="33%">
<h3>~1,000 RPS</h3>
<sub>peak production load</sub>
</td>
<td align="center" width="33%">
<h3>Rp600M+</h3>
<sub>transaction value handled</sub>
</td>
</tr>
</table>

<br>

## About

I'm a Computer Science student at **IPB University** working across
full-stack development, backend systems, data infrastructure, and production operations.

Most of my recent work involves building systems that support real operational
workflows at university scale — from internal ERP and participant platforms to
data pipelines, commerce systems, ticketing, automation, and Kubernetes infrastructure.

I currently work mostly with **TypeScript, Next.js, Bun, PostgreSQL, Docker,
and Kubernetes**, while also maintaining experience with Laravel, Python,
automation, and data analysis.

---

## Selected Systems

<table>
<tr>
<td width="50%" valign="top">

### MySOC

**Integrated ERP · OMB IPB 63 × Agrisymphony 2026**

Internal operational platform connecting committee workflows, participant
management, administration, and institutional stakeholders.

**What I worked on**

- Microservices-oriented architecture
- Role-Based Access Control
- Cross-service data integration
- Internal operational workflows
- Deployment and service operations
- Kubernetes-based infrastructure

**Core stack**

`Next.js` `Bun` `PostgreSQL` `Drizzle ORM`  
`Docker` `Kubernetes` `Redis`

</td>

<td width="50%" valign="top">

### StudentOrientation

**Student Platform · IPB University**

Central student-facing system supporting university orientation and related
digital services.

**What I worked on**

- Student data cleaning and normalization
- Data management for ~8,000 students
- Digital attendance infrastructure
- Participant grouping and authentication
- Helpdesk and information services
- Integration with internal systems

The platform received organic attention on X for its digital orientation
implementation and became a reference for similar initiatives elsewhere.

**Core stack**

`Next.js` `PostgreSQL` `React Query`  
`next-intl` `Tailwind CSS`

</td>
</tr>

<tr>
<td width="50%" valign="top">

### Agrisymphony Store

**Commerce Platform**

Digital merchandise platform built to manage products, orders, and transaction
workflows for MPKMB and Agrisymphony.

**Scale**

**Rp600M+ cumulative transaction value**

The system supported real production transactions and the operational process
behind merchandise distribution.

**Focus**

`Commerce` `Transactions` `Database`  
`Order Management` `Production`

</td>

<td width="50%" valign="top">

### Agrisymphony

**Public Website & Ticketing**

Developed digital services supporting Agrisymphony, including the official
website and event ticketing system.

**Scale**

**1,000+ ticket sales processed**

Worked on application development, transaction workflows, deployment, and
production maintenance.

**Focus**

`Web Development` `Ticketing`  
`Transactions` `Production`

</td>
</tr>
</table>

---

## Platform Engineering

A large part of my recent work sits beyond the application layer.

I work on the infrastructure needed to keep multiple interconnected services
available during real production usage.

```text
                            ┌────────────────────┐
                            │      Clients       │
                            └─────────┬──────────┘
                                      │
                                      ▼
                            ┌────────────────────┐
                            │   Web Applications │
                            └─────────┬──────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
                    ▼                                   ▼
          ┌──────────────────┐                ┌──────────────────┐
          │ Application APIs │                │ Internal Services│
          └────────┬─────────┘                └────────┬─────────┘
                   │                                   │
                   └─────────────────┬─────────────────┘
                                     ▼
                           ┌────────────────────┐
                           │ PostgreSQL / Redis │
                           └─────────┬──────────┘
                                     │
                                     ▼
                           ┌────────────────────┐
                           │ Docker / Kubernetes│
                           └────────────────────┘
````

Areas I have worked on include:

* containerized application deployment
* Kubernetes / k3s orchestration
* horizontal service scaling
* high-traffic application handling
* application and service recovery
* database operations
* production maintenance
* system integration
* authentication and authorization
* incident handling

Production infrastructure has handled peak traffic of approximately
**1,000 requests per second**.

---

## Data Infrastructure

Some of the systems I build depend on data coming from different sources,
formats, and operational units.

For OMB IPB 63, I worked on preparing and structuring data for approximately
**8,000 incoming students**.

```text
Raw Sources
     │
     ▼
Data Cleaning
     │
     ▼
Validation
     │
     ▼
Normalization
     │
     ▼
Centralized Student Data
     │
     ├── Digital Attendance
     ├── Participant Grouping
     ├── Authentication
     ├── Helpdesk
     ├── Student Services
     └── Internal Operations
```

The goal was not simply storing data, but making the same structured data
reusable and consistent across different operational systems.

---

## Engineering Stack

<table>
<tr>
<td width="25%" valign="top">

**Languages**

`TypeScript`
`JavaScript`
`Python`
`PHP`
`C++`
`Java`

</td>

<td width="25%" valign="top">

**Application**

`Next.js`
`React`
`Laravel`
`Inertia.js`
`Bun`
`Tailwind CSS`
`Framer Motion`

</td>

<td width="25%" valign="top">

**Data**

`PostgreSQL`
`Redis`
`MySQL`
`MongoDB`
`Drizzle ORM`
`SQL`

</td>

<td width="25%" valign="top">

**Infrastructure**

`Kubernetes`
`k3s`
`Docker`
`Linux`
`Git`
`GitHub`

</td>
</tr>

<tr>
<td width="25%" valign="top">

**Frontend Tooling**

`React Query`
`next-intl`
`pnpm`

</td>

<td width="25%" valign="top">

**Automation**

`n8n`
`Playwright`
`Baileys`

</td>

<td width="25%" valign="top">

**Data & Analysis**

`Python`
`SQL`
`Spreadsheet`

</td>

<td width="25%" valign="top">

**Product**

`Figma`
`REST API`
`RBAC`
`Microservices`

</td>
</tr>
</table>

---

## Other Engineering Work

### Code Panda

**Web Developer · 2025 — Present**

Working on production web applications across Laravel, Inertia.js, and Next.js.

* Developed a Learning Management System for MBKM-related workflows
* Worked across development, debugging, and maintenance
* Optimized a Next.js application and improved page-load performance by ~60%

<br>

### WhatsApp Automation

Built WhatsApp-based systems using **Baileys** for student services and
operational automation.

Work includes:

* automated student helpdesk
* broadcast workflows
* batch message processing
* session handling
* internal service automation

<br>

### Moodle Automation

Worked with **Playwright** to automate browser-based operational workflows,
including participant management and repetitive administrative processes.

<br>

### Research Data

Worked on quantitative research involving **700+ respondents**, using
Python and spreadsheets to process survey results and translate them into
organizational insights.

---

## Experience

<table>
<tr>
<td width="23%"><strong>2025 — Present</strong></td>
<td>
<strong>Web Developer</strong><br>
Code Panda
</td>
</tr>

<tr>
<td><strong>2025 — Present</strong></td>
<td>
<strong>Information Systems Coordinator</strong><br>
OMB IPB 63 × Agrisymphony 2026
</td>
</tr>

<tr>
<td><strong>2025</strong></td>
<td>
<strong>Web Developer</strong><br>
Agrisymphony
</td>
</tr>

<tr>
<td><strong>2025</strong></td>
<td>
<strong>Head of Research & Development</strong><br>
Ormawa Eksekutif PKU IPB
</td>
</tr>

<tr>
<td><strong>2024</strong></td>
<td>
<strong>Data Operations</strong><br>
Balai Penyuluhan Pertanian Bekri
</td>
</tr>
</table>

---

## Education & Certification

<table>
<tr>
<td width="65%" valign="top">

### IPB University

**B.Sc. Computer Science**

GPA **3.80 / 4.00**
Expected graduation: 2028

Recipient of the **Yayasan Alumni Peduli IPB Scholarship**.

</td>

<td width="35%" valign="top">

### BNSP

**Web Developer Competency Certification**

Badan Nasional Sertifikasi Profesi

</td>
</tr>
</table>

---

## Outside the Main Stack

I have also worked on projects involving:

* AI / LLM-assisted applications
* WhatsApp service automation
* research and quantitative data analysis
* agricultural government data systems
* internal organizational digitalization
* event operations and transaction systems

These projects gave me experience working not only with code, but also with
messy requirements, real users, operational constraints, and systems that
need to remain usable after deployment.

---

## GitHub

<!-- Replace YOUR_USERNAME with your actual GitHub username -->

<p align="center">
  <img
    width="49%"
    src="https://github-readme-stats.vercel.app/api?username=YOUR_USERNAME&show_icons=true&hide_border=true&hide_title=true&include_all_commits=true"
    alt="GitHub statistics"
  />
  <img
    width="37%"
    src="https://github-readme-stats.vercel.app/api/top-langs/?username=YOUR_USERNAME&layout=compact&hide_border=true&hide_title=true"
    alt="Most used languages"
  />
</p>

---

<div align="center">

### Alfath Asqar Tsani

Software Engineering · Backend Systems · Infrastructure

<a href="mailto:Alfath.asqartsani@gmail.com">Email</a>
  ·   <a href="https://www.linkedin.com/in/asqaraa">LinkedIn</a>

</div>
