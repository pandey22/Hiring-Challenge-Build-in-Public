<script setup>
import { ref } from "vue";
import { getAuth, createUserWithEmailAndPassword, deleteUser } from "firebase/auth";
import { useRouter } from "vue-router";
import { getFirestore, doc, setDoc, deleteDoc } from "firebase/firestore";

const auth = getAuth();
const db = getFirestore();
const router = useRouter();

const email = ref("");
const password = ref("");
const role = ref("student"); // Default role
const errorMessage = ref("");

const signUp = async () => {
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email.value, password.value);
    const user = userCredential.user;

    // ✅ Store BOTH email & role in Firestore
    await setDoc(doc(db, "users", user.uid), {
      email: email.value, // 🔹 Save user email
      role: role.value,   // 🔹 Save user role
    });

    // ✅ Redirect to SignIn (fixes unwanted redirection to game)
    router.push("/SignIn");
  } catch (error) {
    console.error("Sign-Up Error:", error);
    errorMessage.value = "Error creating account. Please try again.";
  }
};

// 🔹 Permanently delete user
const deleteUserAccount = async () => {
  const user = auth.currentUser;
  if (!user) return;

  try {
    await deleteDoc(doc(db, "users", user.uid)); // Delete from Firestore
    await deleteUser(user); // Delete from Firebase Authentication
    console.log("User permanently deleted.");
    router.push("/SignIn");
  } catch (error) {
    console.error("Error deleting user:", error);
  }
};
</script>

<template>
  <div class="font-sans min-h-screen flex flex-col sm:justify-center items-center bg-gray-100">
    <div class="relative sm:max-w-md w-full">
      <div class="card bg-blue-400 shadow-lg w-full h-full rounded-3xl absolute transform -rotate-6"></div>
      <div class="card bg-red-400 shadow-lg w-full h-full rounded-3xl absolute transform rotate-6"></div>
      <div class="relative w-full rounded-3xl px-8 py-6 bg-gray-100 shadow-md">
        <label class="block mt-3 text-lg text-gray-700 text-center font-semibold">Sign Up</label>
        <form @submit.prevent="signUp" class="mt-10">
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
            <select 
              v-model="role" 
              class="mt-1 block w-full border-none bg-gray-100 h-12 rounded-xl shadow-lg hover:bg-blue-100 focus:bg-blue-100 focus:ring-0 px-4 cursor-pointer"
            >
              <option value="student">Student</option>
              <option value="teacher">Teacher</option>
            </select>
          </div>
          <div class="mt-7">
            <button 
              type="submit" 
              class="bg-blue-500 w-full py-3 rounded-xl text-white shadow-xl hover:shadow-inner focus:outline-none transition duration-500 ease-in-out transform hover:-translate-x hover:scale-105 cursor-pointer"
            >
              Sign Up
            </button>
          </div>
          <div class="flex mt-7 items-center text-center">
            <hr class="border-gray-300 border-1 w-full rounded-md">
            <label class="block font-medium text-sm text-gray-600 w-full">Comini Learning</label>
            <hr class="border-gray-300 border-1 w-full rounded-md">
          </div>
          <p v-if="errorMessage" class="text-red-600 text-center mt-4 font-semibold">{{ errorMessage }}</p>
          <div class="mt-7 flex justify-center items-center">
            <label class="mr-2">Already have an account?</label>
            <a href="/SignIn" class="text-blue-500 font-semibold transition duration-500 ease-in-out transform hover:-translate-x hover:scale-105 cursor-pointer">Sign In</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
