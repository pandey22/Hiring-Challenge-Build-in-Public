<script setup>
import { ref, onMounted, computed } from "vue";
import { getFirestore, doc, getDoc, setDoc } from "firebase/firestore";
import { getAuth } from "firebase/auth";

const db = getFirestore();
const auth = getAuth();
const targetNumber = ref(0);
const givenNumber = ref(0);
const userInput = ref(null);
const feedback = ref("Fill in the missing number!");
const highScore = ref(0);
const currentScore = ref(0);

const generateTarget = () => {
  targetNumber.value = Math.floor(Math.random() * 50) + 10;
  givenNumber.value = Math.floor(Math.random() * (targetNumber.value - 5)) + 1;
  userInput.value = null;
  feedback.value = "Fill in the missing number!";
};

const checkBalance = () => {
  if (parseInt(userInput.value) + givenNumber.value === targetNumber.value) {
    feedback.value = "🎯 Correct! The scale is balanced!";
    currentScore.value += 1;

    if (currentScore.value > highScore.value) {
      highScore.value = currentScore.value;
      updateHighScore();
    }
    
    setTimeout(generateTarget, 1000);
  } else {
    feedback.value = "❌ Incorrect! Try again.";
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
  const sum = (userInput.value ? parseInt(userInput.value) : 0) + givenNumber.value;
  const ratio = sum / targetNumber.value;

  if (sum === targetNumber.value) return "rotate(0deg)";
  if (sum < targetNumber.value) return `rotate(${-Math.max(30 - ratio * 30, 5)}deg)`;
  return `rotate(${Math.min(ratio * 30, 30)}deg)`;
});
</script>

<template>
  <div class="flex flex-col items-center bg-gray-100 min-h-screen p-6">
    <h1 class="text-5xl font-bold text-yellow-500 mb-4">Balance Scale Addition Game</h1>
    
    <p class="text-2xl font-semibold"> Target Number: <span class="text-green-600">{{ targetNumber }}</span></p>
    <p class="text-lg font-semibold text-gray-800">{{ feedback }}</p>
    <p class="text-lg"> Current Score: <span class="font-semibold text-blue-500">{{ currentScore }}</span></p>
    <p class="text-lg">🏅 High Score: <span class="font-semibold text-yellow-500">{{ highScore }}</span></p>

    <div class="relative flex justify-center items-center my-6">
      <div class="relative w-64 h-64 rounded-full bg-gray-300 flex items-center justify-center border-4 border-black">
        <!-- Scale Indicator -->
        <div 
          class="absolute w-1 h-24 bg-red-600 origin-bottom transition-transform duration-500 ease-in-out" 
          :style="{ transform: scaleTilt }">
        </div>
        
        <!-- Labels Positioned Inside the Scale -->
        <span class="absolute left-10 bottom-8 text-lg font-bold text-gray-800">Low</span>
        <span class="absolute top-10 left-1/2 transform -translate-x-1/2 text-xl font-semibold text-gray-800">Perfect</span>
        <span class="absolute right-10 bottom-8 text-lg font-bold text-gray-800">High</span>
      </div>
    </div>

    <p class="text-lg mb-2"> Fill in the blank: <span class="font-semibold">? + {{ givenNumber }} = {{ targetNumber }}</span></p>
    <input 
      type="number" 
      v-model.number="userInput" 
      placeholder=" Enter the number" 
      class="border border-gray-400 rounded-md p-2 w-40 text-center mb-4"
    />
    
    <button 
      @click="checkBalance" 
      class="px-6 py-2 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700 transition"
    >
      Submit
    </button>
  </div>
</template>

