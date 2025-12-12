# Inventory Management MEAN Application

A full-stack **Inventory Management System** built using the **MEAN stack** — MongoDB, Express.js, Angular, and Node.js — that enables users to manage inventory items through a modern user interface and secure backend API.

---

### Login Page
![Login Page](screenshots/login.png)
*Secure authentication with JWT tokens*

### Inventory Dashboard
![Inventory Dashboard](screenshots/dashboard.png)
*View and manage all inventory items with edit and delete actions*

### Add New Item
![Add Item Page](screenshots/add-item.png)
*Simple form interface for adding new inventory items*

---

## Features

### Frontend (Angular 21)
- Built with **Angular 21 (v21 workspace)**
- **Angular Material** UI components with custom theming (`custom-theme.scss`)
- **Service-based** API communication
- **Authentication-aware UI** (login/register state)
- CRUD interface for item management
- Modern styling and responsive layout

### Backend (Node.js + Express)
- RESTful API built using **Express 5**
- MongoDB data storage via **Mongoose**
- **JWT-based Authentication** (jsonwebtoken)
- Password hashing using **bcrypt**
- Environment configuration with **dotenv**
- **CORS**-enabled secure communication
- **Auto-reload** during development with nodemon

---

## Installation & Setup

### 1. Clone the Repository

*git clone https://github.com/KingQueso12/ePortfolio/Enhanced Projects/inventory-meanapp.git*

*cd inventory-meanapp*

---

### 2. Server Setup (Node + Express)

**Install dependencies:**

*cd server*
*npm install*


**Create a `.env` file:**

*MONGO_URI=mongodb://localhost:27017/inventoryDB*
*JWT_SECRET=yourSecretKey*
*PORT=5000*

**Run the server:**

*npm run dev # uses nodemon*

or

*npm start*


The backend runs on:  
 [http://localhost:5000](http://localhost:5000)

**Backend Dependencies:**
- express  
- mongoose  
- bcrypt  
- jsonwebtoken  
- dotenv  
- cors  
- nodemon (dev)

---

### 3. Client Setup (Angular)

**Install dependencies:**

*cd client*
*npm install*


**Run Angular development server:**

*npm start*

The Angular client runs on:  
[http://localhost:4200](http://localhost:4200)

**Angular build configuration** (assets, styles, environments) is defined in `angular.json`.

---

## Connecting Client and Server

In your Angular services, set the API base URL to:

*http://localhost:5000/api/...*

Ensure **CORS** is enabled in your Express server (already included in dependencies).

---

## Testing

**Angular Unit Tests:**

*ng test*

---

## Authentication Overview

- Passwords hashed using **bcrypt**
- **JWT tokens** used for session management and route protection
- Authentication middleware secures private routes

---

## Database Information

- Uses **MongoDB** with **Mongoose ODM**
- Default local storage path:

C:\Users(<b>YourName</b>)\AppData\Local\MongoDB\

- For **MongoDB Atlas**, update your `.env`:

MONGO_URI=mongodb+srv://<b>username</b>:<b>password</b>@<b>cluster-url</b>/inventoryDB

---

## Technologies Used

| Layer | Technologies |
|-------|---------------|
| **Frontend** | Angular 21, Angular Material, TypeScript, RxJS |
| **Backend** | Node.js, Express.js, Mongoose/MongoDB, JWT, bcrypt |

---


## Author

**Morgan Tyler Kazee**  
💻 Computer Science & Full-Stack Developer
