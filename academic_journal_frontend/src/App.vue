<script>
import { RouterLink, RouterView } from 'vue-router';
import { tokenIsSet } from './service';
import { logout } from './network';

export default{
  methods: {
    toLogOut() {
      logout();
    }
  },
  data() {
    return {
      username: null,
      isAuth: null
    }
  },
  created() {
    // this.isAuth = tokenIsSet();
    if (tokenIsSet()) {
      this.isAuth = true;
      this.username = localStorage.getItem('username')
    }
    else {
      this.isAuth = false;
    }
  }
}

</script>

<template>
  <header>
    <div class="nav-wrapper">
      <nav class="navbar">
        <RouterLink to="/" class="link_reset">Home</RouterLink>
        <RouterLink to="/registration" class="link_reset" v-if="isAuth === false">Регистрация</RouterLink>
        <RouterLink to="/login" class="link_reset" v-if="isAuth === false">Авторизация</RouterLink>
        <button id="logout-button" @click="toLogOut">Выйти</button>
      </nav>
    </div>
  </header>
  

  <div class="wrapper">
    <RouterView />
  </div>

</template>

<style>
  :root {
    --amethyst: #7D70BA;
    --black: #000000;
    --lgreen: #4C9F70;
    --dgreen: #496F5D;
    --dpurple: #161032;
    --white-smoke: #F2F4F3;
  }

  body {
    background-color: var(--white-smoke);
    padding: 0;
    margin: 0;
  }

  .nav-wrapper {
    display: flex;
    justify-content: center;
    background-color: var(--dpurple);
    padding: 2vh 0vw;
  }

  .navbar {
    display: flex;
    column-gap: 4vw;
  }

  .navbar a {
    text-decoration: none;
    color: var(--white-smoke);
    font-size: 1.5em;
    padding: 1vh 1vw;
  }

  .navbar a:hover {
    background-color: var(--white-smoke);
    color: var(--dpurple);
  }

  .wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 20px;
    justify-content: center;
    background-color: var(--amethyst);
    color: var(--white-smoke);
    
    font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
    font: 25px;
    padding: 50px 70px 100px 70px;
    border-radius: 10px;
  }

  .default-button {
    background-color: var(--dpurple);
    color: var(--white-smoke);
    padding: 10px 15px;
    border-radius: 5px;
    margin-top: 20px;
    border: 0px;
  }

  .default-button:hover, #logout-button:hover {
    background-color: var(--white-smoke);
    color: var(--dpurple);
    cursor: pointer;
  }

  .auth-button {
    min-width: 200px;
  }

  h1 {
    font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
    -webkit-text-stroke: 2.5px var(--black);
    font-size: 56px;
  }

  h2 {
    font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
    -webkit-text-stroke: 1.5px var(--black);
    font-size: 35px;
  }

  #logout-button {
    color: var(--white-smoke);
    background-color: transparent;
    border: none;
    font-size: 1.5em;
    font-family: 'Times New Roman', Times, serif;
    padding: 1vh 1vw;
  }

  .default-start-div {
    display: flex;
    flex-direction: column;
    justify-content: start;
    gap: 5px;
  }

  .default-center-div {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}

</style>
