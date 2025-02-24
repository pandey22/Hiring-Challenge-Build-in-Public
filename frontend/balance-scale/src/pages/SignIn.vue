<script setup>
import { ref } from "vue";
import { getAuth, signInWithEmailAndPassword, signInWithPopup, GoogleAuthProvider } from "firebase/auth";
import { useRouter } from "vue-router";
import { getFirestore, doc, getDoc } from "firebase/firestore";

const auth = getAuth();
const db = getFirestore();
const provider = new GoogleAuthProvider();
const router = useRouter();

const email = ref("");
const password = ref("");
const errorMessage = ref("");

async function getUserRole(userId) {
  try {
    const userDoc = await getDoc(doc(db, "users", userId));
    return userDoc.exists() ? userDoc.data().role : null;
  } catch (error) {
    console.error("Error fetching user role:", error);
    return null;
  }
}

// 🔹 Sign in with Email
const signInWithEmail = async () => {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email.value, password.value);
    const role = await getUserRole(userCredential.user.uid);

    if (role === "teacher") {
      router.push("/TeacherDashboard");
    } else {
      router.push("/StudentDashboard");
    }
  } catch (error) {
    console.error("Email Login Error:", error);
    errorMessage.value = "Incorrect email or password. Please try again.";
  }
};

// 🔹 Sign in with Google
const signInWithGoogle = async () => {
  try {
    const result = await signInWithPopup(auth, provider);
    const role = await getUserRole(result.user.uid);

    if (role === "teacher") {
      router.push("/TeacherDashboard");
    } else {
      router.push("/StudentDashboard");
    }
  } catch (error) {
    console.error("Google Login Error:", error);
    errorMessage.value = "Google sign-in failed. Please try again.";
  }
};
</script>

<template>
  <div class="font-sans min-h-screen flex flex-col sm:justify-center items-center bg-gray-100">
    <div class="relative sm:max-w-md w-full"> 
      <div class="card bg-blue-400 shadow-lg w-full h-full rounded-3xl absolute transform -rotate-6"></div>
      <div class="card bg-red-400 shadow-lg w-full h-full rounded-3xl absolute transform rotate-6"></div>
      <div class="relative w-full rounded-3xl px-8 py-6 bg-gray-100 shadow-md">
        <label class="block mt-3 text-lg text-gray-700 text-center font-semibold">Sign In</label>
        <form @submit.prevent="signInWithEmail" class="mt-10">
          <div>
            <input 
              v-model="email" 
              type="email" 
              placeholder="Email" 
              class="mt-1 block w-full border-none bg-gray-100 h-12 rounded-xl shadow-lg hover:bg-blue-100 focus:bg-blue-100 focus:ring-0 px-4"
            />
          </div>
          <div class="mt-7">
            <input 
              v-model="password" 
              type="password" 
              placeholder="Password" 
              class="mt-1 block w-full border-none bg-gray-100 h-12 rounded-xl shadow-lg hover:bg-blue-100 focus:bg-blue-100 focus:ring-0 px-4"
            />
          </div>
          <div class="mt-7">
            <button 
              type="submit" 
              class="bg-blue-500 w-full py-3 rounded-xl text-white shadow-xl hover:shadow-inner focus:outline-none transition duration-500 ease-in-out transform hover:-translate-x hover:scale-105 cursor-pointer"
            >
              Login
            </button>
          </div>
          <div class="flex mt-7 items-center text-center">
            <hr class="border-gray-300 border-1 w-full rounded-md">
            <label class="block font-medium text-sm text-gray-600 w-full">Comini Learning</label>
            <hr class="border-gray-300 border-1 w-full rounded-md">
          </div>
          <div class="flex mt-7 justify-center w-full">
            <button 
              @click.prevent="signInWithGoogle" 
              class="bg-red-500 border-none px-6 py-3 rounded-xl cursor-pointer text-white shadow-xl hover:shadow-inner transition duration-500 ease-in-out transform hover:-translate-x hover:scale-105"
            >
              Sign in with Google
            </button>
          </div>
          <p v-if="errorMessage" class="text-red-600 text-center mt-4 font-semibold">{{ errorMessage }}</p>
          <div class="mt-7 flex justify-center items-center">
            <label class="mr-2">Not a user?</label>
            <router-link to="/SignUp" class="text-blue-500 font-semibold">Sign Up</router-link>
            
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
