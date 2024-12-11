<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="nav-wrapper">
      <nav class="navbar">
        <RouterLink to="/" class="link_reset">Home</RouterLink>
        <RouterLink to="/registration" class="link_reset">Регистрация</RouterLink>
        <RouterLink to="/login" class="link_reset">Авторизация</RouterLink>
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
    font-size: 20px;
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
    padding: 100px;
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

  .default-button:hover {
    background-color: var(--white-smoke);
    color: var(--dpurple);
    cursor: pointer;
  }

  .auth-button {
    min-width: 200px;
  }

</style>
