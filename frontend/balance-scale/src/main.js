import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import router from "./router";
import { initializeApp } from "firebase/app";
import { getAuth, signInWithPopup, GoogleAuthProvider } from "firebase/auth";
import axios from "axios";

// Firebase Configuration
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID
};

// Initialize Firebase
const firebaseApp = initializeApp(firebaseConfig);
const auth = getAuth(firebaseApp);

// Firebase Sign-In Function
async function signInWithGoogle() {
  const provider = new GoogleAuthProvider();
  try {
    const result = await signInWithPopup(auth, provider);
    const idToken = await result.user.getIdToken();  // Get Firebase ID Token
    
    // Send token to FastAPI for verification
    const response = await axios.post("http://localhost:8000/verify", { token: idToken });
    
    // Redirect user based on role
    const role = response.data.role;
    if (role === "teacher") {
      router.push("/TeacherDashboard");  // Admin panel for teachers
    } else {
      router.push("/StudentDashboard");  // Game page for students
    }
  } catch (error) {
    console.error("Authentication Error:", error);
  }
}

// Vue App Instance
const app = createApp(App);
app.use(router);
app.config.globalProperties.$signInWithGoogle = signInWithGoogle;
app.mount('#app');
