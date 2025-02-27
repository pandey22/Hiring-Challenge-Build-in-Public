# Balance Scale Addition Game

## Overview
This is an interactive educational game designed to help students understand addition through a balance scale visualization. The goal is to select numbers that add up to a target value while receiving real-time feedback through a scale meter that tilts based on their input.


## Technologies Used
- Vue.js (Composition API)
- Firebase Authentication (Email/Password, Google Sign-In)
- Firebase Firestore (High score persistence)
- Tailwind CSS

## Setup Instructions

### Prerequisites
- Node.js (>= 14.x)
- Firebase account and project setup
- Vue.js installed globally

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/pandey22/Hiring-Challenge-Build-in-Public.git
   cd frontend
   cd balance-scale
   ```

2. Install dependencies:
   ```sh
   npm install
   ```

3. Configure Firebase:
   - Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
   - Enable **Authentication** (Email/Password, Google Sign-In)
   - Enable **Firestore Database**
   - Get your Firebase config from project settings and update `main.js`:
     ```js
     import { initializeApp } from "firebase/app";
     
     const firebaseConfig = {
       apiKey: "YOUR_API_KEY",
       authDomain: "YOUR_AUTH_DOMAIN",
       projectId: "YOUR_PROJECT_ID",
       storageBucket: "YOUR_STORAGE_BUCKET",
       messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
       appId: "YOUR_APP_ID"
     };
     
     export const app = initializeApp(firebaseConfig);
     ```

### Running the Project

1. Start the development server:
   ```sh
   npm run dev
   ```

2. Open the project in your browser:
   ```sh
   http://localhost:5173
   ```
3. To run backend server
    ```sh
    cd backend
    ```
    ```sh
    uvicorn main:app --reload
    ```


## Authentication

### Sign Up
Users can sign up using their email and password. The authentication data is managed through Firebase.

### Sign In
Users can sign in using either:
- Email & Password
- Google Authentication (If the user already exists in Firebase)

### Sign Out
Authenticated users can sign out from the dashboard.

## Game Mechanics
1. The game starts with a random **target number**.
2. Users add numbers until the sum reaches the target.
3. If the sum exceeds the target, the game resets the total to zero.
4. The scale  adjusts based on how close the user is.
5. Correct answers increase the high score, which is stored in Firebase.

