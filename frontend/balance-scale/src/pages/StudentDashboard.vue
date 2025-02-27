<template>
  <div class="flex flex-col items-center bg-gradient-to-b from-gary-100 to-gary-100 min-h-screen p-4 md:p-6">
    <div class="w-full max-w-7xl">
      <!-- Header Section -->
      <div class="flex flex-col md:flex-row justify-between items-center mb-6 text-center md:text-left">
        <h1 class="text-4xl md:text-5xl font-bold text-blue-600 mb-4 md:mb-0">Balance the Scale!</h1>
        <div class=" ml-9 flex flex-col md:flex-row gap-4 md:gap-8">
          <div class="flex gap-4 md:gap-6">
            <div class="bg-cyan-300 p-3 md:p-4 rounded-lg shadow-md text-lg md:text-xl">
              <p>Score: <span class="font-semibold text-black-600">{{ currentScore }}</span></p>
            </div>
            <div class="bg-white p-3 md:p-4 rounded-lg shadow-md text-lg md:text-xl">
              <p>🏆 High: <span class="font-semibold text-yellow-600">{{ highScore }}</span></p>
            </div>
          </div>
        </div>
      </div>

      <!-- Feedback Section -->
      <div class="mb-6 bg-white py-3 px-4 md:px-6 rounded-lg shadow-md text-center w-full">
        <p class="text-lg md:text-xl font-semibold" :class="{ 'text-green-600': feedback.includes('Balanced'), 'text-red-600': feedback.includes('Too heavy') }">
          {{ feedback }}
        </p>
      </div>

      <!-- Balance Scale -->
      <div class="relative w-full h-64 sm:h-80 flex justify-center items-center mt-6">  <!-- Adjusted centering -->
        <div class="relative w-11/12 max-w-3xl h-3 bg-gray-500 rounded-md transition-transform duration-700" :style="{ transform: scaleTilt }">
          <div class="absolute -left-28 top-[-42px] w-32 sm:w-40 flex flex-col items-center">  <!-- Moved up -->
            <div class="flex flex-wrap justify-center -mt-8">  <!-- Increased spacing -->
              <div v-for="n in leftBalls" :key="`left-${n}`" class="w-4 h-4 sm:w-6 sm:h-6 bg-gray-700 rounded-full m-1 shadow-md"></div>
            </div>
            <div class="mb-2 h-4 sm:h-6 bg-gray-500 rounded-md shadow-md w-full"></div>
          </div>

          <div class="absolute -right-24 top-[-20px] w-32 sm:w-40 flex flex-col items-center">  <!-- Adjusted alignment -->
            <div class="flex flex-wrap justify-center -mt-6">
              <div v-for="n in rightBalls" :key="`right-${n}`" class="w-4 h-4 sm:w-6 sm:h-6 bg-blue-600 rounded-full m-1 shadow-md"></div>
            </div>
            <div class="-mb-1 h-4 sm:h-6 bg-gray-500 rounded-md shadow-md w-full"></div>  <!-- Adjusted position -->
          </div>
        </div>

        <!-- Center Fulcrum -->
        <div class="absolute bottom-19 w-0 h-0 border-l-[20px] sm:border-l-[40px] border-r-[20px] sm:border-r-[40px] border-t-[40px] sm:border-t-[80px] border-gray-800"></div>
      </div>

      <!-- Controls Section -->
      <div class="w-full bg-white rounded-xl shadow-lg p-4 md:p-6 mt-2">
        <p class="text-lg md:text-xl text-center text-gray-700 mb-4">Select a weight to add on the right side:</p>
        <div class="flex justify-center flex-wrap gap-3 md:gap-6">
          <button 
            v-for="number in numberChoices" 
            :key="number" 
            @click="checkBalance(number)" 
            class="w-12 h-12 md:w-16 md:h-16 flex items-center justify-center bg-blue-600 text-white text-xl md:text-2xl font-bold rounded-full hover:bg-blue-700 transition transform hover:scale-110 shadow-md">
            {{ number }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { getFirestore, doc, getDoc, setDoc } from "firebase/firestore";
import { getAuth } from "firebase/auth";

const db = getFirestore();
const auth = getAuth();
const leftBalls = ref(0);
const rightBalls = ref(0);
const highScore = ref(0);
const currentScore = ref(0);
const numberChoices = ref([]);
const feedback = ref("Select a number to balance the scale!");

const generateTarget = () => {
  leftBalls.value = Math.floor(Math.random() * 10) + 5;
  rightBalls.value = 0;
  feedback.value = "Select a number to balance the scale!";
  const exactMatch = leftBalls.value;
  const part1 = Math.floor(Math.random() * (leftBalls.value - 1)) + 1;
  const part2 = leftBalls.value - part1;
  numberChoices.value = [exactMatch, part1, part2].sort(() => Math.random() - 0.5);
};

const checkBalance = (selectedNumber) => {
  rightBalls.value += selectedNumber;
  if (rightBalls.value === leftBalls.value) {
    feedback.value = "🎯 Balanced!";
    currentScore.value += 1;
    if (currentScore.value > highScore.value) {
      highScore.value = currentScore.value;
      updateHighScore();
    }
    setTimeout(generateTarget, 1500);
  } else if (rightBalls.value > leftBalls.value) {
    feedback.value = "❌ Too heavy! Resetting...";
    currentScore.value = 0;
    setTimeout(generateTarget, 1500);
  } else {
    feedback.value = "Not balanced yet. Add more weight!";
  }
};

const updateHighScore = async () => {
  const user = auth.currentUser;
  if (user) {
    await setDoc(doc(db, "users", user.uid), { highScore: highScore.value }, { merge: true });
  }
};

const fetchHighScore = async () => {
  const user = auth.currentUser;
  if (user) {
    const userDoc = await getDoc(doc(db, "users", user.uid));
    if (userDoc.exists()) {
      highScore.value = userDoc.data().highScore || 0;
    }
  }
};

onMounted(() => {
  generateTarget();
  fetchHighScore();
});

const scaleTilt = computed(() => {
  const difference = leftBalls.value - rightBalls.value;
  return `rotate(${Math.min(Math.max(difference * 0.5, -8), 8)}deg)`;
});
</script>
