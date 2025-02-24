<script setup>
import { ref, onMounted, computed } from "vue";
import { getAuth, onAuthStateChanged, signOut } from "firebase/auth";
import { useRouter, useRoute } from "vue-router";
import { getFirestore, doc, getDoc } from "firebase/firestore";

const auth = getAuth();
const db = getFirestore();
const router = useRouter();
const route = useRoute();
const isAuthenticated = ref(false);

// Hide navbar on SignIn and SignUp pages
const hideNavbar = computed(() => ["/SignIn", "/SignUp"].includes(route.path));

onMounted(() => {
  onAuthStateChanged(auth, async (user) => {
    if (user) {
      isAuthenticated.value = true;
      const userDoc = await getDoc(doc(db, "users", user.uid));

      if (userDoc.exists()) {
        const role = userDoc.data().role;

        // Redirect only if user is NOT on SignIn or SignUp page
        if (!hideNavbar.value) {
          router.push(role === "teacher" ? "/TeacherDashboard" : "/StudentDashboard");
        }
      }
    } else {
      isAuthenticated.value = false;

      // Ensure only redirecting if not already on SignIn page
      if (!hideNavbar.value) {
        router.push("/SignIn");
      }
    }
  });
});

// 🔹 Centralized Sign-Out Function
const handleSignOut = async () => {
  try {
    await signOut(auth);
    isAuthenticated.value = false;
    router.push("/SignIn");
  } catch (error) {
    console.error("Sign Out Failed", error);
  }
};
</script>

<template>
  <div class="flex flex-col items-center justify-center h-screen bg-gray-100">
    <!-- Hide Navbar on SignIn & SignUp -->
    <nav v-if="!hideNavbar" class="bg-white p-4 rounded shadow mt-20">
      <template v-if="isAuthenticated">
        <button 
          @click="handleSignOut" 
          class="ml-4 bg-red-500 text-white px-4 py-2 rounded cursor-pointer hover:bg-red-600">
          Sign Out
        </button>
      </template>
      <template v-else>
        <router-link to="/" class="mr-4 text-2xl text-blue-500 hover:text-blue-700">Home</router-link>
        <router-link to="/SignIn" class="mr-4 text-2xl text-blue-500 hover:text-blue-700">Sign In</router-link>
        <router-link to="/SignUp" class="text-2xl text-blue-500 hover:text-blue-700">Sign Up</router-link>
      </template>
    </nav>

    <router-view />
  </div>
</template>
