import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import router from "./router";
import { initializeApp } from "firebase/app";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBwB-_o4QbsLm-lEPNyIM4djFf240hoNnw",
  authDomain: "balance-scale-7aaba.firebaseapp.com",
  projectId: "balance-scale-7aaba",
  storageBucket: "balance-scale-7aaba.firebasestorage.app",
  messagingSenderId: "795955573290",
  appId: "1:795955573290:web:6c736d83686a5fe57c0953",
  measurementId: "G-CQT2VG4JPQ"
};

// Initialize Firebase
initializeApp(firebaseConfig);
const app = createApp(App)

app.use(router)

app.mount('#app')