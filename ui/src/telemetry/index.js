// Import the functions you need from the SDKs you need
import  { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import firebase from "firebase/compat/app";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
export const firebaseConfig = {
  apiKey: "AIzaSyACE4Kid9-ue0Sdfh39kgVLrh13qPYsZl4",
  authDomain: "cueobserve-3b1e1.firebaseapp.com",
  projectId: "cueobserve-3b1e1",
  storageBucket: "cueobserve-3b1e1.appspot.com",
  messagingSenderId: "551390041392",
  appId: "1:551390041392:web:df6373ea8fe8178476a4f5",
  measurementId: "G-SHS7Q15FSS"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const firebaseAnalytics = getAnalytics(app);
