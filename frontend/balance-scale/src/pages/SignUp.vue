<template>
  <div>
    <h1>Create an Account</h1>
    <p><input type="text" placeholder="Email" v-model="email"/></p>
    <p><input type="password" placeholder="Password" v-model="password"></p>
    <p><button @click="register">Submit</button></p>
    <p><button @click="signInWithGoogle"> Sign in with Google</button></p>
  </div>
</template>
 
<script setup>
import {ref} from "vue";
import { getAuth, onAuthStateChanged,createUserWithEmailAndPassword } from "firebase/auth";
import {useRouter} from 'vue-router';
const email=ref("");
const password=ref("");
const router = useRouter();

const register = ()=>{
    const auth = getAuth();
    createUserWithEmailAndPassword(getAuth(),email.value, password.value)
    .then((data)=>{
      console.log("Successfully Registered !");
      router.push('/SignIn');
    })
    .catch((error)=>{
      console.log(error.code);
      alert(error.message);
    })
};
const signInWithGoogle=()=>{

}

</script>
