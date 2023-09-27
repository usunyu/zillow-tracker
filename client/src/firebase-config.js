// Import the functions you need from the SDKs you need
import { initializeApp } from 'firebase/app';
import { getAnalytics } from 'firebase/analytics';
import { getFirestore } from 'firebase/firestore';
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: 'AIzaSyDjuKzfM-WSq6HHxEqFHn6O8LC2b36q1Ow',
  authDomain: 'zillow-tracker-project.firebaseapp.com',
  projectId: 'zillow-tracker-project',
  storageBucket: 'zillow-tracker-project.appspot.com',
  messagingSenderId: '782345412218',
  appId: '1:782345412218:web:f555bd87443f18c336a5c3',
  measurementId: 'G-BH47SBWL30',
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Init services
export const db = getFirestore(app);
